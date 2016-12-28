from django import forms
from django.contrib.auth.models import User
from django.forms import modelform_factory
from .models import UInfo, Commodity

UserForm = modelform_factory(
    model = User,
    fields = ('username', 'email', 'password'),
    labels = {
        'username': '用户名',
        'email': '邮箱',
        'password': '密码',
    }
)

UInfoForm = modelform_factory(
    model = UInfo,
    exclude=('user', ),
    labels = {
        'qq': 'QQ',
        'phone': '手机号',
        'avatar': '头像',
    }
)

CommodityForm = modelform_factory(
    model = Commodity,
    exclude=('user', 'date',),
    labels = {
        'name': '物品名',
        'introduction': '简介',
        'image': '照片',
        'available': '有效（勾选表示显示在主页）',
        'price': '价格',
        'category': '分类',
        'tags': '标签'
    },
)

