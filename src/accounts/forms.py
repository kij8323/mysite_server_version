#coding=utf-8
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from captcha.fields import CaptchaField
from .models import MyUser

#注册表
class RegisterForm(forms.Form):
    username = forms.CharField(label='用户名')
    email = forms.EmailField(label='邮箱地址')
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='密码确认', widget=forms.PasswordInput)
    captcha = CaptchaField(label='请输入下方验证码',)
    #验证用户名有效性
    def clean_username(self):
        username = self.cleaned_data.get("username")
        #验证用户名是否已经被注册
        try:
            exists = MyUser.objects.get(username=username)
            raise forms.ValidationError("该用户名已被注册")
        except MyUser.DoesNotExist:
            return username
        #验证用户名是否正常
        except:
            print "raise"
            raise 
            #forms.ValidationError("There was an error, please try again or contact us111.")



    #验证邮件有效性
    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     try:
    #         #验证邮件是否已经被注册过
    #         exists = MyUser.objects.get(email=email)
    #         raise forms.ValidationError("This username is taken")
    #     except MyUser.DoesNotExist:
    #         return email
    #     except:
    #         #验证邮件是否正常
    #         raise forms.ValidationError("There was an error, please try again or contact us.")

    #验证密码有效性
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        #验证密码长度是否大于4
        if len(password1) <= 4:
            raise forms.ValidationError("密码太短，应超过4位！")
        #验证两次输入的密码是否相同
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次输入密码不相同，请核对!")
        return password2


#在admin中增加用户
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'username', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

#在admin中更改用户信息
class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'username', 'first_name', 'last_name', 'is_active', 'is_admin', "is_member")

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

#登录表
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget=forms.PasswordInput)

    # username = forms.CharField(label='',
    #     widget=forms.TextInput(attrs={"placeholder": "用户名"}))
    # password = forms.CharField(label='', 
    #     widget=forms.PasswordInput(attrs={"placeholder": "密码"}))
