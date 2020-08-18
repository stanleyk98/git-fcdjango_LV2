from django.shortcuts import render
from django.views.generic import ListView, FormView, DeleteView
from django.utils.decorators import method_decorator
from rest_framework import generics , mixins

from fcuser.decorators import admin_required
from .serializers import ProductSerializer
from .models import Product
from .forms import RegisterForm
from order.forms import RegisterForm as OrderForm

# 상품리스트뷰 (rest framework 사용)
# mixins 에서 리스트모델을 가져오기

class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


# 상품디테일 뷰 (rest framework 사용)
# mixins 에서 리스트모델 대신 retrieve 모델을 가져오기 

class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# 상품 리스트 뷰

class ProductList(ListView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product_list'

# 상품 등록 뷰

@method_decorator(admin_required, name= 'dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        product = Product(
            name=form.data.get('name') , 
            price=form.data.get('price') , 
            description=form.data.get('description'), 
            stock=form.data.get('stock')
        )

        product.save()
        return super().form_valid(form)

# 상품 디테일 뷰
 

class ProductDetail(DeleteView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
    context_object_name = 'product'

    # 디테일뷰에 주문하기 폼 추가하기
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderForm(self.request)
        return context
