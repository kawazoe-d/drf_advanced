from rest_framework import generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerializer, LinkSerializer, OrderSerializer
from common.serializers import UserSerializer
from common.authentication import JWTAuthentication
from core.models import User, Product, Link, Order
from django.core.cache import cache

class AmbassadorAPIView(APIView):
    """
    アンバサダー取得APIクラス
    response
    [
        {
            "id": 1,
            "first_name": "admin",
            "last_name": "admin",
            "email": "admin@a.com",
            "is_ambassador": true
        },
        {
            "id": 2,
            "first_name": "test",
            "last_name": "test",
            "email": "test@test.com",
            "is_ambassador": true
        }
    ]
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, _):
        ambassadors = User.objects.filter(is_ambassador=True)
        # リスト形式のjsonを出力する場合は、キーワード引数にmany=Trueを指定する
        serializer = UserSerializer(ambassadors, many=True)
        return Response(serializer.data)

# Generic = 汎用
# RetrieveModelMixin 単体取得Mixin
# ListModelMixin 一覧取得Mixin
class ProductGenericAPIView(
    generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.ListModelMixin, 
    mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # querysetは、モデルから取り出した一連の情報。Djangoが作っているQueryset型のデータ
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk=None):
        # pkがある場合、単体で取得
        if pk:
            return self.retrieve(request, pk)

        # pkがない場合、一覧で取得
        return self.list(request)

    def post(self, request):
        # create:リソースの作成
        response = self.create(request)
        for key in cache.keys('*'):
            if 'products_frontend' in key:
                cache.delete(key)
        cache.delete('products_backend')
        return response
    
    def put(self, request, pk=None):
        # partial_update:リソースの更新（一部）
        response = self.partial_update(request, pk)
        for key in cache.keys('*'):
            if 'products_frontend' in key:
                cache.delete(key)
        cache.delete('products_backend')
        return response
    
    def delete(self, request, pk=None):
        # destroy:リソースの削除
        response = self.destroy(request, pk)
        for key in cache.keys('*'):
            if 'products_frontend' in key:
                cache.delete(key)
        cache.delete('products_backend')
        return response

class LinkAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        links = Link.objects.filter(user_id=pk)
        serilaizer = LinkSerializer(links, many=True)
        return Response(serilaizer.data)

class OrderAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(complete=True)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)