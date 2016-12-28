from django import forms
from django.contrib.auth.models import User
from .models import UInfo


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        labels = {
            'username': '用户名',
            'email': '邮箱',
            'password': '密码',
        }

class UInfoForm(forms.ModelForm):
    pass
    class Meta:
        model = UInfo
        exclude=('user', )
        labels = {
            'qq': 'QQ',
            'phone': '手机号',
            'avatar': '头像',
        }

