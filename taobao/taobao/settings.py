# -*- coding: utf-8 -*-

# Scrapy settings for taobao project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'taobao'

SPIDER_MODULES = ['taobao.spiders']
NEWSPIDER_MODULE = 'taobao.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'taobao (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host':'s.taobao.com',
    'Referer':'https://www.taobao.com/?spm=a230r.1.1581860521.1.10f910b8o0ybKu',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0',
    'cookie': 'thw=cn; isg=BBERRi6tKB4_DEQK4dt-FLZ5Ixtr1haUwHoRP_OmSlj-mjLsO88VwCf4OO58iR0o; t=336ad5fbb287899f2132b0950b85454f; cookie2=1efb081dbd263d34ebd6ea511c1bd9cc; v=0; _tb_token_=eb3b639ae7ba8; cna=jXDFFazH524CAatTOAYxz/dQ; l=cBLRehTVqbBCf8_OBOCCiuIJAobOvIObYuPRwn8Xi_5aB6LIJaQOk2WEqFp6csWhG9YB4tkaIJptoU9_7s00hW064AadZ; unb=3919142570; uc1=cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&cookie14=UoTaHPvzOCicEw%3D%3D; uc3=id2=UNk2Q%2FXU5Gggfg%3D%3D&nk2=8twE35aCkxU%3D&vt3=F8dBy3zUDxz1eja8nMs%3D&lg2=W5iHLLyFOGW7aA%3D%3D; csg=ef68c253; lgc=%5Cu6238%5Cu51A2%5Cu5F69%5Cu52A0; cookie17=UNk2Q%2FXU5Gggfg%3D%3D; dnk=%5Cu6238%5Cu51A2%5Cu5F69%5Cu52A0; skt=0a2b1ff341a38408; existShop=MTU2NDM3Nzg0Mg%3D%3D; uc4=nk4=0%408O8CHqwJdQvBzt8qUQuhKbW63g%3D%3D&id4=0%40Ug48DQA0G3VtNIUeOnjuPuo2S5ZY; tracknick=%5Cu6238%5Cu51A2%5Cu5F69%5Cu52A0; _cc_=UtASsssmfA%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=%E5%8A%A004; _nk_=%5Cu6238%5Cu51A2%5Cu5F69%5Cu52A0; cookie1=V3id9%2F9eLoTYb7pbu7qzvcy1uLj3qd4rLxRSNT6mjME%3D; mt=ci=0_1; enc=Unl%2FX17O18EF0ifnBJ%2Bj1ghmbuD5Qc4o8Gh8wVBS8svSEtutYNmeGiPffMSNYHOleLttTWKRfZRMS3HskP2CqQ%3D%3D; _uab_collina=156437785241703537592333; JSESSIONID=19CCA5A373A377F0BE89E7103FD0B36C; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; hng=CN%7Czh-CN%7CCNY%7C156; x5sec=7b227365617263686170703b32223a226130393036343964356265313731373065666633313832303433636361623032434b66422b756b46454c32513774696b3474694c63426f4e4d7a6b784f5445304d6a55334d4473784d513d3d227d',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'taobao.middlewares.TaobaoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'taobao.middlewares.TaobaoDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'taobao.pipelines.TaobaoPipeline': 300,
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
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
