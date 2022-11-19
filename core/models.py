from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('User must have an Email')
        if not password:
            raise ValueError('User must have a Password')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = False
        user.is_staff = False
        user.is_ambassador = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('User must have an Email')
        if not password:
            raise ValueError('User must have a Password')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_ambassador = False
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField(unique=True)
    password = models.TextField()
    is_ambassador = models.BooleanField(default=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    object = UserManager()

class Product(models.Model):
    title = models.TextField()
    description = models.TextField(null=True)
    image = models.TextField()
    # DecimalField:固定小数点
    # max_digits 数字部分の最大桁数
    # decimal_places 小数部分の桁数
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Link(models.Model):
    code = models.TextField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    transacrion_id = models.TextField(null=True)
    # SET_NULL:オブジェクトが削除されると、代わりにNULLをセット
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    code = models.TextField()
    ambassador_email = models.TextField()
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    address = models.TextField(null=True)
    city = models.TextField(null=True)
    country = models.TextField(null=True)
    zip = models.TextField(null=True)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    # related_name:逆参照するときの名前を指定
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product_title = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    admin_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    ambassador_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)