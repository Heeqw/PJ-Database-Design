from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from merchant_app.models import MerchantToken, MerchantLogin


class MerchantTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token_key = auth_header.split(' ')[1]
            token = MerchantToken.objects.get(key=token_key)
        except (IndexError, MerchantToken.DoesNotExist):
            raise AuthenticationFailed('Invalid token')

        user = token.user
        user.is_authenticated = True  # 设置 is_authenticated 属性
        return user, token
