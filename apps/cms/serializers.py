from rest_framework import serializers
from .models import (
    HomeBanner, Page, ContactSubmission, NewsletterSubscriber,
    FAQ, PopupNotification, SocialLink
)

class HomeBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeBanner
        fields = '__all__'

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = '__all__'

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']

class NewsletterSubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']

class PopupNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PopupNotification
        fields = ['id', 'title', 'content']

class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['platform', 'url', 'icon']