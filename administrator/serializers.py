from rest_framework import serializers

from core.models import Product, Link

# ModelSerializerを継承することでモデルのフィールド定義を再利用可
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # 対象のモデルクラスを指定
        model = Product
        # 利用するモデルのフィールドを指定。全てのフィールドを使用する場合は「__all__」で指定可
        fields = '__all__'

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'