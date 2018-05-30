from api.models import Customer, Store, Coupon, Has_coupon
from api.serializers import CustomerSerializer, StoreSerializer, CouponSerializer, HasCouponSerializer
from api.serializers import  CouponStoreSerializer, CustomerHasCouponStoreSerializer 
from api.serializers import CustomerNameSerializer, StampingSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.contrib.auth.views import *

from django.db import IntegrityError
# Create your views here.

class MyLoginView(LoginView):
    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        customer = Customer.objects.filter(user=self.request.user)
        if len(customer) == 1:  
            return JsonResponse({'is_customer': 'True'}, status=200)
        else :
            return JsonResponse({'is_customer': 'False'}, status=200)        

class MyLogoutView(LogoutView):
    next_page = '/'


# [TODO] CustomerSignUp must not be seen.
class CustomerSignUp(generics.CreateAPIView):
    """
    Create new Customer
    """
    serializer_class = CustomerSerializer

    def perform_create(self, serializer):
        new_user = User.objects.create_user(
                                 username=serializer.validated_data['user']['username'],
                                 password=serializer.validated_data['user']['password'])
        serializer.save(user = new_user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # [TODO] check wrong form 
        try:
            self.perform_create(serializer)
        except IntegrityError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response(serializer.data, status=status.HTTP_201_CREATED)
        return redirect('/')

# [TODO] StoreSignUp must not be seen.
class StoreSignUp(generics.CreateAPIView):
    """
    List all Store, or Create new Store
    """
    serializer_class = StoreSerializer

    def perform_create(self, serializer):
        new_user = User.objects.create_user(
                                 username=serializer.validated_data['user']['username'],
                                 password=serializer.validated_data['user']['password'])
        serializer.save(user = new_user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # [TODO] check wrong form 
        try:
            self.perform_create(serializer)
        except IntegrityError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response(serializer.data, status=status.HTTP_201_CREATED)
        return redirect('/')

class CouponPublishing(generics.CreateAPIView):
    '''
    request have to send customer account, cookie(login)
    '''
    serializer_class = CustomerNameSerializer

    def perform_create(self, serializer, request_store):
        new_coupon = Coupon.objects.create(
                                store=request_store,
                                stamp_count=0)
        customer_user = User.objects.get(username=serializer.validated_data['customer'])
        owner_customer = Customer.objects.get(user=customer_user)
        serializer.save(customer = owner_customer, coupon = new_coupon )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_store = Store.objects.get(user=request.user)
        # [TODO] check wrong form 
        try:
            self.perform_create(serializer, request_store)
        except IntegrityError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CouponListOfCustomer(generics.ListAPIView):
    '''
    request have to send cookie(login) by customer
    '''
    serializer_class = CustomerHasCouponStoreSerializer
    
    def get_queryset(self, *args, **kwargs):
        me = Customer.objects.get(user=self.request.user)
        my_coupon_list = Has_coupon.objects.filter(customer=me)
        return my_coupon_list

class CouponListOfStore(generics.ListAPIView):
    '''
    request have to send cookie(login) by store
    '''
    serializer_class = CustomerHasCouponStoreSerializer

    def get_queryset(self, *args, **kwargs):
        owner_store = Store.objects.get(user=self.request.user)
        all_coupon_list = Coupon.objects.filter(store=owner_store)
        coupon_list_of_store = Has_coupon.objects.filter(coupon__in=all_coupon_list)
        return coupon_list_of_store

class CouponStamping(generics.RetrieveUpdateAPIView):
    '''
    request have to send to /api/coupon_stamping/%coupon_id%
    '''
    serializer_class = StampingSerializer
    queryset = Coupon.objects.all()
    
    def perform_update(self, serializer):
        instance = self.get_object()
        old_data_serializer = self.get_serializer(instance)
        stamp = old_data_serializer.data["stamp_count"]
        serializer.save(stamp_count = stamp+1)
