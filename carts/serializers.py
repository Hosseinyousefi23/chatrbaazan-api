from rest_framework import serializers

from carts.models import Cart, CartItem
from shop.models import Product
from shop.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'price', 'total_price', 'count')

    def get_product(self, obj):
        return ProductSerializer(Product.objects.get(id=obj.product.id), many=False,
                                 context={'request': self.context['request']}).data


class CartSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_item(self, obj):
        return CartItemSerializer(CartItem.objects.filter(cart__id=obj.pk), many=True,
                                  context={'request': self.context['request']}).data
