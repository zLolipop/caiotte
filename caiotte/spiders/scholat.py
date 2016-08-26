# coding: utf-8

import scrapy
import json
import uuid

from caiotte import items


class ScholarSpider(scrapy.Spider):
    name = 'scholart'
    allowed_domains = ["scholat.com"]

    def start_requests(self):
        with open('caiotte/spiders/start_urls_test.json', 'r') as f:
            urls = json.load(f)
        for url in urls['start_urls']:
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
        if not title:
            title = response.xpath("//span[@id='scholartitle']/@title")

        if title:
            raw_title = title.extract_first()
            return raw_title.replace('学术职务: ', '') if '学术职务: ' in raw_title else raw_title.replace('Scholar title:', '')

    def _get_scholar_org(self, response):
        work_place=response.css("#scholarwork").xpath('string(.)')
        if work_place:
            work_place_processed = work_place.extract_first().split()
            if len(work_place_processed) > 3:
                work_place_processed = [' '.join(work_place_processed)]
            return work_place_processed

    def _get_scholar_bio(self, response):
        biography = response.css("#个人简介").xpath("string(./parent::*//div[2])")
        if biography:
            return biography.extract_first().strip()

    def _get_study_field(self, response):
        study_field = response.css("#研究兴趣").xpath("string(./parent::*//div[2])")
        if study_field:
            return study_field.extract_first().strip()

    def _get_scholar_img(self, response):
        img_src = response.css('.profilePicture::attr(src)')
        if not img_src:
            img_src = response.css('.profilePictureEn::attr(src)')
        if img_src:
            img_url = img_src.extract_first()
            if 'default.png' in img_url:
                return None
            return img_url
        else:
            return None

    def parse_scholar(self, response):
        scholar_name = self._get_scholar_name(response)

        if scholar_name is None:
            return
        scholar_email = self._get_scholar_email(response)
        title = self._get_scholar_title(response)
        org = self._get_scholar_org(response)
        biography = self._get_scholar_bio(response)
        study_field = self._get_study_field(response)
        page_url = response.url
        username = page_url.split('/')[-1]
        img_url = self._get_scholar_img(response)

        self.logger.info("url is {url}------>{name}".format(url=page_url,name=scholar_name))

        target= items.ScholarItem(username=username,
                                  name=scholar_name,
                                  email=scholar_email,
                                  title=title,
                                  org=org,
                                  biography=biography,
                                  study_field=study_field,
                                  page_url=page_url,
                                  img_url=img_url)
        yield target


        # -----------------paper and friendship request------------------------

        paper_request = scrapy.FormRequest('http://www.scholat.com/getAcademic_Paper.html',
                                            formdata={'Entry':username},
                                            callback=self.parse_papers)
        paper_request.meta['username'] = username
        yield paper_request

        friend_request = scrapy.FormRequest('http://www.scholat.com/getPortalFriendsList.html',
                                             formdata={'Entry':username},
                                             callback=self.parse_friend)
        friend_request.meta['username'] = username
        yield friend_request
        # ---------------------------------------------------------------------

    def parse_papers(self, response):
        papers_info = json.loads(response.text)[0]
        if papers_info[0]['title'] == "没论文":
            return
        names = map(lambda paper: (paper['title'], paper['summary'], paper['date'], paper['source']), papers_info)
        username = response.meta['username']

        the_item = items.ScholarPaper(scholar=username, papers=names)
        yield the_item


    def parse_friend(self, response):
        friends_info = json.loads(response.text)
        if not friends_info:
            return

        username = response.meta['username']
        for friend in friends_info:
            friend_username = friend['username']
            yield scrapy.Request('http://www.scholat.com/{username}'.format(username=friend_username),
                                  callback=self.parse_scholar)
            yield items.FriendShip(first_user=username, second_user=friend_username)
