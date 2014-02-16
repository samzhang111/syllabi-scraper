#Scraper

Requirements: python 2.7, MySQL, redis, and requirements.txt

A python scraper that takes an input tab-separated file of IDs and URLs, and stores the HTML contents of the URLs into a MySQL database, keyed by ID.

###Run
set config variables in scraper/config.py and scraper/db_settings.py

initialize redis with python helpers/makequeue.py

python scraper/run_workers.py

###Settings
scraper/config.py - contains settings information

- num_workers = the number of parallel workers to create
- redis_name = the name of the redis database
- path = the location of the id-url text file
- timeout = the number of seconds before the worker raises a timeout exception
- wayback = false: scrape the url itself, true: scrape the wayback cache of the page

scraper/db_settings.py - database settings (MySQL)

helpers contains several useful files for setting up redis, peeking at scrape status, and cleaning up aborted scrapes.

###Todo
- Automatically scrape wayback machine on failure.
- Implement google cache support
- Fix sentinel values (the program idles on completion)
