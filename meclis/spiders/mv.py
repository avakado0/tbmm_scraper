import scrapy
from scrapy import Spider
from scrapy.http import Request
# from ..items import MeclisItem
import logging


class MeclisItem(scrapy.Item):
    name = scrapy.Field()
    party = scrapy.Field()
    bill_prop_count = scrapy.Field()
    quest_prop_count = scrapy.Field()
    speech_count = scrapy.Field()
    gen_dis_count = scrapy.Field()
    res_prop_count = scrapy.Field()


class MvSpider(Spider):
    name = 'mv'
    allowed_domains = ['tbmm.gov.tr']
    start_urls = ['https://www.tbmm.gov.tr/Milletvekilleri/liste']

    def parse(self, response):
        mv_list = mv_list = response.xpath("//ul[@class='list-group list-group-flush']") #taking all MPs listed
        for mv in mv_list:
            item = MeclisItem()
            item['name'] = mv.xpath("./li/div/div/a/text()").get() # MP's name taken
            item['party'] = mv.xpath("./li/div/div[@class='col-md-4 text-right']/text()").get().strip() #MP's party name taken
            partial_link = mv.xpath('.//div[@class="col-md-8"]/a/@href').get()
            full_link = response.urljoin(partial_link)
            yield Request(full_link, callback=self.mv_analysis, cb_kwargs={'item': item})

    def mv_analysis(self, response, item):
        billprop_link_path = response.xpath(".//a[contains(text(),'İmzası Bulunan Kanun Teklifleri')]/@href").get()
        billprop_link = response.urljoin(billprop_link_path)

        questionprop_link_path = response.xpath(".//a[contains(text(),'Sahibi Olduğu Yazılı Soru Önergeleri')]/@href").get()
        questionprop_link = response.urljoin(questionprop_link_path)

        speech_link_path = response.xpath(".//a[contains(text(),'Genel Kurul Konuşmaları')]/@href").get()
        speech_link = response.urljoin(speech_link_path)

        res_prop_link_path = response.xpath(".//a[contains(text(),'İmzası Bulunan Meclis Araştırma Önergeleri')]/@href").get()
        res_prop_link = response.urljoin(res_prop_link_path)

        gen_discus_link_path = response.xpath(".//a[contains(text(),'İmzası Bulunan Genel Görüşme Önergeleri')]/@href").get()
        gen_discus_link = response.urljoin(gen_discus_link_path)

        yield Request(billprop_link,
                      callback=self.bill_prop_counter,
                      cb_kwargs={'item': item, 'questionprop_link': questionprop_link,
                                 'speech_link': speech_link, 'res_prop_link': res_prop_link,
                                 'gen_discus_link': gen_discus_link
                                 })

    # COUNTING FUNCTIONS
    def bill_prop_counter(self, response, item, questionprop_link, speech_link, res_prop_link,gen_discus_link):
        billproposals = response.xpath("//tr[@valign='TOP']")
        item['bill_prop_count'] = len(billproposals)
        yield Request(questionprop_link,
                      callback=self.quest_prop_counter,
                      cb_kwargs={'item': item, 'speech_link': speech_link,'res_prop_link': res_prop_link,
                                 'gen_discus_link': gen_discus_link}) #number of question propoesals to be requested

    def quest_prop_counter(self, response, item, speech_link, res_prop_link, gen_discus_link):
        questionproposals = response.xpath("//tr[@valign='TOP']")
        item['quest_prop_count'] = len(questionproposals)
        yield Request(speech_link,
                      callback=self.speech_counter,
                      cb_kwargs={'item': item,'res_prop_link': res_prop_link,
                                 'gen_discus_link': gen_discus_link})  #number of speeches to be requested

    def speech_counter(self, response, item, res_prop_link,gen_discus_link):
        speeches = response.xpath("//tr[@valign='TOP']")
        item['speech_count'] = len(speeches)
        yield Request(gen_discus_link,
                      callback = self.gen_discus_counter,
                      cb_kwargs={'item': item, 'res_prop_link': res_prop_link})

    def gen_discus_counter(self, response, item, res_prop_link):

        discussions = response.xpath("//tr[@valign='TOP']")
        item['gen_dis_count'] = len(discussions)

        yield Request(res_prop_link,
                      callback = self.res_prop_counter,
                      cb_kwargs = {'item': item})

    def res_prop_counter(self, response, item):

        researches = response.xpath("//tr[@valign='TOP']")
        item['res_prop_count'] = len(researches)

        yield item


