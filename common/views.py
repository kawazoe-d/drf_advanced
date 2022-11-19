from django.shortcuts import render
from rest_framework import exceptions, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
# returnで返すResponseオブジェクト
from rest_framework.response import Response

from .serializers import UserSerializer
from .authentication import JWTAuthentication
from core.models import User

class RegisterAPIView(APIView):
    """
    ユーザーモデルの登録APIクラス
    request
    {
        "first_name": "test",
        "last_name": "test",
        "email": "test@t.com",
        "password": "test",
        "password_confirm": "test"
    }
    response
    {
        "id": 1,
        "first_name": "test",
        "last_name": "test",
        "email": "test@t.com",
        "is_ambassador": true
    }
    """
    def post(self, request):
        """ユーザーモデルの登録APIに対応するハンドラメソッド"""

        # 辞書形式で格納されたjsonデータをdataに代入
        data = request.data

        if data['password'] != data['password_confirm']:
            """
            APIException
            500 Internal Server Error
            「サーバエラーが発生しました」というレスポンスデータを返す
            """
            raise exceptions.APIException('Passwords do not match!')
        data['is_ambassedor'] = 0
        
        # 引数dataにリクエストdataを渡してシリアライザをインスタンス化
        serializer = UserSerializer(data=data)
        # バリデーションを実行
        # is_validを実行しないとsaveメソッドは呼び出せない
        # raise_exception=True を与えることで erorrs 情報をラップした ValidationError を投げてくれる
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを登録
        # data (出力専用)属性を参照した後には save() はコールできない
        # どうしても参照する必要があるなら、 validated_dataを使う
        serializer.save()
        # シリアライザオブジェクトのdata属性にdictで格納されたデータをJSON文字列にシリアライズ
        return Response(serializer.data, status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    """
    ログイン認証APIクラス
    request
    {
        "email": "test@t.com",
        "password": "test"
    }
    response
    {
        "message": "success"
    }
    """
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        # filterの引数にモデルクラスのフィールド名と任意の値を指定することで条件検索
        # emailはユニークなので、firstで最初にマッチしたものだけ返す
        user = User.objects.filter(email=email).first()

        if user is None:
            """
            AuthenticationFailed
            401 Unauthorized
            「認証情報が正しくありません」というレスポンスデータを返す
            """
            raise exceptions.AuthenticationFailed('User not found!')
        
        # check_password() ユーザーが入力したパスワードの正しさを検証する関数
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect Password!')

        token = JWTAuthentication.generate_jwt(user.id)

        response = Response()
        # jwtトークンをCookieにセット。httponly=Trueでhttp通信でのみ参照可となる
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'message': 'success'
        }

        return response

class UserAPIView(APIView):
    """
    ログインユーザーAPIクラス
    request
    Cookie
    response
    {
        "id": 1,
        "first_name": "test",
        "last_name": "test",
        "email": "test@t.com",
        "is_ambassador": true
    }
    """
    # 指定したAuthenticationクラスを使って認証を行う
    authentication_classes = [JWTAuthentication]
    # 認証済みでないとerrorを返す
    # "detail": "You do not have permission to perform this action."
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

class LogoutAPIView(APIView):
    """
    ログアウトAPIクラス
    request
    Cookie
    response
    {
        "message": "success"
    }
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    # request引数は使用しないことを明示
    def post(self, _):
        response = Response()
        response.delete_cookie(key='jwt')
        response.data = {
            'message': 'success'
        }
        return response

class ProfileInfoAPIView(APIView):
    """
    ユーザー情報更新APIクラス
    request
    {
        "first_name": "new",
        "last_name": "new",
        "email": "new@new.com"
    }
    response
    {
        "id": 1,
        "first_name": "new",
        "last_name": "new",
        "email": "new@new.com",
        "is_ambassador": true
    }
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        # partial 引数がTrueの場合、第二引数(data)ですべての値を指定しなくても、第一引数のオブジェクトから補完される
        # 引数dataで渡した値のみが更新される
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class ProfilePasswordAPIView(APIView):
    """
    パスワード更新APIクラス
    request
    {
        "password": "new",
        "password_confirm": "new"
    } 
    response
    {
        "id": 1,
        "first_name": "new",
        "last_name": "new",
        "email": "new@new.com",
        "is_ambassador": true
    }
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')
        
        user.set_password(data['password'])
        user.save()

        return Response(UserSerializer(user).data)