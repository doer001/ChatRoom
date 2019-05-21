from django.db import models


class User(models.Model):
    gender_choices = (
        ('男', '男'),
        ('女', '女'),
    )
    username = models.CharField(verbose_name='用户名', max_length=8, unique=True)  # 用户名唯一
    email = models.EmailField(verbose_name='邮箱', unique=True)  # 邮箱唯一
    gender = models.CharField(verbose_name='性别', max_length=8, choices=gender_choices, default='男')
    password = models.CharField(verbose_name='密码', max_length=256)
    reg_time = models.DateTimeField(verbose_name='注册时间', auto_now_add=True)
    friends = models.ManyToManyField('self', verbose_name='好友们')

    def __str__(self):  # 帮助人性化显示对象信息；
        return self.username

    class Meta:
        ordering = ['-reg_time']
        verbose_name = verbose_name_plural = "用户名"  # 数据表别名


class UserInformation(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name='用户')
    name = models.CharField(verbose_name='姓名', max_length=4)
    birthday = models.DateField(verbose_name='生日')
    tel = models.CharField(verbose_name='电话', max_length=15)
    hometown = models.CharField(verbose_name='故乡', max_length=100)
    address = models.CharField(verbose_name='所在地', max_length=100)
    university = models.CharField(verbose_name='大学', max_length=50)
    company = models.CharField(verbose_name='公司', max_length=50)
    profession = models.CharField(verbose_name='职业', max_length=20)



