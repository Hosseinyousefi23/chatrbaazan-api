from django.db.models.expressions import F
# Create your views here.
from rest_framework import mixins, generics
from rest_framework.permissions import AllowAny

from like.serializers import LikeSerializer
from shop.models import Product
from shop.renderers import CustomJSONRenderer


class LikeView(mixins.CreateModelMixin,
               generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LikeSerializer

    def post(self, request, format=None, *args, **kwargs):
        productId = request.POST.get('product', 0)
        if not Product.objects.filter(pk=productId).exists():
            return CustomJSONRenderer().render404('Like', '')
        # if 'like_session' in request.session:
        #     return CustomJSONRenderer().render({
        #         'message': 'You Have Already Like This Post.'
        #     }, status=400)
        # session = str(uuid.uuid1(random.randint(0, 281474976710655)))
        mutable = request.POST._mutable
        request.POST._mutable = True
        # user = None
        # if request.user.is_authenticated:
        #     user = request.user.pk
        request.data.update(user=request.user.pk)
        request.data.update(product=productId)
        request.data.update(like=1)
        # request.data.update(session=request.session)
        request.POST._mutable = mutable
        # if Like.objects.filter(user__id=request.POST.get('user')).filter(
        #         product__id=request.POST.get('product')).exists():
        #     return CustomJSONRenderer().render({
        #         'message': 'Liked Before!'
        #     })
        # like = 1
        # if int(request.POST.get('like')) not in like:
        # return CustomJSONRenderer().render400()
        # request.session['like_session'] = session
        Product.objects.filter(id=productId).update(click=F('click') + 1)
        return self.create(request, *args, **kwargs)
