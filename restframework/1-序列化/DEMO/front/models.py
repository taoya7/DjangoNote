from django.db import models

# Create your models here.

class Pets(models.Model):
    name = models.CharField(max_length=50)

class Person(models.Model):
    SEX_CHOICE = (
        (0, '男'),
        (1, '女')
    )

    name = models.CharField(max_length=200)
    age = models.IntegerField()
    sex = models.IntegerField(choices=SEX_CHOICE, default=0)
    icon = models.ImageField(upload_to='avatar', default='avatar/default.png')

    class Meta:
        db_table = 'person'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name