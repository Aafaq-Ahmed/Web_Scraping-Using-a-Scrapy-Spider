import scrapy

class CoronavirusSpider(scrapy.Spider):
    name = 'coronavirus'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/coronavirus']

    def parse(self, response):
        for country in response.xpath("//td/a"):
            name=country.xpath(".//text()").get()
            link=country.xpath(".//@href").get()
            #absolute_url=f"https://www.worldometers.info/coronavirus/{link}"
            absolute_url=response.urljoin(link)

            # yield{
            #     'country_name':name,
            #     'country_link':absolute_url
            # }
            if link:
                yield response.follow(url=link,callback=self.page2parser , meta={'country_name': name})

    
    def page2parser(self , response):
        country_name=response.request.meta["country_name"]
        active_cases=response.xpath('(//div[@class="maincounter-number"])[1]/span/text()').get()
        deaths=response.xpath('(//div[@class="maincounter-number"])[2]/span/text()').get()
        recovered=response.xpath('(//div[@class="maincounter-number"])[3]/span/text()').get()

        yield{
            'name' : country_name,
            'active_cases':active_cases,
            'deaths': deaths,
            'recovered':recovered
        }


    
            
