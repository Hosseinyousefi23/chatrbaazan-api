from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from shop.renderers import CustomJSONRenderer


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
                 "open_chatrbazi": 2, "all_chatrbazi": 12000.0***REMOVED***,
                {"id": "324e4bab-5e8e-426a-8c29-25d0be1e8012", "parent": None, "name": "فروشگاه اینترنتی",
                 "eng_name": "onlineShop", "open_chatrbazi": 1, "all_chatrbazi": 85000.0***REMOVED***,
                {"id": "c2670bd6-f71f-4bfe-8315-ce022e1ad067", "parent": None, "name": "حمل ونقل",
                 "eng_name": "transport", "open_chatrbazi": 1, "all_chatrbazi": 27700.0***REMOVED***,
                {"id": "cfdddb82-68da-4318-8464-ae12b8afdd50", "parent": None, "name": "اپلیکیشن", "eng_name": "app",
                 "open_chatrbazi": 2, "all_chatrbazi": 16.86***REMOVED***,
                {"id": "19b87ad1-fdef-43de-a383-4a179ed4c990", "parent": None, "name": "مد ولباس",
                 "eng_name": "clothing", "open_chatrbazi": 1, "all_chatrbazi": 70000.0***REMOVED***,
                {"id": "7207cb78-65ca-4895-a7e1-51edbfcb82d5", "parent": None, "name": "کمپین", "eng_name": "Campaign",
                 "open_chatrbazi": 0, "all_chatrbazi": None***REMOVED***,
                {"id": "f31d0fc4-6ebb-40e8-b500-ac1225ec9264", "parent": None, "name": "همایش ها",
                 "eng_name": "Workshop", "open_chatrbazi": 1, "all_chatrbazi": None***REMOVED***,
                {"id": "8a80d350-8aa7-44d0-bde9-377145ad90e5", "parent": None, "name": "موسیقی وفیلم",
                 "eng_name": "FilmMusic", "open_chatrbazi": 0, "all_chatrbazi": None***REMOVED***,
                {"id": "a4acabab-26ee-48d0-b516-f677fe062060", "parent": None, "name": "آموزش مجازی",
                 "eng_name": "Education", "open_chatrbazi": 0, "all_chatrbazi": None***REMOVED***,
                {"id": "c47179ba-778e-48df-bf67-810b8fb3f110", "parent": None, "name": "کتاب", "eng_name": "Book",
                 "open_chatrbazi": 1, "all_chatrbazi": 15000.0***REMOVED***,
                {"id": "1d55677f-fa77-49c1-9c15-2af441f286ab", "parent": None, "name": "شارژواینترنت",
                 "eng_name": "Recharge", "open_chatrbazi": 0, "all_chatrbazi": None***REMOVED***,
                {"id": "a8f0a957-2e90-4671-8868-afb53d810b80", "parent": None, "name": "خدماتی", "eng_name": "Service",
                 "open_chatrbazi": 0, "all_chatrbazi": None***REMOVED***,
                {"id": "c7f356e4-beb0-4958-a184-bb56d95462f8", "parent": None, "name": "بیمه", "eng_name": "Insurance",
                 "open_chatrbazi": 1, "all_chatrbazi": 25000.0***REMOVED***,
                {"id": "84969685-91d4-4e01-95b7-753557c98d35", "parent": None, "name": "گردشگری",
                 "eng_name": "Tourism", "open_chatrbazi": 0, "all_chatrbazi": None***REMOVED***]
        return CustomJSONRenderer().renderData(data)


class GetCity(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        data = [{"id": "47d935e2-4ca2-4f31-8cd6-922380685e79", "parent": None, "name": "مشهد", "eng_name": "Mashhad"***REMOVED***,
                {"id": "b7c8e489-d272-40b5-b25f-c94a19cb287f", "parent": None, "name": "ساری", "eng_name": "Sari"***REMOVED***,
                {"id": "de13066f-1fe8-498e-bb42-303b92a848ef", "parent": None, "name": "انزلی", "eng_name": "Anzali"***REMOVED***,
                {"id": "dd504850-449d-4d55-9af6-96e4a8d627d6", "parent": None, "name": "رشت", "eng_name": "Rasht"***REMOVED***,
                {"id": "1c4b4ada-29ae-4504-ae37-436ad1f1c4a7", "parent": None, "name": "لاهیجان",
                 "eng_name": "Lahijan"***REMOVED***,
                {"id": "38af91e2-29e3-4d25-9359-a31ba8e45ef9", "parent": None, "name": "ارومیه", "eng_name": "Urmia"***REMOVED***,
                {"id": "74d6a077-1bce-4ecf-ada6-ec88cbcf7b79", "parent": None, "name": "نیشابور",
                 "eng_name": "Neyshabur"***REMOVED***,
                {"id": "bb8317af-8a97-4555-975f-6bc545f524c1", "parent": None, "name": "سبزوار",
                 "eng_name": "Sabzevar"***REMOVED***,
                {"id": "88036f54-bb92-4324-aa08-e0e045a982bb", "parent": None, "name": "اردکان",
                 "eng_name": "Ardekan"***REMOVED***,
                {"id": "854c3346-e1be-44f5-83e0-4f201a78f8d4", "parent": None, "name": "یزد", "eng_name": "Yazd"***REMOVED***,
                {"id": "7baaa4e6-bce3-4d87-bd41-041ca894a993", "parent": None, "name": "طبس", "eng_name": "Tabas"***REMOVED***,
                {"id": "0fcb9703-e4d4-4c63-86b6-fa6b3c421a49", "parent": None, "name": "کرمان", "eng_name": "kerman"***REMOVED***,
                {"id": "ca6eb434-3673-472b-8528-d1494d47fee7", "parent": None, "name": "اهواز", "eng_name": "Ahwaz"***REMOVED***,
                {"id": "91080a00-3cab-4ebf-a317-f334bba70de7", "parent": None, "name": "تبریز", "eng_name": "Tabriz"***REMOVED***,
                {"id": "b6feecc2-7d42-4944-8844-d4bf33eefa9a", "parent": None, "name": "قم", "eng_name": "Qom"***REMOVED***,
                {"id": "5ea747d4-24e4-4f40-b4fd-e35c2e2b4ce9", "parent": None, "name": "اصفهان",
                 "eng_name": "Esfehan"***REMOVED***,
                {"id": "3093442d-515c-4ea0-8673-09690400c86e", "parent": None, "name": "شیراز", "eng_name": "Shiraz"***REMOVED***,
                {"id": "da232ac7-5466-44e9-ba78-97f9ab775de0", "parent": None, "name": "کرج", "eng_name": "Karaj"***REMOVED***,
                {"id": "ae4a76be-4614-4ac3-80d1-b48aa244b7dc", "parent": None, "name": "گرگان", "eng_name": "Gorgan"***REMOVED***,
                {"id": "8ac96a83-f16f-4940-9d40-c7d566984a53", "parent": None, "name": "کیش", "eng_name": "Kish"***REMOVED***,
                {"id": "0a1eb53b-f8d4-4b90-88cc-012c0a42c11b", "parent": None, "name": "تهران", "eng_name": "Tehran"***REMOVED***,
                {"all_chatrbazi": 329700.0***REMOVED***]
        return CustomJSONRenderer().renderData(data)


class GetBanner(APIView):
    permission_classes = (AllowAny,)
    allowed_methods = ('GET',)

    # renderer_classes = (JSONRenderer,)

    def get(self, request, format=None, ):
        data = [
            {"id": "d65deacd-9b35-44f6-b039-2e0088dd1169", "link": "http://chatrbaazan.ir/changal", "is_active": True,
             "image": "http://chatrbaazan.ir/media/banner/changal.jpg"***REMOVED***,
            {"id": "17f75c12-8c6a-4ff3-913f-91617b2030ec", "link": "http://chatrbaazan.ir/mrbilit", "is_active": True,
             "image": "http://chatrbaazan.ir/media/banner/mrbilit.jpg"***REMOVED***,
            {"id": "688c3c98-f356-4437-8637-0edea2e614ad", "link": "http://chatrbaazan.ir/company/bimehbazar",
             "is_active": True, "image": "http://chatrbaazan.ir/media/banner/Untitled-2.png"***REMOVED***]
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
                 "company": [{"name": "اسنپ", "eng_name": "Snapp"***REMOVED***],
                 "category": [{"name": "حمل ونقل", "eng_name": "transport"***REMOVED***],
                 "city": [{"name": "همه", "eng_name": "all"***REMOVED***], "create_date": "2018-09-28T16:55:32.816090Z",
                 "expiration_date": None, "link": "http://snapp.ir",
                 "explanation": "ویژه اولین استفاده از اپ\r\nبعداز انتخاب مبدا مقصد در قسمت کد تخفیف وارد کنید",
                 "priority": 8, "image": "http://chatrbaazan.ir/media/offer/Snapp-logo.svg_TBdiWUa.png", "tag": [
                    {"id": "2648b712-a29f-48ef-9e6e-5a1d446e6d58",
                     "labels": ["خرید اول", "سفارش اول", "اولین سفارش", "اولین سفر", "سفر اول"]***REMOVED***], "code": "ahre72",
                 "discount_value": 8000.0, "is_dollar": False, "chatrbazi": 8000.0, "resourcetype": "GiftCard"***REMOVED***,
                {"id": "1f875d82-2aaf-4447-8e4f-9e7cea0f2b00", "title": "کد تخفیف هواپیما، اتوبوس، قطار",
                 "company": [{"name": "مستربلیط", "eng_name": "MrBilit"***REMOVED***],
                 "category": [{"name": "بلیت سفر", "eng_name": "Travel"***REMOVED***], "city": [{"name": "همه", "eng_name": "all"***REMOVED***],
                 "create_date": "2018-09-16T14:48:44.490684Z", "expiration_date": None, "link": "http://mrbilit.ir",
                 "explanation": "هواپیما: 20 تومن\r\nقطار: 10 تومن\r\nاتوبوس: 5 تومن\r\n\r\n⏰ تا آخر مهر \r\n- فقط روی اپلیکیشن\r\n\r\nدانلود از سیب اپ : \r\nbit.ly/2QoZomZ\r\nدانلود از بازار :\r\nbit.ly/2QoZZVL",
                 "priority": 6, "image": "http://chatrbaazan.ir/media/offer/mrbilit.png",
                 "tag": [{"id": "d45f883d-c9dc-45a8-8b18-bbacbcf018a6", "labels": ["قطار"]***REMOVED***,
                         {"id": "a1ae6638-ea34-4363-a658-7f31db10dbed", "labels": ["اتوبوس"]***REMOVED***,
                         {"id": "1d62c4cb-09dd-446c-b72f-f02882e30eee", "labels": ["هواپیما"]***REMOVED***], "code": "mrchtr697",
                 "discount_value": 20000.0, "is_dollar": False, "chatrbazi": 20000.0, "resourcetype": "GiftCard"***REMOVED***,
                {"id": "57be1681-5baf-4de9-8fee-b48737d4b510", "title": "کد تخفیف 20درصد سفارش غذا",
                 "company": [{"name": "چنگال", "eng_name": "Changal"***REMOVED***],
                 "category": [{"name": "سفارش غذا", "eng_name": "food"***REMOVED***],
                 "city": [{"name": "تهران", "eng_name": "Tehran"***REMOVED***, {"name": "کیش", "eng_name": "Kish"***REMOVED***,
                          {"name": "کرج", "eng_name": "Karaj"***REMOVED***, {"name": "تبریز", "eng_name": "Tabriz"***REMOVED***],
                 "create_date": "2018-10-12T19:36:24.742328Z", "expiration_date": None, "link": "http://changal.com",
                 "explanation": "کد تخفیف همیشگی برای همه ی عزیزان مخاطب سایت", "priority": 6,
                 "image": "http://chatrbaazan.ir/media/offer/changal.jpg", "tag": [], "code": "chatrbaazan",
                 "discount_percentage": 20.0, "discount_limit": 30000.0, "is_dollar": False, "chatrbazi": 6000.0,
                 "resourcetype": "Coupon"***REMOVED***,
                {"id": "a04badf9-bb4b-47c1-948c-c8fb1ad6228f", "title": "کد تخفیف 20% همیشگی برای اعضا کانال",
                 "company": [{"name": "چنگال", "eng_name": "Changal"***REMOVED***],
                 "category": [{"name": "سفارش غذا", "eng_name": "food"***REMOVED***],
                 "city": [{"name": "تهران", "eng_name": "Tehran"***REMOVED***, {"name": "کیش", "eng_name": "Kish"***REMOVED***,
                          {"name": "کرج", "eng_name": "Karaj"***REMOVED***, {"name": "تبریز", "eng_name": "Tabriz"***REMOVED***],
                 "create_date": "2018-09-13T20:50:11.129379Z", "expiration_date": None, "link": "https://changal.com/",
                 "explanation": "تا سقف 30 هزارتومان", "priority": 6,
                 "image": "http://chatrbaazan.ir/media/offer/photo_2018-09-08_14-22-26.jpg", "tag": [],
                 "code": "chatrbaazan", "discount_percentage": 20.0, "discount_limit": 30000.0, "is_dollar": False,
                 "chatrbazi": 6000.0, "resourcetype": "Coupon"***REMOVED***,
                {"id": "bb8d5b80-d8f0-4497-ab15-c0c37fa1b206", "title": "25% تخفیف ‏مخصوص کفش",
                 "company": [{"name": "دیجی استایل", "eng_name": "DigiStyle"***REMOVED***],
                 "category": [{"name": "کیف وکفش", "eng_name": "Shoes"***REMOVED***], "city": [{"name": "همه", "eng_name": "all"***REMOVED***],
                 "create_date": "2018-09-13T20:55:31.233569Z", "expiration_date": "2018-10-30T17:52:06Z", "link": "",
                 "explanation": "", "priority": 6, "image": "http://chatrbaazan.ir/media/offer/digistyle_Iyt1rnw.jpg",
                 "tag": [], "code": "DSS25", "discount_percentage": 25.0, "discount_limit": 1000000.0,
                 "is_dollar": False, "chatrbazi": 25000.0, "resourcetype": "Coupon"***REMOVED***,
                {"id": "18a7313a-78fe-4be2-a4ba-ce079312fa87", "title": "فقط خریداول روی اپلیکیشن",
                 "company": [{"name": "مستربلیط", "eng_name": "MrBilit"***REMOVED***],
                 "category": [{"name": "حمل ونقل", "eng_name": "transport"***REMOVED***],
                 "city": [{"name": "همه", "eng_name": "all"***REMOVED***], "create_date": "2018-09-13T20:59:01.530994Z",
                 "expiration_date": "2018-09-30T00:00:00Z", "link": "http://bit.ly/2QoZZVL",
                 "explanation": ":alarm_clock: تا آخر مهر \r\n- فقط خریداول روی اپلیکیشن", "priority": 4,
                 "image": "http://chatrbaazan.ir/media/offer/5025e6f2-0e2f-4689-b046-051ee7b0588a.jpg", "tag": [],
                 "code": "mrchtr697", "discount_value": 10000.0, "is_dollar": False, "chatrbazi": 10000.0,
                 "resourcetype": "GiftCard"***REMOVED***,
                {"id": "48b7d218-64de-4826-ad3e-504a96bd9df8", "title": "کد تخفیف 20 هزار تومانی",
                 "company": [{"name": "کالا", "eng_name": "Kala"***REMOVED***],
                 "category": [{"name": "فروشگاه اینترنتی", "eng_name": "onlineShop"***REMOVED***],
                 "city": [{"name": "همه", "eng_name": "all"***REMOVED***], "create_date": "2018-09-14T12:37:46.646615Z",
                 "expiration_date": "2018-09-22T00:00:00Z", "link": "http://kala.ir",
                 "explanation": "بدون محدودیت سفارش اول\r\n حداقل خرید 100 هزار تومان", "priority": 4,
                 "image": "http://chatrbaazan.ir/media/offer/photo_2018-09-14_17-20-40.jpg", "tag": [],
                 "code": "KALASUMMER", "discount_value": 20000.0, "is_dollar": False, "chatrbazi": 20000.0,
                 "resourcetype": "GiftCard"***REMOVED***,
                {"id": "5354f763-2949-4600-9102-0816a55ee470", "title": "کد تخفیف 15 هزار تومانی سوپرمارکت آنلاین",
                 "company": [{"name": "اسنپ مارکت", "eng_name": "SnappMarket"***REMOVED***],
                 "category": [{"name": "سوپر مارکت", "eng_name": "SuperMarket"***REMOVED***],
                 "city": [{"name": "تهران", "eng_name": "Tehran"***REMOVED***], "create_date": "2018-09-28T17:35:03.525698Z",
                 "expiration_date": None, "link": "http://snapp.market",
                 "explanation": "این کد مخصوص سفارش اول می باشد و بر روی سبد های با حداقل خرید 30 هزار تومان اعمال می شود",
                 "priority": 4, "image": "http://chatrbaazan.ir/media/offer/snappmarket.png", "tag": [
                    {"id": "2648b712-a29f-48ef-9e6e-5a1d446e6d58",
                     "labels": ["خرید اول", "سفارش اول", "اولین سفارش", "اولین سفر", "سفر اول"]***REMOVED***], "code": "SjetL24",
                 "discount_value": 15000.0, "is_dollar": False, "chatrbazi": 15000.0, "resourcetype": "GiftCard"***REMOVED***,
                {"id": "6a1b26e3-0ea5-402c-878c-14a75b1538da",
                 "title": "کد تخفیف 10 هزارتومانی خرید از سوپرمارکت خرید بالای 100 هزارتومان",
                 "company": [{"name": "بامیلو", "eng_name": "Bamilo"***REMOVED***],
                 "category": [{"name": "سوپر مارکت", "eng_name": "SuperMarket"***REMOVED***],
                 "city": [{"name": "همه", "eng_name": "all"***REMOVED***], "create_date": "2018-10-28T22:02:22.806864Z",
                 "expiration_date": "2018-11-06T00:00:00Z", "link": "https://www.bamilo.com/", "explanation": "",
                 "priority": 4, "image": "http://chatrbaazan.ir/media/offer/bamilo_zWqq8Fg.jpg", "tag": [],
                 "code": "bml_supermarket10k", "discount_value": 10000.0, "is_dollar": False, "chatrbazi": 10000.0,
                 "resourcetype": "GiftCard"***REMOVED***,
                {"id": "80fc3ec7-485b-4c55-b7e2-46e43aded77b", "title": "کد تخفیف 25 هزار تومانی ویژه محصولات چرم",
                 "company": [{"name": "بامیلو", "eng_name": "Bamilo"***REMOVED***],
                 "category": [{"name": "کیف وکفش", "eng_name": "Shoes"***REMOVED***, {"name": "لباس", "eng_name": "Clothe"***REMOVED***],
                 "city": [{"name": "همه", "eng_name": "all"***REMOVED***], "create_date": "2018-10-28T22:00:19.246423Z",
                 "expiration_date": "2018-11-06T00:00:00Z", "link": "http://bamilo.com",
                 "explanation": "- خرید بالای 100 هزار تومان", "priority": 4,
                 "image": "http://chatrbaazan.ir/media/offer/bamilo_jefXPxr.jpg",
                 "tag": [{"id": "010e77d1-8ac6-477d-8b13-f6af06bc220f", "labels": ["چرم", "محصول چرم", "کیف"]***REMOVED***],
                 "code": "sv_charmara_25", "discount_value": 25000.0, "is_dollar": False, "chatrbazi": 25000.0,
                 "resourcetype": "GiftCard"***REMOVED***],
                "categories": [["Reservation", "هتل واقامتگاه"], ["transport", "حمل ونقل"], ["Travel", "بلیت سفر"],
                               ["Shoes", "کیف وکفش"], ["Clothe", "لباس"], ["SuperMarket", "سوپر مارکت"],
                               ["clothing", "مد ولباس"], ["Book", "کتاب"], ["onlineShop", "فروشگاه اینترنتی"],
                               ["food", "سفارش غذا"]],
                "companies": [["Tap30", "تپ سی"], ["MrBilit", "مستربلیط"], ["DigiStyle", "دیجی استایل"],
                              ["Kala", "کالا"], ["Snapp", "اسنپ"], ["Snapptrip", "اسنپ تریپ"], ["Fidibo", "فیدیبو"],
                              ["SnappMarket", "اسنپ مارکت"], ["Bamilo", "بامیلو"], ["Changal", "چنگال"],
                              ["Modiseh", "مدیسه"], ["Touchsi", "تاچ سی"]]***REMOVED***
        return CustomJSONRenderer().renderData(data)
