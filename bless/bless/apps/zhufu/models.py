#!/usr/bin/env python
#-*-coding:utf8 -*-
from django.db import models
from django.db.models import signals
from taggit.managers import TaggableManager
from django.conf import settings
# Create your models here.

class Question(models.Model):
    content = models.CharField(max_length=255, verbose_name=u'问题内容')
    #answer = models.ManyToManyField(Article)
    posted = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        verbose_name = u'问题'
        verbose_name_plural = u'问题'
        ordering = ['-posted', ]
    
    def __unicode__(self):
        return self.content


class Article(models.Model):
    content = models.TextField(verbose_name=u'内容')
    #文件暂时存本地,以后要改到存云端,可以写一个FileField.storage
    #可参考:https://docs.djangoproject.com/en/dev/topics/files/
    #https://docs.djangoproject.com/en/dev/howto/custom-file-storage/
    imgurl = models.ImageField(upload_to='img', null=True, 
                                blank=True, verbose_name=u'图片链接')
    posted = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    tags = TaggableManager()
    questions = models.ManyToManyField(Question)    

    class Meta:
        verbose_name = u'祝福词'
        verbose_name_plural = u'祝福词'
        ordering = ['-posted', ]
    
    def __unicode__(self):
        return self.content

#from indexes import Index
#index = Index(settings.INDEX_ROOT)
#
#def post_question_save(sender, instance, created, *args, **kwargs):
#    if not instance.content:
#        return
#    data = {'id': instance.id, 'content':instance.content.encode('utf8')}
#    index._update_index(data)
#
#signals.post_save.connect(post_question_save, sender=Question, 
#                                    dispatch_uid='apps.zhufu.models')
