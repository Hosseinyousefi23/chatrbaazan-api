from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
import uuid

from carts.models import CartItem, Cart
from carts.serializers import CartSerializer
from shop.models import Product
from shop.renderers import CustomJSONRenderer


# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
#
#
# def get_uuid(c=20):
#     return uuid.uuid4().hex[:c].upper()


class AddCart(mixins.CreateModelMixin,
              generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def post(self, request, format=None, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        if 'product' not in body_data:
            pId = 0
        else:
            pId = body_data['product']
        # check exists Product
        product = Product.objects.filter(id=pId)
        if not product.exists():
            return CustomJSONRenderer().render400()
        product = product.first()
        if product.is_free or product.price == 0:
            return Response({'message': 'Product Is Free, can not add to cart'}, status=400)
        mutable = request.POST._mutable
        request.POST._mutable = True
        # if request.user:
        #     request.data.update('user', 1)
        # else:
        #     request.data.update('user', None)
        print('user', str(request.user))
        request.data.update(user=request.user.pk)
        request.data.update(price=product.price)
        request.data.update(total_price=product.price)
        request.POST._mutable = mutable
        cart = self.create(request, *args, **kwargs)
        try:
            CartItem.objects.create(
                product=product,
                price=product.price,
                total_price=product.price,
                cart=Cart.objects.get(pk=cart.data['id']),
                count=1
            )
        except Exception as e:
            Cart.objects.filter(id=cart.data['id']).delete()
            print('error when create item', str(e))
            return Response({'message': 'Problem When Add product To Cart Try Again.'})
        # Create Item Product
        cart = Cart.objects.get(pk=cart.data['id'])
        return CustomJSONRenderer().render(
            {
                'count': cart.count(),
                'result': CartSerializer(cart, many=True).data
            }, status=201
        )

    def get(self, request, format=None, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user)
        return CustomJSONRenderer().render(
            {
                'count': cart.count(),
                'result': CartSerializer(cart, many=True).data
            }
        )
