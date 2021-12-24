# tbmm_scraper
A scraper to scrape the performance details of MPs from different categories in the parliament of Turkey.

Categories to scrape for each MP of TBMM (parliament of Turkey:

-The number of bill proposals that each MP has their signature on (Kanun Teklifi Sayısı)
-The number of written parliamentary questions that each MP has their signature on  (Yazılı Soru Önergesi Sayısı)
-The number of interpalletions that each MP has their signature on (Genel Görüşme Önergesi Sayısı)
-The number of investigative questions (Araştırma Önergesi Sayısı)
-The number of parliamentary councel that the MP gave a speech (Genel Kurul Konuşması Sayısı)

It works in 3 layers

    1) Accessing the link where all the MPs are listed
    2) Accessing the individual ling for each MP
    3) Accessing the relevant stats' link from the page of each MP
    
    
An output of the stats could be taken with the command below:

    scrapy crawl -o MP_stats.csv
