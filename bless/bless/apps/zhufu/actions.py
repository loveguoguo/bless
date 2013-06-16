#!/usr/bin/env python
# coding=utf8
from django.contrib import admin
from django.template.response import TemplateResponse
from forms import AddQuestionForm
from models import Question

def add_questions(modeladmin, request, queryset):
    '''批量添加问题'''
    opts = modeladmin.model._meta
    app_label = opts.app_label
    if request.POST.get('post'):
        form = AddQuestionForm([], 
                        initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)},
                        data = request.POST)
        n = queryset.count()
        if n:
            if form.is_valid():
                question = Question.objects.get(id=form.cleaned_data['question_id'])
                for article in queryset:
                    article.questions.add(question)
                modeladmin.message_user(request, '成功修改%d个产品'%n)
                return None
            else:
                modeladmin.message_user(request, '输入有误，请重新提交;%s'%str(form.errors))
                pass
        else:
            modeladmin.messag_user(request, '未选择任何数据')
            return None

    title = '添加问题'
    action = 'add_questions'
    form = AddQuestionForm([], initial={'_selected_action':
                                       [i.id for i in queryset]})
    context = {
            'title': title,
            'queryset': queryset,
            'count': queryset.count(),
            'opts': opts,
            'app_label': app_label,
            'action': action,
            'action_checkbox_name': admin.ACTION_CHECKBOX_NAME,
            'form': form,
        }
    return TemplateResponse(request, 'zhufu/admin/add_questions.html',
                            context=context, current_app=modeladmin.admin_site.name)
   
add_questions.short_description = '添加问题'
