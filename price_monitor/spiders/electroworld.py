from .base_spider import BaseSpider


class ElectroWorldSpider(BaseSpider):
    name = "electroworld.cz"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.xpath('//h1/text()').extract_first().strip()
        
        currency = u"K\u010d"
        nonBreakSpace = u'\xa0'
        online = 0
        prodejna = 0
        try:
            if not response.xpath('//div[@id="product-buy-eshop"]//div[@class="disabled-box_message"]'):
                online = float(
                    response.css('[itemprop="price"]::text').extract_first().strip().replace(nonBreakSpace, '').replace(currency, '') or 0                
                )
        except:
            pass
        try:
            if not response.xpath('//div[@id="product-buy-store"]//div[@class="disabled-box_message"]'):
                prodejna = float(
                    response.css('#snippet-fullBuyBox-reservation-price > p.price > strong::text').extract_first().strip().replace(nonBreakSpace, '').replace(currency, '') or 0                
                )
        except:
            pass    
        if (online != 0) and (prodejna != 0):
            item['price'] = online if online <= prodejna else prodejna
        elif (online != 0) or (prodejna != 0):
            item['price'] = online if online != 0 else prodejna
        else:
            item['price'] = float(0)
            
        item['online'] = online
        item['prodejna'] = prodejna

        yield item
