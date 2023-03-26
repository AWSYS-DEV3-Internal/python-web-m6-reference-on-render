from . import views

from django.contrib.staticfiles.urls import static
from django.urls import path

app_name = 'marketplace'

urlpatterns = [
    path('', views.FrontHomeTemplateView.as_view(), name='index'),
    
    path('register', views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("password_reset", views.password_reset_request, name="password_reset"),

    path("user/profile", views.userProfileDetailView.as_view(), name="user_profile"),
    path("user/<int:pk>/profile", views.userSellerProfileDetailView.as_view(), name="user_seller_profile"),
    path("user/settings", views.userSettingsDetailView.as_view(), name="user_settings"),
    path("user/change-password", views.userChangePasswordDetailView.as_view(), name="user_change_password"),

    path('buying/browse', views.ListingBrowseAllTemplateView.as_view(), name='browse_all'),
    path('buying/browse/category/<int:pk>/', views.ListingBrowseByCategoryTemplateView.as_view(), name='browse_category'),
    path('buying/browse/listing/<int:pk>/', views.ListingBrowseDetailTemplateView.as_view(), name='browse_listing'),
    path('buying/browse/listing/<int:pk>/like', views.ListingAddWishlistView.as_view(), name='browse_listing_like'),
    path('buying/browse/listing/<int:pk>/unlike', views.ListingRemoveWishlistView.as_view(), name='browse_listing_unlike'),
    path('buying/browse/listing/<int:pk>/order', views.ListingAddOrderView.as_view(), name='browse_listing_order'),

    path('buying/wishlist', views.BuyingWishlistTemplateView.as_view(), name='buying_wishlist'),
    path('buying/wishlist/<int:pk>/unlike', views.BuyingWishlistUnlikeView.as_view(), name='buying_wishlist_unlike'),
    path('buying/orders', views.BuyingOrdersTemplateView.as_view(), name='buying_orders'),
    path('buying/order/<int:pk>', views.BuyingOrderDetailTemplateView.as_view(), name='buying_order_detail'),
    path('buying/order/<int:pk>/cancel', views.BuyingOrderCancelView.as_view(), name='buying_order_cancel'),

    path('selling/listings', views.SellerListingsListView.as_view(), name='selling_listings'),
    path('selling/listing/<int:pk>/', views.SellerListingDetailTemplateView.as_view(), name='selling_listing_detail'),
    path('selling/listing/create/', views.SellerListingCreateView.as_view(), name='selling_listing_create'),
    path('selling/listing/<int:pk>/update', views.SellerListingUpdateView.as_view(), name='selling_listing_update'),
    path('selling/listing/<int:pk>/delete', views.SellerListingDeleteView.as_view(), name='selling_listing_delete'),
    path('selling/listing/<int:pk>/publish', views.SellerListingPublishView.as_view(), name='selling_listing_publish'),
    path('selling/listing/<int:pk>/unpublish', views.SellerListingUnpublishView.as_view(), name='selling_listing_unpublish'),
    path('selling/listing/<int:pk>/reserve', views.SellerListingReserveView.as_view(), name='selling_listing_reserve'),
    path('selling/listing/<int:pk>/unreserve', views.SellerListingUnreserveView.as_view(), name='selling_listing_unreserve'),
    path('selling/listing/<int:pk>/sold', views.SellerListingSoldView.as_view(), name='selling_listing_sold'),
    path('selling/listing/<int:pk>/unsold', views.SellerListingUnsoldView.as_view(), name='selling_listing_unsold'),
    path('selling/fulfillments', views.SellerFulfillmentsTemplateView.as_view(), name='selling_fulfillments'),
    path('selling/fulfillment/<int:pk>/', views.SellerFulfillmentDetailsTemplateView.as_view(), name='selling_fulfillment_details'),
    path('selling/fulfillment/<int:pk>/pack', views.SellerFulfillmentPackView.as_view(), name='selling_fulfillment_pack'),
    path('selling/fulfillment/<int:pk>/ship', views.SellerFulfillmentShipView.as_view(), name='selling_fulfillment_ship'),
    path('selling/fulfillment/<int:pk>/deliver', views.SellerFulfillmentDeliverView.as_view(), name='selling_fulfillment_deliver'),
    path('selling/fulfillment/<int:pk>/cancel', views.SellerFulfillmentCancelView.as_view(), name='selling_fulfillment_cancel'),
]