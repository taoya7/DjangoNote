from rest_framework import serializers

from django.conf import settings
from rest_framework import exceptions


from .models import *

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(read_only=True, many=True)
    class Meta:
        model = Book
        fields = ('name', 'price', 'publish_name', 'author_list', 'authors')

class BookDetailSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        return attrs
    class Meta:
        model = Book
        fields = ('name', 'price', 'publish', 'authors')

'''
    序列化与反序列化整合
    1. fields: 设置所有序列化与反序列化字段
    2. extra_kwargs划分只序列化或反序列化字段
        - write_only
        - read_only
    3. 设置反序列化所需的 系统、局部钩子、全局钩子
'''
class V2BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'price', 'img', 'author_list', 'publish_name', 'publish', 'authors')
        extra_kwargs = {
            'publish': {# 只参与反序列化， 不参与序列化
                'write_only': True
            },
            'authors': {
                'write_only': True
            },
            'img': { # 只参与序列化，不参与反序列化
                'read_only': True
            },
            # 所有自定义的字段都为read_only
        }

    def validate_name(self, value):
        if value.startswith('西'):
            raise exceptions.ValidationError('不能以西开头的书籍哦！')
        return value

    def validate(self, attrs):
        print(attrs)
        publish = attrs.get('publish')
        name = attrs.get('name')
        if Book.objects.filter(name=name, publish=publish):
            raise  exceptions.ValidationError({'book': '该书存在了都。'})
        return attrs
