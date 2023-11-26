from django.shortcuts import render
from django.db import connection

# Create your views here.
from django.http import HttpResponse,HttpRequest
from .models import AdminUser,Blog,QueryHelper

def index(request:HttpRequest):
    return HttpResponse('Welcome to TPCTF')

def debug(request:HttpRequest):
    if request.method != 'POST':
        return HttpResponse('Welcome to TPCTF')
    username = request.POST.get('username')
    if username != 'admin':
        return HttpResponse('you are not admin.')
    password = request.POST.get('password')
    users:AdminUser = AdminUser.objects.raw("SELECT * FROM blog_adminuser WHERE username='%s' and password ='%s'" % (username,password))
    try:
        assert password == users[0].password
        q = QueryHelper(query="select flag from flag",debug=True,debug_sql="select sqlite_version()")
        response = q.run_debug()
        return HttpResponse(response)
    except:
        return HttpResponse('wrong password')

def search(request:HttpRequest):
    try:
        query_helper = QueryHelper("SELECT * FROM blog_blog WHERE id=%s",**request.GET.dict())
        result = query_helper.run(Blog)[0]
        return HttpResponse(result.content)
    except Exception as e:
        return HttpResponse('你来到了没有知识的荒原')
