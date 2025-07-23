from django.contrib import admin
from .models import HomeBanner, Page, ContactSubmission, NewsletterSubscriber, FAQ, PopupNotification, SocialLink

admin.site.register(HomeBanner)
admin.site.register(Page)
admin.site.register(ContactSubmission)
admin.site.register(NewsletterSubscriber)
admin.site.register(FAQ)
admin.site.register(PopupNotification)
admin.site.register(SocialLink)