import datetime

from django.conf import settings
from django.db import models
from django_countries.fields import CountryField

from ..core.models import ModelWithMetadata
from ..permission.enums import ChannelPermissions
from . import AllocationStrategy, MarkAsPaidStrategy, TransactionFlowStrategy


class Channel(ModelWithMetadata):
    name = models.CharField(max_length=250)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True)
    currency_code = models.CharField(max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH)
    default_country = CountryField()
    allocation_strategy = models.CharField(
        max_length=255,
        choices=AllocationStrategy.CHOICES,
        default=AllocationStrategy.PRIORITIZE_SORTING_ORDER,
    )
    order_mark_as_paid_strategy = models.CharField(
        max_length=255,
        choices=MarkAsPaidStrategy.CHOICES,
        default=MarkAsPaidStrategy.PAYMENT_FLOW,
    )

    default_transaction_flow_strategy = models.CharField(
        max_length=255,
        choices=TransactionFlowStrategy.CHOICES,
        default=TransactionFlowStrategy.CHARGE,
    )

    automatically_confirm_all_new_orders = models.BooleanField(default=True, null=True)
    allow_unpaid_orders = models.BooleanField(default=False)
    automatically_fulfill_non_shippable_gift_card = models.BooleanField(
        default=True,
        null=True,
    )
    expire_orders_after = models.IntegerField(default=None, null=True, blank=True)

    delete_expired_orders_after = models.DurationField(
        default=datetime.timedelta(days=60),
    )

    include_draft_order_in_voucher_usage = models.BooleanField(default=False)

    use_legacy_error_flow_for_checkout = models.BooleanField(default=True)
    automatically_complete_fully_paid_checkouts = models.BooleanField(default=False)

    # automatic_completion_delay applies only when
    # automatically_complete_fully_paid_checkouts is set to True
    automatic_completion_delay = models.IntegerField(
        null=True, blank=True, default=None
    )
    # define the cut-off date for automatic completion of fully paid checkouts
    automatic_completion_cut_off_date = models.DateTimeField(null=True, blank=True)

    # time in hours after which the draft order line price will be refreshed
    draft_order_line_price_freeze_period = models.PositiveIntegerField(
        default=24, null=True, blank=True
    )

    # line lvl discounts for orders created from checkout are stored as
    # OrderLineDiscount. This flag controls how we should return it via API.

    use_legacy_line_discount_propagation_for_order = models.BooleanField(default=True)
    release_funds_for_expired_checkouts = models.BooleanField(default=False)
    checkout_ttl_before_releasing_funds = models.DurationField(
        default=datetime.timedelta(hours=6)
    )
    checkout_release_funds_cut_off_date = models.DateTimeField(null=True, blank=True)

    allow_legacy_gift_card_use = models.BooleanField(default=True, db_default=True)

    # Saleor Shop System Extensions
    shop_code = models.CharField(
        max_length=20,
        unique=True,
        help_text="Format: QF-2026-XXXXX"
    )
    owner = models.ForeignKey(
        'account.User',
        on_delete=models.CASCADE,
        related_name='owned_shops',
        null=True,
        blank=True
    )
    seller_name = models.CharField(max_length=200, blank=True)
    shop_type = models.CharField(
        max_length=50,
        choices=[
            ('GENERAL_STORE', 'General Store'),
            ('CLOTH', 'Cloth'),
            ('GRAIN', 'Grain'),
            ('BARBER', 'Barber'),
            ('TECHNICAL', 'Technical'),
            ('SOFTWARE', 'Software'),
            ('MOBILE_SELLING', 'Mobile Selling'),
            ('REPAIRING_MOBILE', 'Repairing Mobile'),
            ('REPAIRING_LAPTOP', 'Repairing Laptop'),
            ('MECHANICAL', 'Mechanical'),
            ('ELECTRONICS', 'Electronics'),
            ('FURNITURE', 'Furniture'),
            ('JEWELRY', 'Jewelry'),
            ('FOOTWEAR', 'Footwear'),
            ('STATIONERY', 'Stationery'),
            ('HOTEL', 'Hotel'),
            ('RESTAURANT', 'Restaurant'),
            ('DAIRY', 'Dairy'),
            ('AGRICULTURE', 'Agriculture'),
            ('MEDICAL', 'Medical'),
            ('HARDWARE', 'Hardware'),
            ('OTHER', 'Other')
        ],
        default='GENERAL_STORE'
    )
    village = models.CharField(max_length=100, blank=True)
    block = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    delivery_radius = models.FloatField(default=2.0)
    opening_time = models.CharField(max_length=20, blank=True)
    closing_time = models.CharField(max_length=20, blank=True)
    is_sunday_available = models.BooleanField(default=True)
    minimum_order = models.DecimalField(
        max_digits=10, decimal_places=2, default=50.00
    )
    verification_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('layer1_verified', 'Layer 1 Verified'),
            ('layer2_verified', 'Layer 2 Verified'),
            ('rejected', 'Rejected')
        ],
        default='pending'
    )

    class Meta(ModelWithMetadata.Meta):
        ordering = ("slug",)
        app_label = "channel"
        permissions = (
            (
                ChannelPermissions.MANAGE_CHANNELS.codename,
                "Manage channels.",
            ),
        )

    def __str__(self):
        return self.slug
