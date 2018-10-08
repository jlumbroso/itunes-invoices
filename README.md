# iTunes Invoice Scraper

This project is a command-line interface to retrieve receipts from iTunes invoices from your Apple account.

It uses a Python package called `browsercookie` to retrieve the login cookie from your Apple account.

## Example

Below, the CSV export is demonstrated:

```
$ python main.py
year,month,day,amount,reference,description
2018,07,02,$34.10,MM8809GT8K,"El Mundo"
2018,07,13,$34.09,MM88D0BGFK,"STARZ, STARZ® Monthly (Automatic Renewal); Spectrum"
2018,07,15,$0.00,R3KN94KMJDV,"WIRED Magazine"
2018,07,16,$0.00,R3KN9774TYM,"Heartfulness"
2018,07,21,$0.00,R3KN9LJH4FV,"Pingify App"
2018,07,23,$26.62,MM8902G84K,"The Horizon Leans Forward; Shazam, Ad free; Substitutions"
2018,07,28,$0.00,R3KNB3Z8Y58,"PressReader"
2018,07,29,$0.00,R3KNB5GK49S,"YNAB (You Need A Budget)"
2018,07,31,$0.00,R3KNB9N6T0B,"Twitchy - watch streams on TV"
2018,07,31,$0.00,R3KNB99DTWL,"Turbo: Scores-Income & Credit"
2018,08,02,$2.12,MM89FBN80J,"Reuters TV: Video News, Reuters TV Monthly (Automatic Renewal)"
2018,08,04,$0.00,R3KNBL821N2,"Udacity"
2018,08,04,$0.00,R3KNBL81BXN,"Brilliant – solve, learn, grow"
2018,08,11,$3.19,MM89X34BJ8,"Hiya Caller ID and Block, Hiya Premium - Monthly (Automatic Renewal)"
2018,08,13,$10.64,MM8B0748GQ,"Human Anatomy Atlas 2019; STARZ, STARZ® Monthly (Automatic Renewal)"
2018,08,17,$0.00,R3KNDLJYTHW,"Duolingo"
2018,08,20,$0.00,MM8B9TZWMW,"Duolingo, Duolingo Plus (Automatic Renewal); Episode - Choose Your Story; Geovelo : bike GPS"
2018,08,20,$0.00,R3KNDSSMTNX,"Tinycards - Fun Flashcards"
2018,08,22,$0.00,R3KNDYKGFQ9,"Lingvist: learn a language"
2018,08,29,$10.65,MM8BS306J5,"Duolingo, Duolingo Plus (Automatic Renewal)"
2018,08,30,$0.00,R3KNFK61919,"COOP ATM Shared Branch Locator"
2018,08,31,$0.00,R3KNFMFDK0T,"App in the Air"
2018,09,02,$2.12,MM8BZTK8TK,"Reuters TV: Video News, Reuters TV Monthly (Automatic Renewal)"
2018,09,06,$24.50,MM8D4D4TBZ,"TapeACall Pro: Call Recorder, Pro W/Unlimited Recording (Automatic Renewal); Sour Grapes"
2018,09,10,$0.00,R3KNGBBKXH7,"HiHello Contact Exchange"
2018,09,11,$3.19,MM8DDD5999,"Hiya Caller ID and Block, Hiya Premium - Monthly (Automatic Renewal)"
2018,09,13,$9.59,MM8DJ5SKY5,"STARZ, STARZ® Monthly (Automatic Renewal)"
2018,09,18,$0.00,R3KNGZ82JBM,"Lemonade Insurance"
2018,09,19,$0.00,R3KNH1SSM0V,"Smart Countdown Timer"
2018,09,24,$21.31,MM8F227DTL,"Younger, Season 5"
2018,09,24,$0.00,R3KNHBZXK0G,"Roadtrippers - Trip Planner"
2018,09,29,$26.65,MM8FDT6TBT,"AnkiMobile Flashcards"
2018,09,29,$10.65,MM8F8QXFKB,"Duolingo, Duolingo Plus (Automatic Renewal)"
2018,10,02,$2.12,MM8FFMKDV0,"Reuters TV: Video News, Reuters TV Monthly (Automatic Renewal)"
2018,10,07,$1.06,MM8FSYTL1M,"Heads Up!, Harry Potter"
```