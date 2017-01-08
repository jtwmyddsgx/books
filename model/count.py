# coding: utf-8
from model import BaseModel
from peewee import *


class Count(BaseModel):
    title = CharField()
    num = IntegerField()
    cost = FloatField()

    @classmethod
    def new(cls, title, num, cost):
        cls.create(title=title, num=num, cost=cost)

    @classmethod
    def record(cls, title, num, cost):
        try:
            recode = cls.get(cls.title == title)
        except DoesNotExist:
            return cls.new(title, num, cost)
        recode.num += num
        recode.save()

    @classmethod
    def get_all(cls):
        return cls.select()
