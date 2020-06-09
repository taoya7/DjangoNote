from django.db import models

from django.contrib.auth.models import AbstractUser # 基表

'''
Book表：name、price、img、authors、publish、is_delete、create_time
Publish表：name、address、is_delete、create_time   
Author表：name、age、is_delete、create_time
AuthorDetail表：mobile, author、is_delete、create_time
'''

# ) 基表
# 被加载后，也不会在数据库中创建表

class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta: # 设置 abstract = True 来声明基表，作为基表的Model不能在数据库中形成对应的表
        abstract = True

class Book(BaseModel):
    name = models.CharField(max_length=64, verbose_name='书名')
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='价格')
    img = models.ImageField(upload_to='img', default='img/default.jpg', verbose_name='封面')


    publish = models.ForeignKey(
        to='Publish',
        on_delete=models.DO_NOTHING, # 设置连表操作关系
        related_name='books', # 反向查询
        db_constraint=False #断关联（断开Book表和Publish表的关联,方便删数据,虽然断开了关联但是还能正常使用）
    )
    authors = models.ManyToManyField(
        to='Author',
        related_name='books', # 反向查询字段
        db_constraint=False
    )

    @property
    def publish_name(self):
        return self.publish.name

    @property
    def author_list(self):
        return self.authors.values('name', 'age', 'detail__mobile').all()

    class Meta:
        db_table = 'book'
        verbose_name = '书籍',
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 出版社
class Publish(BaseModel):
    name = models.CharField(max_length=64, verbose_name='名称')
    address = models.CharField(max_length=200, verbose_name='地址')

    class Meta:
        db_table = 'publish'
        verbose_name = '出版社'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 作者表
class Author(BaseModel):
    name = models.CharField(max_length=64)
    age = models.IntegerField()

    class Meta:
        db_table = 'author'
        verbose_name = '作者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class AuthorDetail(BaseModel):
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    author = models.OneToOneField(
        to='Author',
        on_delete=models.CASCADE,
        related_name='detail',
        db_constraint=False
    )

    class Meta:
        db_table = 'author_detail'
        verbose_name = '作者详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author.name
