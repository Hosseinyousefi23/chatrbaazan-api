from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import uuid

from carts.models import CartSession, CartItem, Cart
from carts.serializers import CartSerializer
from shop.models import Product
from shop.renderers import CustomJSONRenderer


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_uuid(c=20):
    return uuid.uuid4().hex[:c].upper()


class AddCart(mixins.CreateModelMixin,
              generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CartSerializer

    def post(self, request, format=None, *args, **kwargs):
        # check exists Product
        product = Product.objects.filter(id=request.POST.get('product'))
        if not product.exists():
            return CustomJSONRenderer().render400()
        product = product.first()
        if product.is_free() and product.price == 0:
            return Response({'message': 'Product Is Free, can not add to cart'}, status=400)
        mutable = request.POST._mutable
        request.POST._mutable = True
        if request.user:
            request.data.update('user', 1)
        else:
            request.data.update('user', None)

        uuid = get_uuid()
        cartOld = CartSession.objects.filter(key=uuid).filter(ip=get_client_ip(request))
        # TODO check time Expire Cart And check User
        if cartOld.exists():
            return Response()  # TODO return Carts And Item Cart
        else:
            session = CartSession.objects.create(
                ip=get_client_ip(request),
                key=uuid.uuid4().hex[:20].upper(),
                header=request.META
            )
        request.data.update('session', session.id)
        request.data.update('price', product.price)
        request.data.update('total_price', product.price)
        cart = self.create(request, *args, **kwargs)
        try:
            CartItem.objects.create(
                product=product.id,
                price=product.price,
                total_price=product.price,
                cart=cart.data.id,
                count=1
            )
        except Exception as e:
            Cart.objects.filter(id=cart.data.id).delete()
            return Response({'message': 'Problem When Add product To Cart Try Again.'})

        request.POST._mutable = mutable
        # Create Item Product
        return Response({'data': 'data'}, status=201)
