from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Commodity(models.Model):
    # 商品信息
    name = models.CharField(max_length = 50)
    introduction = models.TextField()
    image = models.ImageField(upload_to="uploads/commodity")
    available = models.BooleanField(default = True)
    date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    tags = models.ManyToManyField(
        "Tag",
        db_table = "commodity_tag"
    )

    def __str__(self):
        return self.name


class Category(models.Model):
    # 商品分类，一对一
    name = models.CharField(max_length = 50, unique = True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    # 商品标签，多对多
    name = models.CharField(max_length = 50, unique = True)
    def __str__(self):
        return self.name

class UInfo(models.Model):
    # 用户信息
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.BigIntegerField(null=True, blank=True)
    qq = models.BigIntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='uploads/avatar', null=True, blank=True)

