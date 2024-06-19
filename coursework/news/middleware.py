#from django.utils.deprecation import MiddlewareMixin
#from .models import Visit
#
#class VisitMiddleware(MiddlewareMixin):
#    def process_view(self, request, view_func, view_args, view_kwargs):
#        # Получите путь к странице
#        path = request.path
#
#        # Сохраните посещение в базе данных
#        Visit.objects.create(path=path)
#
#        return None

#from django.http import HttpResponse
#from django.utils.deprecation import MiddlewareMixin
#
#from coursework.news import visit_cache_service
#
#
#
#class VisitCacheMiddleware(MiddlewareMixin):
#    def process_response(self, request, response):
#        service = visit_cache_service(request, response)
#        service.add_to_cache()
#        return response

import datetime
from django.utils.deprecation import MiddlewareMixin
from django_redis import get_redis_connection
from django.contrib.auth.models import User

class VisitCacheService:
    def __init__(self, request, response):
        self.request = request
        self.response = response

    def add_to_cache(self):
        data = self._prepare_visit_data()
        key = self._get_key_name()
        redis_conn = get_redis_connection("default")
        redis_conn.hmset(key, data)  # Save data to Redis as a hash

    def _prepare_visit_data(self):
        user = self.request.user if self.request.user.is_authenticated else None
        username = user.username if user else "Anonymous"
        return {
            'path': self.request.path,
            'timestamp': self._get_timestamp(),
            'username': username
        }

    def _get_key_name(self):
        return f"visit:{self.request.path}"

    def _get_timestamp(self):
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        return timestamp

class VisitCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        service = VisitCacheService(request, response)
        service.add_to_cache()
        return response



