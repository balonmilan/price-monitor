from .base_spider import BaseSpider


class XZoneSpider(BaseSpider):
    name = "xzone.cz"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.xpath('//h2[@class="none-flash"]/text()').extract_first().strip()
        
        currency = u"K\u010d"
        nonBreakSpace = ' '
        try:
            item['price'] = float(
                response.xpath('//td[@class="cena"]//span[@class="color"]/text()').extract_first().strip().replace(nonBreakSpace, '').replace(currency, '') or 0
            )
        except:
            item['price'] = float(0)
            
        try:
            item['bazar'] = float(
                 response.xpath('//div[@class="panel-175"]/div/span[2]/text()').extract_first().strip().replace("ZA ", '').replace(nonBreakSpace, '').replace(currency, '') or 0
            )
        except:
            item['bazar'] = float(0)
        yield item
