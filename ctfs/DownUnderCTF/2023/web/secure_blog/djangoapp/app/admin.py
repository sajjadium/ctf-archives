from django.contrib import admin
from app.models import Article, Flag

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

@admin.register(Flag)
class FlagAdmin(admin.ModelAdmin):
    pass