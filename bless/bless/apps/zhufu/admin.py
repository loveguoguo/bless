#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.contrib import admin
from models import Article, Question


class AnswershipInline(admin.TabularInline):
    model = Article.questions.through

class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswershipInline,
    ]

class ArticleAdmin(admin.ModelAdmin):
    filter_horizontal = ('questions', )

admin.site.register(Article, ArticleAdmin)
admin.site.register(Question, QuestionAdmin)
