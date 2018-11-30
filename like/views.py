from django.shortcuts import render

# Create your views here.
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from like.models import Like
from like.serializers import LikeSerializer
from shop.models import Product
from shop.renderers import CustomJSONRenderer


class LikeView(mixins.CreateModelMixin,
               generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def post(self, request, format=None, *args, **kwargs):
        productId = request.POST.get('product', 0)
        if not Product.objects.filter(pk=productId).exists():
            return CustomJSONRenderer().render400()
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.data.update(user=request.user.pk)
        request.data.update(product=productId)
        request.data.update(like=1)
        request.POST._mutable = mutable
        if Like.objects.filter(user__id=request.POST.get('user')).filter(
                product__id=request.POST.get('product')).exists():
            return CustomJSONRenderer().render400()
        like = {1, 2***REMOVED***
        if int(request.POST.get('like')) not in like:
            return CustomJSONRenderer().render400()

        return self.create(request, *args, **kwargs)
