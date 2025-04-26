from django.urls import path, include
from . import views

app_name = "shop"

management_patterns = [
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('add/', views.CreateProductView.as_view(), name='product_add'),
    path('update/<int:pk>/', views.UpdateProductView.as_view(), name='product_update'),
    path('order/all/', views.AdminOrderManagementView.as_view(), name='order_all'),
    path('order/update/<int:pk>/', views.AdminOrderUpdateView.as_view(), name='order_update'),
]

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='product_list'),
    path('manage/', include(management_patterns)),
    path('cart/', views.CartManagementView.as_view(), name='cart'),
    path('cart/clear/', views.CartManagementView.as_view(), name='cart_clear'),
    path('cart/delete/<int:product_id>/', views.CartItemDeleteView.as_view(), name='cart_delete'),
    path('order/', views.ClientOrderManagementView.as_view(), name='order'),
    path('details/<slug:category_slug>/<slug:product_slug>/', views.ProductDetailsView.as_view(), name='product_details'),
    path('rate/<int:id>/', views.ToggleProductRatingView.as_view(), name='toggle_product_rating'),
    path('comment/<int:product_id>/', views.ProductCommentView.as_view(), name='toggle_product_comment'),
    path('<slug:category_slug>/', views.ProductsListView.as_view(), name='category_filter')
]