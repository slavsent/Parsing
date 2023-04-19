# Scrapy settings for lm_goods project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "lm_goods"

SPIDER_MODULES = ["lm_goods.spiders"]
NEWSPIDER_MODULE = "lm_goods.spiders"

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

IMAGES_STORE = 'photos'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:111.0) Gecko/20100101 Firefox/111.0"


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}
#DEFAULT_REQUEST_HEADERS = {
#    'cookie':'qrator_ssid=1681824418.063.y8mB6198qMNc2KTG-4sg9rabbnmiv63qb9cmajgejcf3cdlpi; ggr-widget-test=0; cookie_accepted=true; _clientTypeInBasket=true; _gaexp=GAX1.2.uu_s8oSGRIuODfEn27HyEg.19530.0!IUgFRjY7S7qnkK4uRsCZRw.19540.2; x-api-option=srch-2705-default; iap.uid=97e1ac4f69924206817b6f856819d108; aplaut_distinct_id=cv3NMEpnXGDe; uxs_uid=b542d5f0-ddec-11ed-87ef-6944c634ebba; _gid=GA1.2.813898931.1681824426; sawOPH=true; GACookieStorage=GA1.2.1869059450.1681824424; _slfs=1681824642189; _slid=643e9b83303e0e11990f967f; _slsession=F8F24489-39C5-46FE-A8EC-8A346EB13B53; X-API-Experiments-sub=B; _regionID=34; _ga=GA1.2.1869059450.1681824424; _gat_UA-20946020-1=1; qrator_jsid=1681824417.306.M84wxTPQEq6G8Qhm-f8ekenkcbituig7e0bavgraff5g1v2d7; _ga_Z72HLV7H6T=GS1.1.1681824424.1.1.1681825306.0.0.0',
#}


# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "lm_goods.middlewares.LmGoodsSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "lm_goods.middlewares.LmGoodsDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "lm_goods.pipelines.LmPhotosPipeline": 200,
    "lm_goods.pipelines.LmGoodsPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
#TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
TWISTED_REACTOR = "twisted.internet.selectreactor.SelectReactor"
FEED_EXPORT_ENCODING = "utf-8"
