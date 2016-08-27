# -*- coding: utf-8 -*-

from pony import orm
from uuid import UUID, uuid1


db = orm.Database()

class Scholar(db.Entity):
    scholar_id  = orm.PrimaryKey(str)
    name        = orm.Required(str)
    username    = orm.Required(str, unique=True)
    title       = orm.Optional(str, nullable=True)
    email       = orm.Optional(str, nullable=True)
    org         = orm.Optional(str, nullable=True)
    org_detail  = orm.Optional(str, nullable=True)
    biography   = orm.Optional(orm.LongStr, nullable=True)
    study_field = orm.Optional(orm.LongStr, nullable=True)
    page_url    = orm.Optional(str, 512, nullable=True)
    img_url     = orm.Optional(str, 512, nullable=True)

    papers      = orm.Set('Paper')
    fs          = orm.Set('Friend', reverse='scholar1')
    fs2         = orm.Set('Friend', reverse='scholar2')


class Friend(db.Entity):
    friend_id = orm.PrimaryKey(str)
    scholar1  = orm.Required(Scholar, reverse='fs')
    scholar2  = orm.Required(Scholar, reverse='fs2')
    orm.composite_key(scholar1, scholar2)

class Paper(db.Entity):
    paper_id       = orm.PrimaryKey(str)
    title          = orm.Required(str)
    abstract       = orm.Optional(orm.LongStr)
    published_date = orm.Optional(str)
    source         = orm.Optional(orm.LongStr)
    author         = orm.Required(Scholar)

class FriendTemp(db.Entity):
    scholar1_name = orm.Required(str)
    scholar2_name = orm.Required(str)

class PaperTemp(db.Entity):
    title          = orm.Required(str)
    abstract       = orm.Optional(orm.LongStr)
    published_date = orm.Optional(str)
    source         = orm.Optional(orm.LongStr)
    author_name    = orm.Required(str)



db.bind('mysql', host='localhost', user='root', passwd='zzg550413470', db='scholar')
db.generate_mapping(create_tables=True)
