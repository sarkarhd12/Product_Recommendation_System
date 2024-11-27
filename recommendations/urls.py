from django.urls import path
from .views import recommend_products, ProductListView,OrderListView, CreateOrderView

#urls for fetch the all the products,orders,place orders and recommend products
urlpatterns = [
    path('recommendations/<int:product_id>/', recommend_products, name='recommend-products'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('orders/create/', CreateOrderView.as_view(), name='create_order'),
]
