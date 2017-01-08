# coding:utf-8
from model import pagination
from model.books import Books
from model.count import Count
from view import route, url_for, View, LoginView, NoLoginView, AdminView
from model.user import User
import time


@route('/record', name="record")
class Record(LoginView):
    def get(self):
        self.render('record.html')

    def post(self):
        user = self.current_user()
        title = self.get_argument('title')
        cost = self.get_argument('cost')
        num = self.get_argument('num')
        trading = self.get_argument('trading')
        str_time = self.get_argument('time_pay')
        num = 1 if not num else int(num)
        if str_time:
            time_pay = time.mktime(time.strptime(str_time, '%Y-%m-%d'))
        else:
            time_pay = None

        Books.new(title=title, num=num, cost=cost, trading=trading, user_id=user.id, _time=time_pay)

        self.redirect(url_for('index'))


@route('/count', name='count')
class Total(LoginView):
    def get(self):
        cur_page = self.get_argument('cur_page', 1)
        _count = Count.get_all()

        count_all = _count.count()
        page_size = 20
        if count_all > 0:
            the_count = pagination(count_all=count_all, query=_count, page_size=page_size,
                                   cur_page=cur_page)
        else:
            the_count = None

        self.render('count.html', the_count=the_count)


@route('/update/([0-9]+)', name='update')
class Update(AdminView):
    def get(self, record_id):
        record = Books.get_by_pk(record_id)

        if record:
            self.render('update.html', record=record)

    def post(self, record_id):
        title = self.get_argument('title')
        cost = self.get_argument('cost')
        num = self.get_argument('num')
        trading = self.get_argument('trading')
        str_time = self.get_argument('time_pay')
        num = 1 if not num else int(num)
        if str_time:
            time_pay = time.mktime(time.strptime(str_time, '%Y-%m-%d'))
        else:
            time_pay = None

        Books.update_record_by_id(record_id=record_id, title=title, num=num, cost=cost, trading=trading, _time=time_pay)
        self.redirect(url_for('index'))


@route('/remove/([0-9]+)', name='remove')
class Remove(AdminView):
    def get(self, record_id):
        _record = Books.get_by_pk(record_id)
        if _record:
            Books.remove_record_by_id(record_id)
            self.redirect(url_for('index'))
        else:
            self.redirect(url_for('index'))
