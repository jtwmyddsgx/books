# coding:utf-8

import math

import time

import datetime

import config
import peewee
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict

db = connect(config.DATABASE_URI)


class BaseModel(peewee.Model):
    class Meta:
        database = db

    def to_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_by_pk(cls, value):
        try:
            return cls.get(cls._meta.primary_key == value)
        except cls.DoesNotExist:
            return

    @classmethod
    def exists_by_pk(cls, value):
        return cls.select().where(cls._meta.primary_key == value).exists()


def pagination(count_all, query, page_size, cur_page=1, nearby=2):
    """
    :param count_all: count of all items
    :param query: a peewee query object
    :param page_size: size of one page
    :param cur_page: current page number, accept string digit
    :return: num of pages, an iterator
    """
    if type(cur_page) == str:
        cur_page = int(cur_page) if cur_page.isdigit() else 1
    elif type(cur_page) == int:
        if cur_page <= 0:
            cur_page = 1
    else:
        cur_page = 1

    page_count = int(math.ceil(count_all / page_size))
    items_length = nearby * 2 + 1

    # if first page in page items, first_page is None,
    # it means the "go to first page" button should not be available.
    first_page = None
    last_page = None

    prev_page = cur_page - 1 if cur_page != 1 else None
    next_page = cur_page + 1 if cur_page != page_count else None

    if page_count <= items_length:
        items = range(1, page_count + 1)
    elif cur_page <= nearby:
        # start of items
        items = range(1, items_length + 1)
        last_page = True
    elif cur_page >= page_count - nearby:
        # end of items
        items = range(page_count - items_length + 1, page_count + 1)
        first_page = True
    else:
        items = range(cur_page - nearby, cur_page + nearby + 1)
        first_page, last_page = True, True

    if first_page:
        first_page = 1
    if last_page:
        last_page = page_count

    return {
        'cur_page': cur_page,
        'prev_page': prev_page,
        'next_page': next_page,

        'first_page': first_page,
        'last_page': last_page,

        'page_numbers': items,
        'page_count': page_count,

        'items': query.paginate(cur_page, page_size),
        'count_all': count_all,
    }


def today_time():
    now_time = time.time()
    local_time = time.localtime(now_time)
    # 由于时区问题，当天00：00的时间戳不可直接用秒计算
    year = local_time.tm_year
    mon = local_time.tm_mon
    mday = local_time.tm_mday
    str_time = str(year) + '-' + str(mon) + '-' + str(mday) + ' 00:00:00'
    today_t = time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S'))
    return today_t


def monday_time():
    now_time = time.time()
    local_time = time.localtime(now_time)
    wday = local_time.tm_wday
    year = local_time.tm_year
    mon = local_time.tm_mon
    mday = local_time.tm_mday
    str_time = str(year) + '-' + str(mon) + '-' + str(mday) + ' 00:00:00'
    monday_t = time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S'))
    monday_t -= 60 * 60 * 24 * wday  # 算出星期一 00:00的时间戳
    return monday_t


def month_begin_current_time():
    now_time = time.time()
    local_time = time.localtime(now_time)
    year = local_time.tm_year
    mon = local_time.tm_mon
    str_time = str(year) + '-' + str(mon) + '-' + str(1) + ' 00:00:00'
    month_begin_t = time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S'))
    return month_begin_t


def month_begin_last_time():
    now_time = time.time()
    local_time = time.localtime(now_time)
    year = local_time.tm_year
    mon = local_time.tm_mon
    mon -= 1
    if mon == 0:
        year -= 1
        mon = 12
    str_time = str(year) + '-' + str(mon) + '-' + str(1) + ' 00:00:00'
    month_begin_t = time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S'))
    return month_begin_t


def month_begin_time():
    now_time = time.time()
    local_time = time.localtime(now_time)
    year = local_time.tm_year
    mon = local_time.tm_mon
    mon -= 1
    if mon == 0:
        year -= 1
        mon = 12
    str_time = str(year) + '-' + str(mon) + '-' + str(1) + ' 00:00:00'
    month_begin_t = time.mktime(time.strptime(str_time, '%Y-%m-%d %H:%M:%S'))
    return month_begin_t


def year_month_to_time(date):
    return int(time.mktime(time.strptime(date, '%Y-%m')))


def one_month(date, reverse=None):
    m = date.split("-")
    if not reverse:
        if int(m[1]) == 12:
            m[1] = str(1)
            m[0] = str(int(m[0]) + 1)
        else:
            m[1] = str(int(m[1]) + 1)
    else:
        if int(m[1]) == 1:
            m[1] = str(12)
            m[0] = str(int(m[0]) - 1)
        else:
            m[1] = str(int(m[1]) - 1)
    return m[0] + "-" + m[1]

if __name__ == "__main__":
    print(one_month(time.strftime("%Y-%m", time.localtime(time.time())), reverse=True))
