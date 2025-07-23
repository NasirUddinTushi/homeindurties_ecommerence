from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.IntegerField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # SEO fields
    meta_title = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Image for {self.product.title}"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  
    value = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.name}: {self.value}"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.product} ({self.rating})"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    products = models.ManyToManyField(Product, related_name='tags', blank=True)

    def __str__(self):
        return self.name
