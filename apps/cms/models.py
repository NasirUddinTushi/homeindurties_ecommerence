from django.db import models

class HomeBanner(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='banners/')
    button_text = models.CharField(max_length=50, blank=True)
    button_link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Page(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

class PopupNotification(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SocialLink(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    icon = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.platform
