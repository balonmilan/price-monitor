from .base_spider import BaseSpider


class LanShopSpider(BaseSpider):
    name = "lan-shop.cz"

    def parse(self, response):
        item = response.meta.get('item', {})
        item['url'] = response.url
        item['title'] = response.xpath('//h1/a/text()').extract_first().strip()
        try:
            currency = u"K\u010d"
            nonBreakSpace = u'\xa0'
            
            item['price'] = float(
                response.css('span[itemprop="price"]::text').extract_first().strip().replace(nonBreakSpace, '').replace(currency, '').replace(' ', '') or 0
            )
        except:
            item['price'] = float(0)
        yield item
