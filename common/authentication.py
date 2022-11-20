import jwt, datetime
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from config import settings
from core.models import User

class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
        Cookieを受け取り認証し、ユーザーを返す
        ambassadorエンドポイントでログインした場合、scopeにambassadorを入れる
        adminエンドポイントでログインした場合、scopeにadminを入れる
        エンドポイントとscopeに差異がある場合、エラーを返す
        """

        is_ambassador = 'api/ambassador' in request.path

        token = request.COOKIES.get('jwt')

        if not token:
            return None
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            # 有効期限切れ
            raise exceptions.AuthenticationFailed('unauthenticated')

        """
        is_ambassadorである かつ scopeがambassadorでない または
        is_ambassadorでない(adminである) かつ scopeがadminでない
        """
        if ((is_ambassador and payload['scope'] != 'ambassador') or
        (not is_ambassador and payload['scope'] != 'admin')):
            raise exceptions.AuthenticationFailed('Invalid Scope!')

        user = User.objects.get(pk=payload['user_id'])

        if user is None:
            raise exceptions.AuthenticationFailed('user not found!')

        return (user, None)


    @staticmethod
    def generate_jwt(id, scope):
        """
        payloadを使用してjwtトークンを発行
        “exp” (Expiration Time) JWTが失効する日時
        “iat” (Issued At) JWTが発行された日時
        """
        payload = {
            'user_id': id,
            'scope': scope,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }

        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')