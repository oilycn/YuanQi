import scrapy

class YuanSpider(scrapy.Spider):
    name = "yuan"
    start_urls = [
        'https://www.oxmo.cn/',
    ]

    def parse(self, response):
        yield {
            # return some results
            'title': response.css('.entry-title::text').extract_first(default='Missing').strip().replace('"', ""),
            'url': response.url,
            'article': response.css('.entry-content').extract(),
        }


        urls = response.css('a[href*="www.oxmo.cn/"]::attr(href)')#.re(r'https://www.oxmo.cn/.+?/$')     # find all sub urls
        for url in urls:
            yield response.follow(url, callback=self.parse)     # it will filter duplication automatically


