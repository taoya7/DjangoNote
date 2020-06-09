from rest_framework import serializers

from django.conf import settings
from rest_framework import exceptions

from .models import *

class PersonSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=10,
        min_length=6,
        error_messages={
            'max_length': '太长了',
            'min_length': '太少了'
        }
    )
    age = serializers.IntegerField(required=True) # 不是必须填写的

    # 自定义序列化
    gender = serializers.SerializerMethodField()
    def get_gender(self, obj): # obj 每个序列化对象
        return obj.get_sex_display()
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        return settings.MEDIA_URL+str(obj.icon)

    # 局部钩子 validate_要校验的字段名
    # 校验规则  通过返回原值， 失败抛出异常
    def validate_age(self, value):
        if  value<0 or value>100:
            raise exceptions.ValidationError('年龄不符合要求')
        return value
    def validate_name(self, name):
        obj = Person.objects.filter(name=name).first()
        if obj:
            raise exceptions.ValidationError('用户已存在')
        return name

    # 全局钩子 系统与局部钩子校验通过的所有数据
    def validate(self, attrs):
        return attrs

    # 重写新增方法
    def create(self, validated_data):
        # 在所有校验规则完毕之后，数据可以直接入库
        obj = Person.objects.create(**validated_data)
        return obj