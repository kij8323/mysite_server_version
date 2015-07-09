#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from .models import Comment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# class CommentForm(forms.ModelForm):
# 	class Meta:
# 		model = Comment
# 		fields = ('user', 'path', 'text')

class CommentForm(forms.Form):
	comment = forms.CharField(
		widget=forms.Textarea(attrs={"placeholder": "你的回复或评论:"})
	)
	def __init__(self, data=None, files=None, **kwargs):
		super(CommentForm, self).__init__(data, files, kwargs)
		self.helper = FormHelper()
		self.helper.form_show_labels = False
		self.helper.add_input(Submit('submit', '添加回复', css_class='btn btn-primary',))