from django.urls import path
from .views import (
    ActiveHomeBannerListView,
    PageDetailView,
    ContactSubmissionCreateView,
    NewsletterSubscribeView,
    FAQListView,
    PopupNotificationView,
    SocialLinksView,
)

urlpatterns = [
    path('banners/', ActiveHomeBannerListView.as_view(), name='banners'),
    path('pages/<slug:slug>/', PageDetailView.as_view(), name='page-detail'),
    path('contact/', ContactSubmissionCreateView.as_view(), name='contact-submit'),
    path('newsletter/subscribe/', NewsletterSubscribeView.as_view(), name='newsletter-subscribe'),
    path('faqs/', FAQListView.as_view(), name='faq-list'),
    path('popup/', PopupNotificationView.as_view(), name='popup-latest'),
    path('social-links/', SocialLinksView.as_view(), name='social-links'),
]
