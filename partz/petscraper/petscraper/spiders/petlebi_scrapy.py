import scrapy

class PetspiderSpider(scrapy.Spider):
    name = "petspider"
    page_number = 2
    start_urls = ["https://www.petlebi.com/alisveris/ara?page=1"]

    custom_settings = {
        'FEEDS' : {
            'petdata.json': {'format': 'json', 'overwrite': True},

        }
    }

    def parse(self, response):
    
        stocked_products = response.css('div.card.mb-4')
        for stocked_product in stocked_products:
            relative_url =  stocked_product.css('div a ::attr(href)').get()   
            pet_url = relative_url
            yield response.follow(pet_url, callback=self.parse_pet_page)


        next_page = 'https://www.petlebi.com/alisveris/ara?page='+ str(PetspiderSpider.page_number)

        if PetspiderSpider.page_number < 216:
            PetspiderSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)
    
        
    def parse_pet_page(self, response):
        
        yield{
            'url' : response.url,
            'name' : response.css('h1.product-h1::text').get(),
            'barcode' : response.xpath('//*[@id="hakkinda"]/div[3]/div[2]/text()').get(),               
            'price' : response.xpath('/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div[1]/p/span/text()').get(),
            'description' : response.xpath('//*[@id="productDescription"]/p[2]/text()').get(),
            'category' : response.xpath("(//a[@itemprop='item']/@title)[last()-1]").get(),
            'brand': response.xpath('//*[@id="hakkinda"]/div[1]/div[2]/span/a/text()').get(),
            'stock': response.xpath('/html/body/div[3]/div[2]/div/div/div[2]/div[5]/div[2]/a/span/text()').get()
            }                        
 
    