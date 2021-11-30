import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&noGeo=1',
                  ]
    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[contains(@class, 'icMQ_ bs_sM _3ze9n _1M2AW f-test-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//span[contains(@class, '_1e6dO _1XzYb _2EZcW')]//@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)



    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath("//h1//text()").get()
        salary = response.xpath("//span[@class='_2Wp8I _1e6dO _1XzYb _3Jn4o']//text()").getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)