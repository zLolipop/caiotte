# coding: utf-8

import scrapy
import json


class ScholarSpider(scrapy.Spider):
    name = 'scholart'
    allowed_domains = ["scholart.com"]

    def start_requests(self):
        with open('caiotte/spiders/start_urls_test.json', 'r') as f:
            urls = json.load(f)
        for url in urls['start_urls']:
            print(url)
            yield scrapy.Request(url, callback=self.parse_scholar)

    def _get_scholar_name(self, response):
        """
        parse the scholar name from response
        ::return: return scholar_name if exist else None
        """
        scholar_name = response.css('#scholarChineseName::attr(title)').extract()
        if not scholar_name:  # do this if chinese scholar_name is empty
            scholar_name = response.css('#scholarEnglishName::attr(title)').extract()

        return scholar_name[0].strip() if scholar_name else None

    def _get_scholar_email(self, response):
        email = response.xpath("//img[@id='emailimg']/@title").extract()
        return email[0].replace("[scholat]", "@")[:-14] if email else None

    def _get_scholar_title(self, response):
        title = response.xpath("//span[@id='scholarTitle']/@title")
        if title:
            raw_title = title.extract_first()
            return raw_title.replace('学术职务: ', '') if '学术职务: ' in raw_title else raw_title.replace('Scholar title:', '')

    def _get_scholar_org(self, response):
        work_place=response.xpath("//span[@id='scholarwork']/@title")
        if work_place:
            return work_place.extract_first().split(" \xa0 ")


    def parse_scholar(self, response):
        # scholar_name = self._get_scholar_name(response)
        # if scholar_name is None:
        #     return
        # scholar_email = self._get_scholar_email(response)
        # title = self._get_scholar_title(response)
        # org = self._get_scholar_org(response)
        # self.logger.info(org)
