import logging
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product, Order, Category,User
from .serializers import ProductSerializer, OrderSerializer
from collections import Counter
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status

logger = logging.getLogger(__name__)


#For fetching all the Product
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


#For fetching all the order
class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.all()  # Fetch all orders
        serializer = OrderSerializer(orders, many=True)  # Serialize the orders
        return Response(serializer.data, status=status.HTTP_200_OK)



#For Recomendation System
@api_view(['GET'])
def recommend_products(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # fetch orders containing the input product
    related_orders = Order.objects.filter(products=product).prefetch_related('products')

    if not related_orders:
        return Response({"message": "No related orders found."}, status=404)

    # collect related products, prioritizing same-category products
    same_category_products = []
    co_purchased_products = []

    for order in related_orders:
        for ordered_product in order.products.all():
            if ordered_product.id != product.id:
                if ordered_product.category == product.category:
                    same_category_products.append(ordered_product)
                else:
                    co_purchased_products.append(ordered_product)

    # count product occurrences in both lists
    product_counts_same_category = Counter(same_category_products)
    product_counts_co_purchased = Counter(co_purchased_products)

    # combine the results for a hybrid recommendation
    hybrid_recommendations = (
        list(product_counts_same_category.most_common(3)) +
        list(product_counts_co_purchased.most_common(2))
    )

    # extract unique products while preserving order
    unique_recommended_products = []
    seen_ids = set()
    for product, _ in hybrid_recommendations:
        if product.id not in seen_ids:
            unique_recommended_products.append(product)
            seen_ids.add(product.id)

    if not unique_recommended_products:
        return Response({"message": "No related products found."}, status=404)

    # serialize and return the recommended products
    serializer = ProductSerializer(unique_recommended_products, many=True)
    return Response(serializer.data)



#For Place a Order
class CreateOrderView(APIView):
    def post(self, request):
        # get the user id and product id's from the request body
        user_id = request.data.get('user')  # sser id should be in the request
        product_ids = request.data.get('products')  # product ids should be a list
        
        if not user_id or not product_ids:
            return Response(
                {"message": "User and products are required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # find the user by id
            user = User.objects.get(id=user_id)  

            # dind products by their ids
            products = Product.objects.filter(id__in=product_ids)  
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({"message": "One or more products not found."}, status=status.HTTP_404_NOT_FOUND)

        # create the order and associate the products with it
        order = Order.objects.create(user=user)  # create a new order for the user
        order.products.set(products)  # associate the products with the order
        order.save()

        # serialize the order data to return as a response
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)





