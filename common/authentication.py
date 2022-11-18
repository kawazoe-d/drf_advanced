import jwt, datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from config import settings
from core.models import User

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """Cookieを受け取り認証し、ユーザーを返す"""
        token = request.COOKIES.get('jwt')

        if not token:
            return None
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            # 有効期限切れ
            raise exceptions.AuthenticationFailed('unauthenticated')

        user = User.objects.get(pk=payload['user_id'])

        if user is None:
            raise exceptions.AuthenticationFailed('user not found!')

        return (user, None)


    @staticmethod
    def generate_jwt(id):
        """
        payloadを使用してjwtトークンを発行
        “exp” (Expiration Time) JWTが失効する日時
        “iat” (Issued At) JWTが発行された日時
        """
        payload = {
            'user_id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')