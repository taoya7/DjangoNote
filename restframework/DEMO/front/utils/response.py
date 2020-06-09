from rest_framework.response import Response


class APIResponse(Response):
    def __init__(self, data_status=0, data_msg='ok', results=None,
                 http_status=None,
                 headers=None,
                 content_type=None,
                 **kwargs
     ):
        data = {
           'status': data_status,
            'msg': data_msg
        }

        if results is not None:
            data['results'] = results

        # 其他内容
        if kwargs is not None:
            for k,v in kwargs.items():
                setattr(data, k, v)
        # Or data.update(kwargs)

        super().__init__(data=data, status=http_status,
                 template_name=None, headers=headers,
                 exception=False, content_type=content_type)
