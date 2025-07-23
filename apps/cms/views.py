from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    HomeBanner, Page, ContactSubmission, NewsletterSubscriber,
    FAQ, PopupNotification, SocialLink
)
from .serializers import (
    HomeBannerSerializer, PageSerializer, ContactSubmissionSerializer,
    NewsletterSubscriberSerializer, FAQSerializer,
    PopupNotificationSerializer, SocialLinkSerializer
)

def custom_response(success=True, message="", data=None, status_code=200):
    return Response({
        "success": success,
        "message": message,
        "data": data or {},
        "status": status_code
    }, status=status_code)

class ActiveHomeBannerListView(APIView):
    def get(self, request):
        banners = HomeBanner.objects.filter(is_active=True)
        serializer = HomeBannerSerializer(banners, many=True)
        return custom_response(
            success=True,
            message="Active banners retrieved successfully.",
            data=serializer.data
        )

class PageDetailView(APIView):
    def get(self, request, slug):
        try:
            page = Page.objects.get(slug=slug)
            serializer = PageSerializer(page)
            return custom_response(
                success=True,
                message="Page retrieved successfully.",
                data=serializer.data
            )
        except Page.DoesNotExist:
            return custom_response(
                success=False,
                message="Page not found.",
                status_code=404
            )

class ContactSubmissionCreateView(APIView):
    def post(self, request):
        serializer = ContactSubmissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                success=True,
                message="Contact form submitted successfully.",
                data=serializer.data,
                status_code=201
            )
        return custom_response(
            success=False,
            message="Invalid input.",
            data=serializer.errors,
            status_code=400
        )

class NewsletterSubscribeView(APIView):
    def post(self, request):
        serializer = NewsletterSubscriberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(
                success=True,
                message="Subscription successful.",
                data=serializer.data,
                status_code=201
            )
        return custom_response(
            success=False,
            message="Invalid input.",
            data=serializer.errors,
            status_code=400
        )

class FAQListView(APIView):
    def get(self, request):
        faqs = FAQ.objects.filter(is_active=True)
        serializer = FAQSerializer(faqs, many=True)
        return custom_response(
            success=True,
            message="FAQs retrieved successfully.",
            data=serializer.data
        )

class PopupNotificationView(APIView):
    def get(self, request):
        popup = PopupNotification.objects.filter(visible=True).order_by('-created_at').first()
        if not popup:
            return custom_response(
                success=False,
                message="No popup available.",
                status_code=404
            )
        serializer = PopupNotificationSerializer(popup)
        return custom_response(
            success=True,
            message="Popup notification retrieved.",
            data=serializer.data
        )

class SocialLinksView(APIView):
    def get(self, request):
        links = SocialLink.objects.all()
        serializer = SocialLinkSerializer(links, many=True)
        return custom_response(
            success=True,
            message="Social links retrieved.",
            data=serializer.data
        )