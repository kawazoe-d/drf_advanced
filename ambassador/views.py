from rest_framework.views import APIView
from rest_framework.response import Response

from .serializer import ProductSerializer
from core.models import Product

class ProductFrontendAPI(APIView):

    def get(self, _):
        products = Product.objects.all()
        serializser = ProductSerializer(products, many=True)
        return Response(serializser.data)

class ProductBackendAPIView(APIView):


    def get(self, _):
        products = Product.objects.all()
        serializser = ProductSerializer(products, many=True)
        return Response(serializser.data)