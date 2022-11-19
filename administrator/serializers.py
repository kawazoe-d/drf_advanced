from rest_framework import serializers

from core.models import Product, Link, Order, OrderItem

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

class OrderItremSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItremSerializer(many=True)
    # SerializerMethodField()を使うことにより、メソッドの結果によってフィールドの値を決めることが可能
    # 適用されるメソッド名はget_ + フィールド名
    # 適用されるメソッド名をSerializerMethodField()のmethod_nameという引数で指定することも可能
    total = serializers.SerializerMethodField('get_total')

    def get_total(self, obj):
        items = OrderItem.objects.filter(order_id=obj.id)
        # for文を一行で書くときの構文
        # x for {変数} in {イテラブル}
        return sum((o.price * o.quantity) for o in items)

    class Meta:
        model = Order
        fields = '__all__'