﻿# coding:utf-8

import time
from peewee import *
from hashlib import md5
from random import Random
from model import BaseModel
from lib.state_obj import StateObject


def random_str(random_length=16):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


class USER_LEVEL(StateObject):
    DEL = 0
    BAN = 30
    NORMAL = 50
    MANAGER = 80
    ADMIN = 100

    txt = {DEL: '删除', BAN: '封禁', NORMAL: '正常', MANAGER: '管理', ADMIN: '超级管理'}


USER_LEVEL.init()


class User(BaseModel):
    username = TextField(index=True, unique=True)
    password = TextField()
    salt = TextField()

    key = TextField(index=True)
    level = IntegerField()

    reg_time = BigIntegerField()
    key_time = BigIntegerField()

    class Meta:
        db_table = 'users'

    def is_admin(self):
        return self.level == USER_LEVEL.ADMIN

    def refresh_key(self):
        self.key = random_str(32)
        self.key_time = int(time.time())
        self.save()

    def set_password(self, new_password):
        salt = random_str()
        password_md5 = md5(new_password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        self.salt = salt
        self.password = password_final
        self.save()

    @classmethod
    def new(cls, username, password):
        username = username.lower()
        salt = random_str()
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + salt).encode('utf-8')).hexdigest()
        level = USER_LEVEL.ADMIN if cls.count() == 0 else USER_LEVEL.NORMAL  # 首个用户赋予admin权限
        the_time = int(time.time())
        return cls.create(username=username, password=password_final, salt=salt, level=level, key=random_str(32),
                          key_time=the_time, reg_time=the_time)

    @classmethod
    def auth(cls, username, password):
        username = username.lower()
        try:
            u = cls.get(cls.username == username)
        except DoesNotExist:
            return False
        password_md5 = md5(password.encode('utf-8')).hexdigest()
        password_final = md5((password_md5 + u.salt).encode('utf-8')).hexdigest()
        if u.password == password_final:
            return u

    @classmethod
    def password_change(cls, username, password, new_password):
        username = username.lower()
        u = cls.auth(username, password)
        if u:
            u.set_password(new_password)
            u.refresh_key()
            return u

    @classmethod
    def exist(cls, username):
        username = username.lower()
        return cls.select().where(cls.username == username).exists()

    @classmethod
    def get_by_key(cls, key):
        try:
            return cls.get(cls.key == key)
        except DoesNotExist:
            return None

    @classmethod
    def get_by_username(cls, username):
        username = username.lower()
        try:
            return cls.get(cls.username == username)
        except DoesNotExist:
            return

    @classmethod
    def count(cls):
        return cls.select(cls.level > 0).count()

    @classmethod
    def duty(cls):
        time_now = int(time.time()) + (60 * 60 * 8)
        days = int(time_now / (60 * 60 * 24))
        who = days % cls.select().count()
        if who == 0:
            who = 5
        return cls.get_by_pk(who)
