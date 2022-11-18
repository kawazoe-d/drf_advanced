from django.shortcuts import render
from rest_framework import exceptions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import UserSerializer

class RegisterAPIView(APIView):
    """ユーザーモデルの登録APIクラス"""
    def post(self, request):
        """ユーザーモデルの登録APIに対応するハンドラメソッド"""

        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException('Passwords do not match!')
        data['is_ambassedor'] = 0
        
        # シリアライザオブジェクトを作成
        serializer = UserSerializer(data=data)
        # バリデーションを実行
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを登録
        serializer.save()
        # レスポンスオブジェクトを作成して返す
        return Response(serializer.data, status.HTTP_201_CREATED)