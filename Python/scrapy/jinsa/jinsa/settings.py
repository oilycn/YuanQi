# -*- coding: utf-8 -*-

# Scrapy settings for jinsa project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jinsa'

SPIDER_MODULES = ['jinsa.spiders']
NEWSPIDER_MODULE = 'jinsa.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jinsa (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'cookie': 'thw=cn; t=cf14c7bc25269d4e93f0be80767bb1de; cna=rV2aFftTWRECAatTOBf7WyFH; tracknick=%5Cu6238%5Cu51A2%5Cu5F69%5Cu52A0; lgc=%5Cu6238%5Cu51A2%5Cu5F69%5Cu52A0; tg=0; enc=egObbOl9uwvANvbVlJBxxru8siyVFcUfysjrycwi4ovEe81Bg1OGg2%2Blg8rPPatdZIHFhbBOo%2FyVmyKEAAXa3Q%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; UM_distinctid=16bdf70f715a11-017df98137cc7e-37617e02-100200-16bdf70f71671b; miid=828295062092357675; cookie2=1f8e5123eca652547aeebb50c6ad55a1; v=0; _tb_token_=348b3d1331bde; unb=3919142570; uc3=lg2=URm48syIIVrSKA%3D%3D&nk2=8twE35aCkxU%3D&id2=UNk2Q%2FXU5Gggfg%3D%3D&vt3=F8dBy3zUDxW4VfDm%2FYM%3D; csg=f935d240; cookie17=UNk2Q%2FXU5Gggfg%3D%3D; dnk=%5Cu6238%5Cu51A2%5Cu5F69%5Cu52A0; skt=c179b102daf46d2e; existShop=MTU2NDM2ODE5MA%3D%3D; uc4=nk4=0%408O8CHqwJdQvBzt8qUQug6HJASA%3D%3D&id4=0%40Ug48DQA0G3VtNIUeOnjuPuukkrVK; _cc_=URm48syIZQ%3D%3D; _l_g_=Ug%3D%3D; sg=%E5%8A%A004; _nk_=%5Cu6238%5Cu51A2%5Cu5F69%5Cu52A0; cookie1=V3id9%2F9eLoTYb7pbu7qzvcy1uLj3qd4rLxRSNT6mjME%3D; mt=ci=0_1; uc1=cookie14=UoTaHPv99%2Fkzag%3D%3D&lng=zh_CN&cookie16=W5iHLLyFPlMGbLDwA%2BdvAGZqLg%3D%3D&existShop=false&cookie21=WqG3DMC9FxUx&tag=8&cookie15=VT5L2FSpMGV7TQ%3D%3D&pas=0; JSESSIONID=32B89711170BB2455B253ED08634F6F9; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; isg=BDAwbV9BGQ24rsUSTjkVVy9LAfhC0Yen4Or7eSqBvwte5dCP04kwU4XfPa0g9cyb; l=cBavxbTPqxY7GeoyBOCaZuIJAob9tIRAguPRwn8Xi_5hG6Y_BDQOk2rYYFv6cjWdOeTp4GDd2Kw9-etXs0t6Qt--g3fP.',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jinsa.middlewares.JinsaSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'jinsa.middlewares.JinsaDownloaderMiddleware': 543,
#}
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'jinsa.middlewares.RandomUserAgent': 543,
}
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'jinsa.pipelines.JinsaPipeline': 300,
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
#USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
