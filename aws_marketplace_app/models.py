from django.contrib.auth import models as authModels
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=False, blank=False)
    created_by = models.ForeignKey(
        authModels.User, on_delete=models.CASCADE, related_name="category_created_by")
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(authModels.User, null=True, blank=True,
                                   on_delete=models.CASCADE, related_name="category_updated_by")
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(authModels.User, null=True, blank=True,
                                   on_delete=models.CASCADE, related_name="category_deleted_by")

    def __str__(self):
        return self.name


class Posting(models.Model):

    class ItemCondition(models.IntegerChoices):
        NEW = 1, _('New')
        LIKE_NEW = 2, _('Used - Like New')
        EXCELLENT = 3, _('Used - Excellent')
        GOOD = 4, _('Used - Good')
        FAIR = 5, _('Used - Fair')
        SALVAGE = 6, _('Used - Salvage')

        __empty__ = _('(Unknown)')

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True, default=None)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    address = models.CharField(
        max_length=256, null=True, blank=True, default=None)
    postal_code = models.IntegerField(null=True, blank=True, default=None)
    manufacturer = models.CharField(
        max_length=256, null=True, blank=True, default=None)
    model_name = models.CharField(
        max_length=256, null=True, blank=True, default=None)
    length_cm = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    width_cm = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    height_cm = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True, default=0)
    condition = models.IntegerField(
        choices=ItemCondition.choices, default=ItemCondition.NEW)
    can_meetup = models.BooleanField(default=True)
    can_deliver = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=True)
    is_reserved = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=False, blank=False)
    created_by = models.ForeignKey(
        authModels.User, on_delete=models.CASCADE, related_name="posting_created_by")
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(authModels.User, null=True, blank=True,
                                   on_delete=models.CASCADE, related_name="posting_updated_by")
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(authModels.User, null=True, blank=True,
                                   on_delete=models.CASCADE, related_name="posting_deleted_by")

    def __str__(self):
        return self.title


class UserProfile(models.Model):

    class UserGender(models.IntegerChoices):
        MALE = 1, _('Male')
        FEMALE = 2, _('Female')
        OTHER = 3, _('Other')

        __empty__ = _('(Unknown)')

    user = models.OneToOneField(
        authModels.User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    display_image = models.ImageField(
        upload_to='uploads/media/user_display_image', null=True, blank=True)
    biography = models.CharField(max_length=256, null=True, blank=True)
    gender = models.IntegerField(
        choices=UserGender.choices, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    mobile_no = models.CharField(max_length=13, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=False, blank=False)
    created_by = models.ForeignKey(
        authModels.User, on_delete=models.CASCADE, related_name="user_profile_created_by")
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(authModels.User, null=True, blank=True,
                                   on_delete=models.CASCADE, related_name="user_profile_updated_by")
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(authModels.User, null=True, blank=True,
                                   on_delete=models.CASCADE, related_name="user_profile_deleted_by")


class PostingImage(models.Model):

    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/media/posting_image')
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=False, blank=False)
    created_by = models.ForeignKey(
        authModels.User, on_delete=models.CASCADE, related_name="posting_image_created_by")
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(authModels.User, null=True, blank=True,
                                   on_delete=models.CASCADE, related_name="posting_image_updated_by")
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(authModels.User, null=True, blank=True,
                                   on_delete=models.CASCADE, related_name="posting_image_deleted_by")


class Wishlist(models.Model):
    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=False, blank=False)
    created_by = models.ForeignKey(authModels.User, null=True, blank=True,
                                   on_delete=models.CASCADE, related_name="wishlist_created_by")


class Order(models.Model):

    class OrderStatus(models.IntegerChoices):
        PENDING = 0, _('Pending')
        PACKED = 1, _('Packed')
        SHIPPED = 2, _('Shipped')
        DELIVERED = 3, _('Delivered')
        CANCELLED_BY_USER = 81, _('Cancelled by User')
        CANCELLED_BY_SELLER = 82, _('Cancelled by Seller')

        __empty__ = _('(Unknown)')

    posting = models.ForeignKey(Posting, on_delete=models.CASCADE)
    status = models.IntegerField(
        choices=OrderStatus.choices, default=OrderStatus.PENDING)
    is_complete = models.BooleanField(default=False)
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=False, blank=False)
    created_by = models.ForeignKey(
        authModels.User, on_delete=models.CASCADE, related_name="order_created_by")
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(authModels.User, null=True, blank=True,
                                   on_delete=models.CASCADE, related_name="order_updated_by")
