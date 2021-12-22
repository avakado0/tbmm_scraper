# tbmm_scraper
A scrapy scraper to scrape the performance details of the MPs in the parliament of Turkey.

It works in 3 layers

    1) Accessing the link where all the MPs are listed
    2) Accessing the individual ling for each MP
    3) Accessing the relevant stats' link from the page of each MP
    
    
An output of the stats could be taken with the command below:

    scrapy crawl -o MP_stats.csv
