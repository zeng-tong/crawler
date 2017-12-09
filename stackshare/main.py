# -*-coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from stackshare.item_info import itemInfo
from stackshare import get_item

engine = create_engine('mysql+pymysql://root:123456@138.197.95.94/stackshare?charset=utf8')
DBSession = sessionmaker(bind=engine)
session = DBSession()
categories = get_item.get_categories()


def start(start_pos, end_pos):
    for category in categories:
        ids = get_item.get_items_ids(category)
        limit_ids = []
        for i in range(start=start_pos, stop=end_pos):
            limit_ids.append(ids[i])
        items = get_item.get_item(limit_ids, category)
        for item in items:
            item = itemInfo(app_url=item['url'], name=item['name'])
            stacks = item.get_stacks()
            session.add(stacks)
            session.commit()
            session.close()


if __name__ == '__main__':
    start_pos, end_pos = input('There are too many stacks,download partly may better.input start and end position e.g: 1 10')
    start(start_pos=start_pos, end_pos=end_pos)