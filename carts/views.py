from django.http.request import QueryDict
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
        # body_unicode = request.body.decode('utf-8')
        # body_data = json.loads(body_unicode)
        pId = request.POST.get('product', 0)
        # check exists Product
        product = Product.objects.filter(id=pId)
        if not product.exists():
            return CustomJSONRenderer().render404('product', '')
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
        cart = Cart.objects.filter(user=request.user).filter(status=1)
        if cart.count() == 0:
            cart = self.create(request, *args, **kwargs)
        else:
            cart = CartSerializer(cart.first(), many=False, context={'request': request})

        print(str(cart.data['id']))
        try:
            cItem = CartItem.objects.filter(cart__id=cart.data['id'])

            if cItem.filter(product__id=product.id).count() > 0:
                cItem = cItem.first()
                cItem.count = cItem.count + 1
                cItem.total_price = cItem.total_price + cItem.product.price
                cItem.save()
            else:
                cartCreate = CartItem.objects.create(
                    product=product,
                    price=product.price,
                    total_price=product.price,
                    cart=Cart.objects.get(pk=int(cart.data['id'])),
                    count=1
                )
        except Exception as e:
            raise e
            # Cart.objects.filter(id=cart.data['id']).delete()
            print('error when create item', str(e))
            return Response({'message': 'Problem When Add product To Cart Try Again.'})
        # Create Item Product
        # cart = Cart.objects.get(pk=cart.data['id'])
        CartItem().update_price(Cart.objects.get(pk=int(cart.data['id'])).id)

        cart = Cart.objects.filter(user=request.user)
        
        return CustomJSONRenderer().render(
            {
                'count': cart.count(),
                'result': CartSerializer(cart, many=True, context={'request': request}).data
            }, status=201
        )

    def get(self, request, format=None, *args, **kwargs):
        cart = Cart.objects.filter(user=request.user)
        return CustomJSONRenderer().render(
            {
                'count': cart.count(),
                'result': CartSerializer(cart, many=True, context={'request': request}).data
            }
        )

    def delete(self, request, format=None, *args, **kwargs):
        # pId = 0
        # if 'product' not in request.POST:
        #     body_unicode = request.body.decode('utf-8')
        #     body_data = json.loads(body_unicode)
        #     if 'product' in body_data:
        #         pId = body_data['product']
        # else:
        cId = request.POST.get('cart', 0)
        cartItem = CartItem.objects.filter(id=cId)
        if not cartItem.exists():
            return CustomJSONRenderer().render404('cart', '')
        else:
            try:
                idCart = cartItem.first().cart.id
                cartItem.first().delete()
                CartItem().update_price(idCart)

            except Exception as e:
                return CustomJSONRenderer().render500(str(e), '')
            cart = Cart.objects.filter(user=request.user)
            return CustomJSONRenderer().render(
                {
                    'count': cart.count(),
                    'result': CartSerializer(cart, many=True, context={'request': request}).data
                }, status=200
            )

    def put(self, request, format=None, *args, **kwags):
        itemId = request.POST.get('itemId', 0)
        itemCount = request.POST.get('itemCount',1)
        
        itemFound = CartItem.objects.filter(id=itemId)
        if not itemFound:
            return CustomJSONRenderer().render404('Cart Item',None)

        itemFoundFirst = itemFound.first()
        itemFoundFirst.count = itemCount
        if itemFoundFirst.save():
            CartItem().update_price(itemFoundFirst.cart.id)
            cart = Cart.objects.filter(user=request.user)
            return CustomJSONRenderer().render(
                {
                    'count': cart.count(),
                    'result': CartSerializer(cart, many=True, context={'request': request}).data
                }
            )
        else:
            return CustomJSONRenderer().render({'success':False},status=500)
        

