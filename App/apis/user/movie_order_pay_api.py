from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from flask_restful import Resource

from App.apis.apis_constant import HTTP_OK
from App.apis.user.movie_user_utils import login_require
from App.models.cinema.cinema_flight_model import Flight
from App.models.common.movie_model import Movie
from App.models.user.movie_order_model import MovieOrder
from App.settings import ALIPAY_APPID, ALIPAY_PRIVATE_KEY, ALIPAY_PUBLIC_KEY

class MovieOrderPayResource(Resource):
    @login_require
    def get(self,order_id):
        order = MovieOrder.query.get(order_id)
        total_price = order.o_price
        flight = Flight.query.get(order.o_flight_id)
        movie = Movie.query.get(flight.f_movie_id)

        # Alipay Client
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = 'https://openapi.alipaydev.com/gateway.do'

        alipay_client_config.app_id = ALIPAY_APPID
        alipay_client_config.app_private_key = ALIPAY_PRIVATE_KEY
        alipay_client_config.alipay_public_key = ALIPAY_PUBLIC_KEY
        client = DefaultAlipayClient(alipay_client_config=alipay_client_config)

        model = AlipayTradePagePayModel()
        model.out_trade_no = "pay2018050200005262"
        model.total_amount = total_price
        model.subject = movie.showname
        model.body = order.o_seat
        model.product_code = "FAST_INSTANT_TRADE_PAY"

        pay_request = AlipayTradePagePayRequest(biz_model=model)
        pay_request.notify_url = 'https://ruoxianer.github.io/'
        pay_request.return_url = 'https://ruoxianer.github.io/'

        # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
        response = client.page_execute(pay_request, http_method="GET")
        # print("alipay.trade.page.pay response:" + response)
        data = {
            'msg':'ok',
            'status':HTTP_OK,
            'data':{
                'pay_url':response,
                'order_id':order_id
            }
        }
        return data
