# coding:utf-8
from model import BaseModel, month_begin_current_time, year_month_to_time, one_month
from peewee import *
import time

from model.count import Count


class Books(BaseModel):
    title = CharField()
    num = IntegerField()
    cost = FloatField()
    trading = CharField()
    user_id = IntegerField()
    time = BigIntegerField()

    @classmethod
    def new(cls, title, num, cost, trading, user_id, _time=None):
        if not _time:
            _time = time.time()
        cls.record_num(title, cost, num, trading)
        cls.create(title=title, num=num, cost=cost, trading=trading,
                   user_id=user_id, time=int(_time))

    @classmethod
    def get_all(cls, month=None, trading=None):
        """获取所有记录"""
        get_all = cls.select()
        if month:
            month1 = one_month(month)
            get_all = get_all.select().where(
                year_month_to_time(month) <= cls.time, cls.time < year_month_to_time(month1))
        if trading:
            get_all = get_all.select().where(cls.trading == trading)
        else:
            get_all = get_all.select().where(month_begin_current_time() <= cls.time)
        return get_all

    @classmethod
    def get_shop(cls, month=None):
        pass

    @classmethod
    def get_sell(cls, month=None):
        pass

    @classmethod
    def get_count(cls, month=None):
        _all = cls.get_all(month)
        category = {}
        for i in _all:
            _num = i.num if i.trading == 'in' else -i.num
            if i.title not in category:
                category[i.title] = {"num": _num, "cost": i.cost}
            else:
                category[i.title]["num"] += _num
        return category

    @classmethod
    def record_num(cls, title, cost, num, trading):
        if trading == "in":
            Count.record(title, num, cost)
        else:
            Count.record(title, -num, cost)

    @classmethod
    def update_record_by_id(cls, record_id, title, num, cost, trading, _time=None):
        record = cls.get_by_pk(record_id)
        if not record:
            return
        if record.trading == trading:
            if record.num != num:
                _num = record.num - num
                cls.record_num(title, cost, -_num, trading)
        elif (record.trading == 'in' and trading == 'out') or (record.trading == 'out' and trading == 'in'):
            _num = record.num + num
            cls.record_num(title, cost, _num, trading)

        record.title = title
        record.num = num
        record.cost = cost
        record.trading = trading
        if _time:
            record.time = _time
        record.save()

    @classmethod
    def remove_record_by_id(cls, record_id):
        _record = cls.get_by_pk(record_id)
        if _record:
            if _record.trading == 'in':
                cls.record_num(_record.title, _record.cost, _record.num, 'out')
            if _record.trading == 'out':
                cls.record_num(_record.title, _record.cost, _record.num, 'in')
            cls.delete_instance(_record)