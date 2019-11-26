from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from django.contrib.auth import get_user_model
from django.conf import settings


def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)

    if response is not None:
        message = []

        for field, value in response.data.items():
            if not isinstance(value, list):
                message.append(value)
            else:
                message.append(value[0])

        response.data = {}
        response.data['message'] = message[0]
        response.data['success'] = False

    return response


class CustomApiException(APIException):

    detail = None

    def __init__(self, detail):
        CustomApiException.detail = detail


