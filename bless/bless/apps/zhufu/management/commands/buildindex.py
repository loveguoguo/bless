#!/usr/bin/env python
#-*- coding:utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core.paginator import Paginator, EmptyPage
from django.conf import settings
from bless.apps.zhufu.indexes import Index
from bless.apps.zhufu.models import Question
import datetime

index = Index(settings.INDEX_ROOT)

class Command(BaseCommand):
    def handle(self, *args, **options):
        question_list = Question.objects.all()
        paginator = Paginator(question_list, 100)
        page = 1
        while True:
            try:
                questions = paginator.page(page)
                for q in questions:
                    data = {'id': q.id, 'content': q.content.encode('utf8')}
                    index._update_index(data)
                page = page + 1
            except EmptyPage:
                break
