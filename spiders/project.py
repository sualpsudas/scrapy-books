import scrapy


class ProjectSpider(scrapy.Spider):
    name = 'project'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com//']

    def parse(self, response):
        
        linkler=response.xpath("//article[@class='product_pod']/h3/a/@href").getall()
        for i in linkler:
            sayfa=response.urljoin(i)
            yield scrapy.Request(url=sayfa,callback=self.parse2)
        next_page=response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            full_link=response.urljoin(next_page)
            yield scrapy.Request(url=full_link,callback=self.parse)
    
    def parse2(self,response):
        kutu=response.xpath("//div[@class='col-sm-6 product_main']")
        isim=kutu.xpath(".//h1/text()").get()
        fiyat=kutu.xpath(".//p[@class='price_color']/text()").get()
        stok=kutu.xpath(".//p[@class='instock availability']/text()").getall()[1].split("\n")[2]
        isim={"isim":isim}
        fiyat={"fiyat":fiyat}
        stok={"stok":stok}
        son={**isim,**fiyat,**stok}
        yield son