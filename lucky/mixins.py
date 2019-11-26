"""
A mixin which provides some helper classes for User app
"""

from django.core.serializers import serialize
import json
from lucky import models
#from base.utils import user_membership_level
from rest_framework_jwt.utils import jwt_payload_handler
import jwt
from lucky_day import settings
#from rest_framework_expiring_authtoken.models import ExpiringToken



class UserSerializer(object):
    """
    This class provide helper methods for user related serializers.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = self.context['request']
        self.user = None

    def get_data(self):
        """
        Serialize user and its related objects.
        A serializer must provide self.user to consume this method
        """
        user = serialize('json', [self.user])
        user = json.loads(user)[0]['fields']
        user.pop('password')
        user.pop('is_superuser')
        user.pop('is_admin')
        user.pop('is_staff')
        user.pop('is_active')
        user.pop('last_login')
        
        payload = jwt_payload_handler(self.user)
        token = jwt.encode(payload, settings.SECRET_KEY)

        user['token'] = token #self.user.auth_token.key
        user['id_user'] = self.user.id

        #profile_master = models.SignUp.objects.get(id=self.user)
        user['first_name'] = self.user.first_name
        user['last_name'] = self.user.last_name
        
        return user
