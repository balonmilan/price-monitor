from .base_spider import BaseSpider


class MironetSpider(BaseSpider):
    name = "mironet.cz"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.xpath('//h1/text()').extract_first().strip()
        try:
            currency = u"K\u010d"
            nonBreakSpace = u'\xa0'
            
            item['price'] = float(
                response.xpath('//div[@class="product_cena_box"]/span[@class="product_dph"]/text()').extract_first().strip().replace(nonBreakSpace, '').replace(currency, '') or 0
            )
        except:
            item['price'] = float(0)
        yield item
