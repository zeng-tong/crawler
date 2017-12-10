# -*- coding: utf-8 -*-
from stackshare import get_item
from stackshare.exceptions import InvalidValueException
from stackshare.item_info import itemInfo
from stackshare.utils import mysql_session

categories = get_item.get_categories()


def start(start_pos, end_pos):
    for category in categories:
        ids = get_item.get_items_ids(category)
        if start_pos > len(ids):
            raise InvalidValueException(msg='Under category %s list ids max lenth is %s' % (category, len(ids)))
        if end_pos > len(ids):
            end_pos = len(ids) - 1

        slice_ids = []
        for i in range(start_pos, end_pos):
            slice_ids.append(ids[i])

        items = get_item.get_item(slice_ids, category)
        for item in items:
            try:
                session = mysql_session()
                item = itemInfo(app_url=item['url'], name=item['name'])
                stacks = item.get_stacks()
                session.add(stacks)
                session.commit()
                print(stacks.name + ' succed...')
                session.close()
            except Exception as e:
                print(e)
    print('Process finished...')


if __name__ == '__main__':
    start_pos, end_pos = map(int, input('There are too many stacks,download partly may better.input start and end position e.g: 1 10 \n').split())
    start(start_pos=start_pos, end_pos=end_pos)