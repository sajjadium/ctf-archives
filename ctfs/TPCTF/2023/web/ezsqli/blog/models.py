from django.db import models
from django.db import connection

class AdminUser(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class Blog(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    content = models.TextField()

class QueryHelper:
    debug_query = []
    query = ""
    def __init__(self,query,**kwargs):
        self.query = query
        print(kwargs)
        if kwargs.get("debug"):
            self.debug_query.append(kwargs.get("debug_sql"))
        self.parameters = kwargs.get("params")
        print(self.debug_query)


    def run(self,obj):
        return obj.objects.raw(self.query,self.parameters)

    def append_debug_sql(self,sql):
        self.debug_query.append(sql)

    def run_debug(self):
        response = ""
        print(self.debug_query)
        with connection.cursor() as cursor:
            cursor.execute(self.debug_query[0])
            result = cursor.fetchone()
            response += str(result)
        return response
