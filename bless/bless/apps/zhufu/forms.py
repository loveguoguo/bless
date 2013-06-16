#!/usr/bin/env python
#coding=utf8
from django import forms
from models import Question

class AddQuestionForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    
    def __init__(self, question_choices=[], *args, **kwargs):
        super(AddQuestionForm, self).__init__(*args, **kwargs)
        if not question_choices:
            question_choices = [(q.id, q.content) for q in Question.objects.all()]    
        question_id = forms.ChoiceField(label='问题', required=True, choices=question_choices, widget=forms.RadioSelect)
        self.fields['question_id'] = question_id
