from scrapy import cmdline
import sys
# 方法 1
# cmdline.execute('scrapy crawl yourspidername'.split())

# 方法 2
sys.argv = ['scrapy', 'crawl', 'jd']
cmdline.execute()