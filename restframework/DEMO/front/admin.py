from django.contrib import admin


from .models import *

# 注册
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(AuthorDetail)
admin.site.register(Publish)