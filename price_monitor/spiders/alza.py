from .base_spider import BaseSpider


class AlzaSpider(BaseSpider):
    name = "alza.cz"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.xpath('//h1/text()').extract_first().strip()
        
        currency = ",-"
        nonBreakSpace = u'\xa0'
                        
        #normalni cena
        try:
            item['price'] = float(
                response.css('.price_withVat::text').extract_first().strip().replace(nonBreakSpace, '').replace(currency, '') or 0
            )
        except:
            item['price'] = float(0)
            
        if item['price'] == 0:
            #slevove tornado
            try:
                item['price'] = float(
                    response.xpath('//tr[@class="pricenormal"]/td[@class="c2"]/span/text()').extract_first().strip().replace(nonBreakSpace, '').replace(currency, '') or 0
                )
            except:
                item['price'] = float(0)
        yield item
