from flask_restful import Resource
from sqlalchemy import func

from App.apis.apis_constant import HTTP_OK
from App.ext import db
from App.models.cinema.cinema_flight_model import Flight
from App.models.common.movie_model import Movie
from App.models.user.movie_order_model import MovieOrder


class MovieTopResource(Resource):
    def get(self):
        results = db.session.query(Movie.id,Movie.showname,func.sum(MovieOrder.o_price)).join(Movie.flight).join(Flight.movieorder).group_by(Movie.id).order_by(-func.sum(MovieOrder.o_price))

        print(results)
        print(type(results))
        for result in results:
            print(result)

        data = {
            'status':HTTP_OK,
            'msg':'ok',
            'data':results.all()
        }
        return data