import scrapy
from scrapy.item import Item, Field


class StringUtil:

    def __init__(self):
        pass

    @staticmethod
    def get_first(in_list, if_empty):
        if len(in_list) > 0:
            return in_list[0]
        else:
            return if_empty

class XpathUtil:

    def __init__(self):
        pass

    @staticmethod
    def xpath_for_class(classname):
        return "*[contains(concat(' ', @class, ' '), ' " + classname + " ')]"        
        
class StackItem(Item):
    #author = Field()
    article_title = Field()
   # headline = Field()
    article_url = Field()
    article_summary = Field()
    article_tags = Field()

from scrapy import Spider
from scrapy.selector import Selector

#from stack.items import StackItem

class StackSpider(Spider):
    name = "isentiabbcade1234"
    allowed_domains = ["bbc.com"]
    start_urls =  ["http://www.bbc.com/"
    ]

    def parse(self,response):
        questions = Selector(response).xpath('//div[@class="media__content"]/h3')
      #  questions1 = Selector(response).xpath('//div[@class="media__content"]')
      #  questions2 = Selector(response).xpath('//div[@class="media__content"]')
        
        for question in questions:
            item = StackItem()
            item['article_title'] = question.xpath(
                    'a[@class="media__link"]/text()').extract()[0].strip(' \n')
            item['article_url'] = question.xpath(
                    'a[@class="media__link"]/@href').extract()[0].strip(' \n')
            article_url = ''.join(question.xpath(
                    'a[@class="media__link"]/@href').extract()[0].strip(' \n'))
            url = response.urljoin(article_url)
            yield scrapy.Request(url, callback=self.parse_dir_contents, meta=item)
     #       yield item

     #   for questiona in questions1:   
      #      item['article_summary'] = questiona.xpath(
      #              '//p[@class="media__summary"]/text()').extract()[0].strip(' \n')
       #     yield item
       # for questionb in questions2:
       #     item['article_tags'] = questionb.xpath(
       #             'a[@class="media__tag tag tag--news"]/text()').extract()[0].strip(' \n')
       #     yield item

    def parse_dir_contents(self, response):
          item = response.meta

          header = StringUtil.get_first(
            response.xpath("//" + XpathUtil.xpath_for_class("story-body__h1") + "/text()").extract(), "").strip(' \n')

          body_list = response.xpath("//" + XpathUtil.xpath_for_class("story-body__inner") + "//p/text()").extract()
          body = ' '.join(body_list).strip(' \n')

        #  header = response.xpath(
         #           '//h1[@class="story-body_h1"]/text()').extract()[0].strip(' \n')
        #StringUtil.get_first(
         #   response.xpath("//" + XpathUtil.xpath_for_class("story-body__h1") + "/text()").extract(), "").strip(' \n')

        #  body_list = response.xpath(
        #            '//p[@class="story-body__inner"]/text()').extract()[0].strip(' \n')
        #response.xpath("//" + XpathUtil.xpath_for_class("story-body__inner") + "//p/text()").extract()
        #  body = ' '.join(body_list).strip(' \n')

          item['header'] = header
          item['url'] = response.url
          item['body'] = body
          yield item
