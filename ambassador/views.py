from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .serializer import ProductSerializer
from core.models import Product
from django.core.cache import cache
import time

class ProductFrontendAPI(APIView):

    @method_decorator(cache_page(60 * 60 * 2, key_prefix='products_frontend'))
    def get(self, _):
        time.sleep(2)
        products = Product.objects.all()
        serializser = ProductSerializer(products, many=True)
        return Response(serializser.data)

class ProductBackendAPIView(APIView):

    def get(self, request):
        products = cache.get('products_backend')
        if not products:
            time.sleep(2)
            products = list(Product.objects.all())
            cache.set('products_backend', products, timeout=60 * 30) # 30 min

        # 引数はクエリパラメータのkeyとdefault
        s = request.query_params.get('s', '')
        if s:
            products = list([
                # リスト内包表記 [式 for 任意の変数名 in イテラブルオブジェクト]
                # リスト内包表記とif文の組合せ
                # some_var = [expression for item in iterable_obj if condition]
                # 「if condition」に記述した条件（condition）が真になるかどうかをテストして、
                # その結果が真の場合にのみ、「expression」が評価されて、その結果が新たなリストの要素となる

                # この場合、クエリパラメータを小文字に変換したものと
                # productsのtitile、descriptionを小文字に変換したものを比較し
                # マッチしたものをproductsに戻している
                p for p in products
                if (s.lower() in p.title.lower()) or (s.lower() in p.description.lower())
            ])

        # 引数はクエリパラメータのkeyとdefault
        sort = request.query_params.get('sort', None)
        if sort == 'asc':
            # リスト型のメソッドsort(): 元のリストをソート
            # 引数keyにラムダ式(無名関数)を用いてソートしたい要素を指定する
            # lambda p の p は products.sort の products の各要素を表す
            # この場合は、productsの各要素のpriseでsortするよう指示している
            products.sort(key=lambda p: p.price)
        elif sort == 'desc':
            products.sort(key=lambda p: p.price, reverse=True)

        serializser = ProductSerializer(products, many=True)
        return Response(serializser.data)