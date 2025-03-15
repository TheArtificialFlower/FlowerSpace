from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator,MaxValueValidator


class Category(models.Model):
    sub_category = models.ForeignKey("self", on_delete=models.CASCADE, related_name="s_categories", blank=True, null=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:category_filter", args=[self.slug,])


class Product(models.Model):
    category = models.ManyToManyField(Category, related_name="products")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, unique=True)
    image = models.ImageField(upload_to="shop/")
    description = models.TextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        category = self.category.filter(is_sub=False).first()
        return reverse("shop:product_details", args=[category.slug, self.slug])





class Order(models.Model):
    CHOICES = (
        ('pending', 'PENDING'),
        ('delivered', 'DELIVERED'),
        ('denied', 'DENIED'),
        ('shipping', 'SHIPPING')
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="orders")
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coupon = models.IntegerField(null=True, blank=True, default=None)
    status = models.CharField(max_length=100, choices=CHOICES, default='pending')

    address = models.CharField(max_length=500, default="")
    client_info = models.CharField(max_length=50, default="")

    class Meta:
        ordering = ("paid", "-updated")

    def __str__(self):
        return f"{self.user} --- {self.paid}"

    def get_total_price(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.coupon:
            total = total - ((self.coupon / 100) * total)
        return int(total)



class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity



class Coupons(models.Model):
    code = models.CharField(max_length=20, unique=True)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    discount = models.IntegerField(validators=[MaxValueValidator(99),MinValueValidator(1)])
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.code
