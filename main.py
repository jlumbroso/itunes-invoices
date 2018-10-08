import json
import os
import re
import sys
import datetime
from urllib.parse import urljoin
import logging

import browsercookie
import bs4
import click
import requests

_logger = logging.getLogger("iTunesInvoices")

APPLE_INVOICE_CACHE_FILE = ".apple.invoices.json"


APPLE_COOKIES = ["myacinfo"]
APPLE_COOKIES_CACHE = None
APPLE_ENDPOINT_BASE = "https://reportaproblem.apple.com"
APPLE_ENDPOINT_INVOICE_LIST = "/invoices/weborderIds.json"
APPLE_ENDPOINT_INVOICE_DETAIL = "/invoices/summaries/{invoice_id}.html"

def get_apple_cookie(as_string=False):
    """
    Extracts necessary cookies to retrieve Apple API endpoints from
    the local user's browsers. This method requires authentication
    through keychain, to gain access to the browser cookies.
    """
    
    # Check live cache first
    global APPLE_COOKIES_CACHE
    if APPLE_COOKIES_CACHE == None:
                
        # Grab cookie jar from all local browsers (will invoke keychain)
        full_cj = browsercookie.load()
        
        # Retrieve the Apple cookies
        apple_cj = [
            cookie
            for cookie in full_cj
            if cookie.name in APPLE_COOKIES
        ]
        
        # Update cache
        APPLE_COOKIES_CACHE = apple_cj

    else:
        apple_cj = APPLE_COOKIES_CACHE
    
    # Return as cookie list or string
    if as_string:
        return "; ".join(map(
            lambda c: "{}={}".format(c.name, c.value),
            apple_cj))

    return apple_cj

def fetch_invoice_list():
    r = requests.get(
        url=urljoin(
            APPLE_ENDPOINT_BASE,
            APPLE_ENDPOINT_INVOICE_LIST),
        params={
            "size": "100",
            "entityType": "invoices",
            "category": "all",
            "batchSize": "100",
        },
        headers={
            "Cookie": get_apple_cookie(as_string=True)
        }
    )

    if r.ok:
        try:
            data = r.json()
            invoices = list(data.get("idToHint", {}).keys())
            return invoices
        except JSONDecodeError:
            pass

    return []

def fetch_invoice(invoice_id):
    r = requests.get(
        url=urljoin(
            APPLE_ENDPOINT_BASE,
            APPLE_ENDPOINT_INVOICE_DETAIL).format(invoice_id=invoice_id),
        headers={
            "Cookie": get_apple_cookie(as_string=True)
        })

    if r.status_code == 200:
        soup = bs4.BeautifulSoup(
            r.content,
            from_encoding="utf8",
            features="html5lib")
        div = soup.find(name="div", attrs={"class": "ph-row"})

        # Extract fields
        desc_str = div.find(
            name="ul",
            attrs={"class": "purchaseLineItems"}).text.strip()
        f_desc = re.sub(r"[ \t\r]*\n[ \t\n\r]+", "; ", desc_str)
        
        ts_str = div.find(name="div", attrs={"class": "date"}).text.strip()
        f_date = datetime.datetime.strptime(ts_str, "%b %d, %Y").date()

        total_str = div.find(name="div", attrs={"class": "total"}).text
        f_total = re.findall(r"\$[0-9]+\.[0-9]+", total_str)[0]

        return {
            "id": invoice_id,
            "date": f_date,
            "total": f_total,
            "description": f_desc
        }

def _to_json(python_object):
    if isinstance(python_object, datetime.date):
        return {'__class__': 'datetime.date',
                '__value__': python_object.strftime('%Y-%m-%d')}
    if isinstance(python_object, bytes):
        return {'__class__': 'bytes',
                '__value__': list(python_object)}
    raise TypeError(repr(python_object) + ' is not JSON serializable')

def _from_json(obj):
    # Check if this is serialized in our way
    _class_type = obj.get('__class__')
    if not _class_type:
        return obj
    
    # Apply conversion
    val = obj.get('__value__', "")
    if _class_type == "datetime.date":
        return datetime.datetime.strptime(val, '%Y-%m-%d')
    elif _class_type == "bytes":
        return bytes(val)
    
    raise Exception('Unknown {}'.format(_class_type))

def get_username():
    r = requests.get(
        url=APPLE_ENDPOINT_BASE,
        headers={
            "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) " +
                           "AppleWebKit/537.36 (KHTML, like Gecko) " +
                           "Chrome/69.0.3497.100 Safari/537.36"),
            "Cookie": get_apple_cookie(as_string=True)
        }
    )
    if r.ok:
        soup = bs4.BeautifulSoup(
            r.content,
            from_encoding="utf8",
            features="html5lib")
        username = soup.find(name="a", attrs={"id": "login-info-dropdown"}).text.strip()
        if username != "":
            return username

def get_invoices():
    invoices = {}

    # Load the cache
    filepath = os.path.expanduser(os.path.join("~", APPLE_INVOICE_CACHE_FILE))
    if os.path.exists(filepath):
        try:
            _logger.debug("Preparing to load invoice cache")
            _logger.debug("Cache path: {}".format(filepath))
            invoices = json.loads(open(filepath).read(), object_hook=_from_json)
            _logger.debug("Successfully read {} records from cache".format(len(invoices)))
        except:
            _logger.debug("Exception occurred while reading cache")

    # Fill `invoices` dict or update it with most recent invoices
    invoice_list = fetch_invoice_list()
    _logger.debug("Retrieved list of invoices: {}".format(", ".join(invoice_list)))
    newly_fetched = 0
    for invoice_id in invoice_list:

        if not invoice_id in invoices:
            invoice = fetch_invoice(invoice_id)
            _logger.debug("Fetched invoice {}: {}".format(invoice_id, invoice))
            invoices[invoice_id] = invoice
            newly_fetched += 1

    # Store the cache
    try:
        _logger.debug(
            "Preparing to store invoice cache ({} records, {} newly fetched)".format(
                len(invoices), newly_fetched))
        _logger.debug("Cache path: {}".format(filepath))
        with open(filepath, "w") as f:
            json_str = json.dumps(invoices, indent=2, default=_to_json)
            _logger.debug("Converting to JSON string ({})".format(len(json_str)))
            f.write(json_str)
            _logger.debug("Successfully wrote to {}".format(filepath))
            f.flush()
            f.close()
    except:
        _logger.debug("Exception occurred while writing cache")

    return invoices


@click.command()
def cli_root():
    pass


if __name__ == "__main__" and len(sys.argv) > 0 and sys.argv[0] != "":
    # Pretty printing of log messages
    try:
        from nicelog import setup_logging
        setup_logging(debug=True)
    except ImportError:
        pass

    # Click function
    cli_root()
