from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html
from django.conf import settings


class MenuInfo(models.Model):
    parent = models.ForeignKey('MenuInfo', blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField('菜单名称', max_length=15)
    menu_icon = models.ForeignKey('IconInfo', verbose_name='图标', on_delete=models.PROTECT)
    url = models.CharField('网址', max_length=100, blank=True, null=True)

    show = models.BooleanField('是否显示', default=False)
    priority = models.IntegerField(verbose_name=u'显示优先级', null=True, blank=True, default=-1)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'MenuInfo'
        ordering = ['priority']
        verbose_name = '菜单'
        verbose_name_plural = '菜单'


class IconInfo(models.Model):
    DisplayName = models.CharField(max_length=100)
    ClassName = models.CharField(max_length=100)
    SourceType = models.CharField(max_length=100)
    CreateTime = models.DateTimeField(auto_created=True)

    def __str__(self):
        return self.DisplayName

    class Meta:
        db_table = 'IconInfo'
        verbose_name = '图标'
        verbose_name_plural = '图标'


class User(AbstractUser):
    phone_number = models.CharField('手机号码',max_length=11)
    photo = models.ImageField('照片',upload_to="icons/%Y/%m/%d", blank=True, null=True,default='icons/user2-160x160.jpg')


    def name(self):
        return self.last_name+self.first_name
    name.short_description = '姓名'

    def show_photo(self):
        return format_html(
            '<img src="{}{}" class="img-circle" alt="User Image" />'.format(settings.MEDIA_URL,self.photo)
        )

    show_photo.short_description = '图片'

    def src(self):
        return '{}{}'.format(settings.MEDIA_URL,self.photo)

    src.short_description = '链接'

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
