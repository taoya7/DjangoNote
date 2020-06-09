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

from .utils.response import APIResponse

class BookView(APIView):
    def get(self, request):
        books = Book.objects.all()
        book_data = BookSerializer(books, many=True).data
        return APIResponse(data_status=0, results=book_data)


class BookDetailView(APIView):
    def get(self, request):
        books = Book.objects.all()
        book_data = BookDetailSerializer(books, many=True).data
        return Response({
            'status' : 0,
            'msg': '请求成功',
            'result': book_data
        })
    def post(self):

        pass


class V2BookView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        if pk:
            try:
                book_query = Book.objects.get(pk=pk, is_delete=False)
                book_res = V2BookSerializer(book_query).data
            except:
                return Response({
                    'status': 1,
                    'msg': '书籍不存在'
                })
        else:
            book_query = Book.objects.filter(is_delete=False).all()
            book_res = V2BookSerializer(book_query,many=True).data

        return APIResponse(results=book_res, http_status=201)

    # 单增
    # 群增
    '''
        测试
{
	"name": "1西游记1",
	"price": "6.66",
	"publish": 2,
	"authors": [1],
}
    '''
    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, dict):
            many = False
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                'status':1,
                'msg': '传递的数据有误'
            })

        book_ser = V2BookSerializer(data=request_data, many=many)
        book_ser.is_valid(raise_exception=True) # 校验操作
        book_res = book_ser.save() # 保存操作
        return Response({
            'status': 0,
            'msg': '保存成功',
            'result': V2BookSerializer(book_res, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        print('dele')
        pk = kwargs.get('pk')
        if pk:
            pks = [pk]
        else:
            pks = request.data.get('pks')

        if Book.objects.filter(pk__in=pks, is_delete=False).update(is_delete=True):
            return Response({
                'status': 0,
                'msg': '删除成功'
            })
        return Response({
            'status': 1,
            'msg': '删除失败'
        })

