from django.shortcuts import render


# 序列化组件
from rest_framework.serializers import Serializer
from rest_framework.serializers import BaseSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ListSerializer


# 其他
from rest_framework.views import  APIView
from rest_framework.response import  Response

from .models import *
from .serializers import *

class PersonView(APIView):

    def get(self, request, *args, **kwargs):
        pers = Person.objects.all()
        res = PersonSerializer(pers, many=True)
        return Response({
            'status':0,
            'msg':'请求成功',
            'result':res.data
        })
    def post(self, request):
        request_data = request.data

        if not isinstance(request_data, dict) or request_data=={}:
            return Response({
                'status': 1,
                'msg': '数据有误'
            })

        per_ser = PersonSerializer(data=request_data)

        # 序列化对象调用is_valid 完成校验。 如果失败了会保存在序列化对象errors
        if per_ser.is_valid():
            # 校验通过 - 新增
            per_pbj = per_ser.save()
            return Response({
                'status': 0,
                'msg': '保存成功',
                'result': PersonSerializer(per_pbj).data
            })
        else:
            return Response({
                'status': 1,
                'msg': per_ser.errors
            })


