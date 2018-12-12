from .base_spider import BaseSpider


class JRCSpider(BaseSpider):
    name = "jrc.cz"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.xpath('//h1/text()').extract_first().strip()
        
        currency = u"K\u010d"
        nonBreakSpace = ' '
        try:
            item['price'] = float(
                response.css('[itemprop="price"]::text').extract_first().strip().replace(nonBreakSpace, '').replace(currency, '') or 0                
            )
        except:
            item['price'] = float(0)
            
        try:
            item['bazar'] = float(
                response.css('.preownCoste div.price::text').extract_first().strip().replace(nonBreakSpace, '').replace(currency, '') or 0                
            )
        except:
            item['bazar'] = float(0)
        yield item
