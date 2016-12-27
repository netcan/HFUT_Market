from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(
        label = '用户名',
        max_length = 150,
    )
    email = forms.EmailField(
        label = '邮箱',
    )
    password = forms.CharField(
        label = '密码',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label = '确认密码',
        widget=forms.PasswordInput
    )
    phone = forms.IntegerField(
        required = False,
        label = '手机号'
    )
    qq = forms.IntegerField(
        required = False,
        label = 'QQ'
    )
    avatar = forms.ImageField(
        required = False,
        label = '头像'
    )


