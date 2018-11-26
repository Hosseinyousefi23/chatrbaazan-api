from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from shop.models import City, Banner
from shop.renderers import CustomJSONRenderer
from shop.serializers import CitySerializer, BannerSerializer


def test(request):
    return render(request, 'index.html')


class TestAPi(APIView):
    permission_classes = (IsAuthenticated,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        return Response("test")


def testr(request):
    return Response('test')


class GetCategory(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        data = [{"id": "db636bfb-cdcb-497e-830e-b441415f5050", "parent": None, "name": "سفارش غذا", "eng_name": "food",
                 "open_chatrbazi": 2, "all_chatrbazi": 12000.0},
                {"id": "324e4bab-5e8e-426a-8c29-25d0be1e8012", "parent": None, "name": "فروشگاه اینترنتی",
                 "eng_name": "onlineShop", "open_chatrbazi": 1, "all_chatrbazi": 85000.0},
                {"id": "c2670bd6-f71f-4bfe-8315-ce022e1ad067", "parent": None, "name": "حمل ونقل",
                 "eng_name": "transport", "open_chatrbazi": 1, "all_chatrbazi": 27700.0},
                {"id": "cfdddb82-68da-4318-8464-ae12b8afdd50", "parent": None, "name": "اپلیکیشن", "eng_name": "app",
                 "open_chatrbazi": 2, "all_chatrbazi": 16.86},
                {"id": "19b87ad1-fdef-43de-a383-4a179ed4c990", "parent": None, "name": "مد ولباس",
                 "eng_name": "clothing", "open_chatrbazi": 1, "all_chatrbazi": 70000.0},
                {"id": "7207cb78-65ca-4895-a7e1-51edbfcb82d5", "parent": None, "name": "کمپین", "eng_name": "Campaign",
                 "open_chatrbazi": 0, "all_chatrbazi": None},
                {"id": "f31d0fc4-6ebb-40e8-b500-ac1225ec9264", "parent": None, "name": "همایش ها",
                 "eng_name": "Workshop", "open_chatrbazi": 1, "all_chatrbazi": None},
                {"id": "8a80d350-8aa7-44d0-bde9-377145ad90e5", "parent": None, "name": "موسیقی وفیلم",
                 "eng_name": "FilmMusic", "open_chatrbazi": 0, "all_chatrbazi": None},
                {"id": "a4acabab-26ee-48d0-b516-f677fe062060", "parent": None, "name": "آموزش مجازی",
                 "eng_name": "Education", "open_chatrbazi": 0, "all_chatrbazi": None},
                {"id": "c47179ba-778e-48df-bf67-810b8fb3f110", "parent": None, "name": "کتاب", "eng_name": "Book",
                 "open_chatrbazi": 1, "all_chatrbazi": 15000.0},
                {"id": "1d55677f-fa77-49c1-9c15-2af441f286ab", "parent": None, "name": "شارژواینترنت",
                 "eng_name": "Recharge", "open_chatrbazi": 0, "all_chatrbazi": None},
                {"id": "a8f0a957-2e90-4671-8868-afb53d810b80", "parent": None, "name": "خدماتی", "eng_name": "Service",
                 "open_chatrbazi": 0, "all_chatrbazi": None},
                {"id": "c7f356e4-beb0-4958-a184-bb56d95462f8", "parent": None, "name": "بیمه", "eng_name": "Insurance",
                 "open_chatrbazi": 1, "all_chatrbazi": 25000.0},
                {"id": "84969685-91d4-4e01-95b7-753557c98d35", "parent": None, "name": "گردشگری",
                 "eng_name": "Tourism", "open_chatrbazi": 0, "all_chatrbazi": None}]
        return CustomJSONRenderer().renderData(data)


class GetCity(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        print(str(City.objects.count()))
        dt = CitySerializer(City.objects.all(), many=True)
        return CustomJSONRenderer().renderData(dt.data)


class GetBanner(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        data = BannerSerializer(Banner.objects.all(), many=True).data
        return CustomJSONRenderer().renderData(data)


class GetOffer(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        limits = request.GET.get('limits', 10)
        try:
            limits = int(limits)
        except(ValueError):
            limits = 5
        if limits >= 30:
            limits = 30

        ordering = request.GET.get('ordering', '-priority')
        order = ['priority', '-priority', 'created_at']
        if ordering not in order:
            ordering = '-ordering'

        data = {"count": 18,
                "next": "http://chatrbaazan.ir/api/offer/?limit=10&offset=10&ordering=-priority&type=11%2C12",
                "previous": None, "results": [
                {"id": "37589ecf-6d00-4288-9aa3-f6e486296abc", "title": "کد دریافت اعتبار ۸ هزارتومانی ویژه اولین سفر",
                 "company": [{"name": "اسنپ", "eng_name": "Snapp"}],
                 "category": [{"name": "حمل ونقل", "eng_name": "transport"}],
                 "city": [{"name": "همه", "eng_name": "all"}], "create_date": "2018-09-28T16:55:32.816090Z",
                 "expiration_date": None, "link": "http://snapp.ir",
                 "explanation": "ویژه اولین استفاده از اپ\r\nبعداز انتخاب مبدا مقصد در قسمت کد تخفیف وارد کنید",
                 "priority": 8, "image": "http://chatrbaazan.ir/media/offer/Snapp-logo.svg_TBdiWUa.png", "tag": [
                    {"id": "2648b712-a29f-48ef-9e6e-5a1d446e6d58",
                     "labels": ["خرید اول", "سفارش اول", "اولین سفارش", "اولین سفر", "سفر اول"]}], "code": "ahre72",
                 "discount_value": 8000.0, "is_dollar": False, "chatrbazi": 8000.0, "resourcetype": "GiftCard"},
                {"id": "1f875d82-2aaf-4447-8e4f-9e7cea0f2b00", "title": "کد تخفیف هواپیما، اتوبوس، قطار",
                 "company": [{"name": "مستربلیط", "eng_name": "MrBilit"}],
                 "category": [{"name": "بلیت سفر", "eng_name": "Travel"}], "city": [{"name": "همه", "eng_name": "all"}],
                 "create_date": "2018-09-16T14:48:44.490684Z", "expiration_date": None, "link": "http://mrbilit.ir",
                 "explanation": "هواپیما: 20 تومن\r\nقطار: 10 تومن\r\nاتوبوس: 5 تومن\r\n\r\n⏰ تا آخر مهر \r\n- فقط روی اپلیکیشن\r\n\r\nدانلود از سیب اپ : \r\nbit.ly/2QoZomZ\r\nدانلود از بازار :\r\nbit.ly/2QoZZVL",
                 "priority": 6, "image": "http://chatrbaazan.ir/media/offer/mrbilit.png",
                 "tag": [{"id": "d45f883d-c9dc-45a8-8b18-bbacbcf018a6", "labels": ["قطار"]},
                         {"id": "a1ae6638-ea34-4363-a658-7f31db10dbed", "labels": ["اتوبوس"]},
                         {"id": "1d62c4cb-09dd-446c-b72f-f02882e30eee", "labels": ["هواپیما"]}], "code": "mrchtr697",
                 "discount_value": 20000.0, "is_dollar": False, "chatrbazi": 20000.0, "resourcetype": "GiftCard"},
                {"id": "57be1681-5baf-4de9-8fee-b48737d4b510", "title": "کد تخفیف 20درصد سفارش غذا",
                 "company": [{"name": "چنگال", "eng_name": "Changal"}],
                 "category": [{"name": "سفارش غذا", "eng_name": "food"}],
                 "city": [{"name": "تهران", "eng_name": "Tehran"}, {"name": "کیش", "eng_name": "Kish"},
                          {"name": "کرج", "eng_name": "Karaj"}, {"name": "تبریز", "eng_name": "Tabriz"}],
                 "create_date": "2018-10-12T19:36:24.742328Z", "expiration_date": None, "link": "http://changal.com",
                 "explanation": "کد تخفیف همیشگی برای همه ی عزیزان مخاطب سایت", "priority": 6,
                 "image": "http://chatrbaazan.ir/media/offer/changal.jpg", "tag": [], "code": "chatrbaazan",
                 "discount_percentage": 20.0, "discount_limit": 30000.0, "is_dollar": False, "chatrbazi": 6000.0,
                 "resourcetype": "Coupon"},
                {"id": "a04badf9-bb4b-47c1-948c-c8fb1ad6228f", "title": "کد تخفیف 20% همیشگی برای اعضا کانال",
                 "company": [{"name": "چنگال", "eng_name": "Changal"}],
                 "category": [{"name": "سفارش غذا", "eng_name": "food"}],
                 "city": [{"name": "تهران", "eng_name": "Tehran"}, {"name": "کیش", "eng_name": "Kish"},
                          {"name": "کرج", "eng_name": "Karaj"}, {"name": "تبریز", "eng_name": "Tabriz"}],
                 "create_date": "2018-09-13T20:50:11.129379Z", "expiration_date": None, "link": "https://changal.com/",
                 "explanation": "تا سقف 30 هزارتومان", "priority": 6,
                 "image": "http://chatrbaazan.ir/media/offer/photo_2018-09-08_14-22-26.jpg", "tag": [],
                 "code": "chatrbaazan", "discount_percentage": 20.0, "discount_limit": 30000.0, "is_dollar": False,
                 "chatrbazi": 6000.0, "resourcetype": "Coupon"},
                {"id": "bb8d5b80-d8f0-4497-ab15-c0c37fa1b206", "title": "25% تخفیف ‏مخصوص کفش",
                 "company": [{"name": "دیجی استایل", "eng_name": "DigiStyle"}],
                 "category": [{"name": "کیف وکفش", "eng_name": "Shoes"}], "city": [{"name": "همه", "eng_name": "all"}],
                 "create_date": "2018-09-13T20:55:31.233569Z", "expiration_date": "2018-10-30T17:52:06Z", "link": "",
                 "explanation": "", "priority": 6, "image": "http://chatrbaazan.ir/media/offer/digistyle_Iyt1rnw.jpg",
                 "tag": [], "code": "DSS25", "discount_percentage": 25.0, "discount_limit": 1000000.0,
                 "is_dollar": False, "chatrbazi": 25000.0, "resourcetype": "Coupon"},
                {"id": "18a7313a-78fe-4be2-a4ba-ce079312fa87", "title": "فقط خریداول روی اپلیکیشن",
                 "company": [{"name": "مستربلیط", "eng_name": "MrBilit"}],
                 "category": [{"name": "حمل ونقل", "eng_name": "transport"}],
                 "city": [{"name": "همه", "eng_name": "all"}], "create_date": "2018-09-13T20:59:01.530994Z",
                 "expiration_date": "2018-09-30T00:00:00Z", "link": "http://bit.ly/2QoZZVL",
                 "explanation": ":alarm_clock: تا آخر مهر \r\n- فقط خریداول روی اپلیکیشن", "priority": 4,
                 "image": "http://chatrbaazan.ir/media/offer/5025e6f2-0e2f-4689-b046-051ee7b0588a.jpg", "tag": [],
                 "code": "mrchtr697", "discount_value": 10000.0, "is_dollar": False, "chatrbazi": 10000.0,
                 "resourcetype": "GiftCard"},
                {"id": "48b7d218-64de-4826-ad3e-504a96bd9df8", "title": "کد تخفیف 20 هزار تومانی",
                 "company": [{"name": "کالا", "eng_name": "Kala"}],
                 "category": [{"name": "فروشگاه اینترنتی", "eng_name": "onlineShop"}],
                 "city": [{"name": "همه", "eng_name": "all"}], "create_date": "2018-09-14T12:37:46.646615Z",
                 "expiration_date": "2018-09-22T00:00:00Z", "link": "http://kala.ir",
                 "explanation": "بدون محدودیت سفارش اول\r\n حداقل خرید 100 هزار تومان", "priority": 4,
                 "image": "http://chatrbaazan.ir/media/offer/photo_2018-09-14_17-20-40.jpg", "tag": [],
                 "code": "KALASUMMER", "discount_value": 20000.0, "is_dollar": False, "chatrbazi": 20000.0,
                 "resourcetype": "GiftCard"},
                {"id": "5354f763-2949-4600-9102-0816a55ee470", "title": "کد تخفیف 15 هزار تومانی سوپرمارکت آنلاین",
                 "company": [{"name": "اسنپ مارکت", "eng_name": "SnappMarket"}],
                 "category": [{"name": "سوپر مارکت", "eng_name": "SuperMarket"}],
                 "city": [{"name": "تهران", "eng_name": "Tehran"}], "create_date": "2018-09-28T17:35:03.525698Z",
                 "expiration_date": None, "link": "http://snapp.market",
                 "explanation": "این کد مخصوص سفارش اول می باشد و بر روی سبد های با حداقل خرید 30 هزار تومان اعمال می شود",
                 "priority": 4, "image": "http://chatrbaazan.ir/media/offer/snappmarket.png", "tag": [
                    {"id": "2648b712-a29f-48ef-9e6e-5a1d446e6d58",
                     "labels": ["خرید اول", "سفارش اول", "اولین سفارش", "اولین سفر", "سفر اول"]}], "code": "SjetL24",
                 "discount_value": 15000.0, "is_dollar": False, "chatrbazi": 15000.0, "resourcetype": "GiftCard"},
                {"id": "6a1b26e3-0ea5-402c-878c-14a75b1538da",
                 "title": "کد تخفیف 10 هزارتومانی خرید از سوپرمارکت خرید بالای 100 هزارتومان",
                 "company": [{"name": "بامیلو", "eng_name": "Bamilo"}],
                 "category": [{"name": "سوپر مارکت", "eng_name": "SuperMarket"}],
                 "city": [{"name": "همه", "eng_name": "all"}], "create_date": "2018-10-28T22:02:22.806864Z",
                 "expiration_date": "2018-11-06T00:00:00Z", "link": "https://www.bamilo.com/", "explanation": "",
                 "priority": 4, "image": "http://chatrbaazan.ir/media/offer/bamilo_zWqq8Fg.jpg", "tag": [],
                 "code": "bml_supermarket10k", "discount_value": 10000.0, "is_dollar": False, "chatrbazi": 10000.0,
                 "resourcetype": "GiftCard"},
                {"id": "80fc3ec7-485b-4c55-b7e2-46e43aded77b", "title": "کد تخفیف 25 هزار تومانی ویژه محصولات چرم",
                 "company": [{"name": "بامیلو", "eng_name": "Bamilo"}],
                 "category": [{"name": "کیف وکفش", "eng_name": "Shoes"}, {"name": "لباس", "eng_name": "Clothe"}],
                 "city": [{"name": "همه", "eng_name": "all"}], "create_date": "2018-10-28T22:00:19.246423Z",
                 "expiration_date": "2018-11-06T00:00:00Z", "link": "http://bamilo.com",
                 "explanation": "- خرید بالای 100 هزار تومان", "priority": 4,
                 "image": "http://chatrbaazan.ir/media/offer/bamilo_jefXPxr.jpg",
                 "tag": [{"id": "010e77d1-8ac6-477d-8b13-f6af06bc220f", "labels": ["چرم", "محصول چرم", "کیف"]}],
                 "code": "sv_charmara_25", "discount_value": 25000.0, "is_dollar": False, "chatrbazi": 25000.0,
                 "resourcetype": "GiftCard"}],
                "categories": [["Reservation", "هتل واقامتگاه"], ["transport", "حمل ونقل"], ["Travel", "بلیت سفر"],
                               ["Shoes", "کیف وکفش"], ["Clothe", "لباس"], ["SuperMarket", "سوپر مارکت"],
                               ["clothing", "مد ولباس"], ["Book", "کتاب"], ["onlineShop", "فروشگاه اینترنتی"],
                               ["food", "سفارش غذا"]],
                "companies": [["Tap30", "تپ سی"], ["MrBilit", "مستربلیط"], ["DigiStyle", "دیجی استایل"],
                              ["Kala", "کالا"], ["Snapp", "اسنپ"], ["Snapptrip", "اسنپ تریپ"], ["Fidibo", "فیدیبو"],
                              ["SnappMarket", "اسنپ مارکت"], ["Bamilo", "بامیلو"], ["Changal", "چنگال"],
                              ["Modiseh", "مدیسه"], ["Touchsi", "تاچ سی"]]}
        return CustomJSONRenderer().renderData(data)
