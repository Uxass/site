
#from django_redis import get_redis_connection
#from django.utils import timezone
#
#class VisitCacheService:
#    def __init__(self, request, response):
#        self.request = request
#        self.response = response
#
#    def add_to_cache(self):
#        data = self._prepare_visit_data()
#        key = self._get_key_name()
#        redis_conn = get_redis_connection("default")
#        redis_conn.hmset(key, data)  # Сохранение данных в Redis в виде хеша
#
#    def _prepare_visit_data(self):
#        return {
#            'path': self.request.path,
#            'timestamp': self._get_timestamp()
#        }
#
#    def _get_key_name(self):
#        return f"visit:{self.request.path}"
#
#    def _get_timestamp(self):
#        # Логика вычисления временной метки на основе текущего времени
#        return timezone.now().strftime('%Y-%m-%d %H:%M:%S')




