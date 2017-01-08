# coding:utf-8
import time

from model import pagination
from model.books import Books
from model.user import User
from view import route, url_for, View, LoginView


@route('/', name='index')
class Books_All(LoginView):
    def get(self):
        month = self.get_argument('month', None)
        cur_page = self.get_argument('cur_page', 1)
        trade = self.get_argument('trade', None)
        if trade == '入库':
            trading = 'in'
        elif trade == '出库':
            trading = 'out'
        else:
            trading = None
        shop = Books.get_all(month=month, trading=trading)
        _shop = Books.get_all(month=month)
        in_total = 0
        out_total = 0
        for i in _shop:
            if i.trading == 'in':
                in_total += i.cost * i.num
            elif i.trading == 'out':
                out_total += i.cost * i.num
        count_all = shop.count()

        page_size = 20
        if count_all > 0:
            shop_p = pagination(count_all=count_all, query=shop, page_size=page_size,
                                cur_page=cur_page)
        else:
            shop_p = None

        def time_readable(t):
            x = time.localtime(t)
            return time.strftime('%Y-%m-%d', x)

        self.render('index.html', shop_p=shop_p, time_readable=time_readable, out_total=out_total, in_total=in_total,
                    trade=trade)
