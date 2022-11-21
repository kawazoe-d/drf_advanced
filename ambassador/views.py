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

    def get(self, _):
        products = cache.ger('products_backend')

        if not products:
            time.sleep(2)
            products = list(Product.objects.all())
            cache.set('products_backend', products, timeout=60 * 30) # 30 min
        serializser = ProductSerializer(products, many=True)
        return Response(serializser.data)