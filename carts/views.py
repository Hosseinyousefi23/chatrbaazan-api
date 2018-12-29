from datetime import datetime, timedelta, time

from django.db.models.expressions import F
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
from chatrbaazan import settings
from shop.models import Product, UserProduct
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
        cart = Cart.objects.filter(user=request.user).filter(status=1).filter(
            updated_at__gte=datetime.now() - timedelta(hours=24))
        print(str(cart.query))
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
        itemCount = request.POST.get('itemCount', 1)

        itemFound = CartItem.objects.filter(id=itemId)
        if not itemFound:
            return CustomJSONRenderer().render404('Cart Item', None)

        itemFoundFirst = itemFound.first()
        itemFoundFirst.count = itemCount
        try:
            itemFoundFirst.save()
            CartItem().update_price(itemFoundFirst.cart.id)
            cart = Cart.objects.filter(user=request.user)
            return CustomJSONRenderer().render(
                {
                    'count': cart.count(),
                    'result': CartSerializer(cart, many=True, context={'request': request}).data
                }
            )
        except Exception as e:
            return CustomJSONRenderer().render({'success': False, 'e': str(e)}, status=500)


class CompleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id=None, format=None, *args, **kwargs):
        if id is None:
            cart = Cart.objects.filter(user=request.user).filter(status=1).filter(
                updated_at__gte=datetime.now() - timedelta(hours=24))

        else:
            cart = Cart.objects.filter(pk=id).filter(user=request.user).filter(
                updated_at__gte=datetime.now() - timedelta(hours=24)).filter(
                status=1)
        # check not empty cart
        if cart.count() == 0:
            return CustomJSONRenderer().render({
                'message': 'cart is empty',
                'success': False
            }, status=400)

        cart = cart.first()
        if cart.total_price == 0:
            # Product is free ~ BUG :)
            return CustomJSONRenderer().render({'message': 'Problem The System Cart', 'success': False}, status=400)

        if settings.CART_DEBUG:
            # Debug enable for cart
            """""
            :: save product into user product
            :: change status cart in 3
            :: mince count product
            :: check count product
            """""
            cartItems_date = CartItem.objects.filter(cart__id=cart.pk)
            for cartItem in cartItems_date:
                product = Product.objects.filter(id=cartItem.product.id)
                if product.first().count == 0:
                    # deleted item product from cart item
                    CartItem.objects.filter(id=cartItem.id).delete()
                    return CustomJSONRenderer().render({
                        'message': 'Product {} Not Exists'.format(cartItem.product),
                        'success': False,
                        'reload': True
                    }, status=400)
            for cartItem in cartItems_date:
                UserProduct.objects.create(
                    user=request.user,
                    product=cartItem.product
                )
                product = Product.objects.filter(id=cartItem.product.id).update(count=F('count') - 1)
            Cart.objects.filter(pk=cart.pk).update(status=3)
            return CustomJSONRenderer().render({
                'redirect_uri': settings.URI_FRONT + 'cart/factor/{}/'.format(cart.pk),
                'success': True,
            })
        else:
            pass


class FactorView(APIView):
    permission_classes = (IsAuthenticated,)
    allowed_method = ('GET',)

    def get(self, request, id=None, format=None, *args, **kwargs):
        print('str id cart in uri factor', str(id))
        if id is None:
            return CustomJSONRenderer().render404('cart', '')
        try:
            cart = Cart.objects.filter(user=request.user).filter(status=3).get(id=id)
        except Exception as e:
            print('str e in factor ', str(e))
            return CustomJSONRenderer().render404('cart', '')

        if cart.status == 3:
            return CustomJSONRenderer().renderData(CartSerializer(cart, many=False, context={'request': request}).data)
        else:
            return CustomJSONRenderer().render({
                'message': u'محصول هم چنان در وضعیت معلق قرار دارد.',
            }, status=403)
