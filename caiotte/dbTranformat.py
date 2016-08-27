# coding: utf-8

from entities import *
from pony import orm
from uuid import uuid1


@orm.db_session
def transform_friend():
    friends = orm.select((fs.scholar1_name, fs.scholar2_name) for fs in FriendTemp)
    for first_name, second_name in friends:
        first_user = Scholar.get(username=first_name)
        second_user= Scholar.get(username=second_name)
        if not first_user or not second_user:
            print("pass a null user")
            continue
        if first_user.scholar_id > second_user.scholar_id:
            first_user, second_user = second_user, first_user
        Friend(friend_id=uuid1().hex,
               scholar1 = first_user,
               scholar2 = second_user)

@orm.db_session
def transform_paper():
    papers = orm.select(pa for pa in PaperTemp)
    for paper in papers:
        author_name = paper.author_name
        author = Scholar.get(username=author_name)
        title = paper.title
        abstract = paper.abstract
        published_date = paper.published_date
        source = paper.source
        Paper(paper_id = uuid1().hex,
              title = title,
              abstract= abstract,
              published_date=published_date,
              source=source,
              author=author)

if __name__ == '__main__':
    transform_friend()
    transform_paper()
