# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from caiotte.entities import *
from caiotte.items import *
from pony import orm
from uuid import uuid1

class CaiottePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ScholarItem):
            self._scholar_storage(item)
        elif isinstance(item, FriendShip):
            self._friend_storage(item)
        elif isinstance(item, ScholarPaper):
            self._paper_storage(item)

    def _scholar_storage(self, item):
        org_list = item.get('org', None)
        org_detail = None
        org = None
        if org_list:
            org = org_list.pop(0)
            org_detail = ''.join(org_list)
        with orm.db_session:
            scholar = Scholar(scholar_id=uuid1().hex,
                              name = item.get('name'),
                              username= item.get('username'),
                              title = item.get('title', ''),
                              email = item.get('email', ''),
                              org   = org,
                              org_detail = org_detail,
                              biography = item.get('biography', ''),
                              study_field = item.get('study_field', ''),
                              page_url = item.get('page_url', ''),
                              img_url  = item.get('img_url', ''))

    def _paper_storage(self, item):
        username = item.get('scholar')
        papers = item.get('papers')
        with orm.db_session:
            scholar = Scholar.get(username=username)
            for title, summary, date, source in papers:
                Paper(paper_id=uuid1().hex,
                      title = title,
                      abstract = summary,
                      published_date = date,
                      source = source,
                      author=scholar)

    def _friend_storage(self, item):
        first_user  = item.get('first_user')
        second_user = item.get('second_user')
        with orm.db_session:
            user1 = Scholar.get(username=first_user)
            user2 = Scholar.get(username=second_user)
            print(user1.username, "="*5, user2.usernam)
