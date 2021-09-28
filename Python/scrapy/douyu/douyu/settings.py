# -*- coding: utf-8 -*-

# Scrapy settings for douyu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'douyu'

SPIDER_MODULES = ['douyu.spiders']
NEWSPIDER_MODULE = 'douyu.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'douyu (+http://www.yourdomain.com)'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

LOG_LEVEL = 'WARNING'

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Host0':'www.douyu.com',
   'Accept-Encoding':'gzip, deflate, br',
   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
   'Referer':'https://www.douyu.com/directory/all',
   'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0',
   'Cookie0':'dy_did=9372576ce15c6569d21e047700041501; acf_did=9372576ce15c6569d21e047700041501; Hm_lvt_e99aee90ec1b2106afe7ec3b199020a7=1564460377; Hm_lpvt_e99aee90ec1b2106afe7ec3b199020a7=1564460431; smidV2=201907301220063f505ea4630ca799c202562f4b52958a009bcc678ba36e3d0; PHPSESSID=ivfi3vu7a9r2jbqfs45t284191; acf_auth=4def0sIVPniXZv3paaU8Eum%2BA7BrfI9qggUfTs6l1WUoVI2gBw0s9wCBQAvRlufgBPFekfrrAs1R18zKwLJ407RTk2GoGlep9tTv5Q8VGx%2FPn3bez3f1klo; wan_auth37wan=4c6013301d2fgBPoctGr4CNBqykUXrIyanYG21fda71fYqw%2BnS7j3PtBtsi7ZfGn4OOSAc3V4WaujBCR49mpp6TD0VEUTuLU0l11jlph1o85nmb%2F; acf_uid=2108120; acf_username=qq_kQ2r9QCI; acf_nickname=%E6%88%91%E5%B7%B2%E6%87%92%E5%BE%97%E6%97%A0%E8%8D%AF%E5%8F%AF%E6%95%91; acf_own_room=0; acf_groupid=1; acf_phonestatus=1; acf_avatar=https%3A%2F%2Fapic.douyucdn.cn%2Fupload%2Favanew%2Fface%2F201612%2F16%2F21%2F06aa1595ee4c67e0f544e07385c67ae0_; acf_ct=0; acf_ltkid=52770152; acf_biz=1; acf_stk=e01142abeab073e6',

}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'douyu.middlewares.DouyuSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'douyu.middlewares.DouyuDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'douyu.pipelines.DouyuPipeline': 300,
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
