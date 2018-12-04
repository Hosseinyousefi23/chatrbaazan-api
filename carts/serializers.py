from rest_framework import serializers

from carts.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = '__all__'

    def get_item(self, obj):
        return CartItemSerializer(CartItem.objects.filter(cart__id=obj.pk), many=True).data
