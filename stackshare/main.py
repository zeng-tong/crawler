# -*-coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from stackshare.itemInfoGetter import ItemInfo

engine = create_engine('mysql+pymysql://root:@localhost/stackshare?charset=utf8')
DBSession = sessionmaker(bind=engine)

session = DBSession()
item = ItemInfo(app_url='/bootstrap')
stacks = item.get_stacks()
session.add(stacks)
session.commit()
session.close()
