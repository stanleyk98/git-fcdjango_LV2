from django.shortcuts import render , redirect
from django.views.generic import FormView, ListView
from django.utils.decorators import method_decorator
from django.db import transaction
from fcuser.decorators import login_required
from .forms import RegisterForm
from .models import Order
from product.models import Product
from fcuser.models import Fcuser

# Create your views here.

# 주문등록 뷰

@method_decorator(login_required, name= 'dispatch')
class OrderCreate(FormView):
    #template_name = 'register_product.html'   
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        with transaction.atomic():
            # quan = form.data.get('quantity')
            prod = Product.objects.get(pk=form.data.get('product')) 
            # user = Fcuser.objects.get(email= self.request.session.get('user'))
            
            order = Order(
                quantity= form.data.get('quantity') ,
                product = prod ,
                fcuser = Fcuser.objects.get(email= self.request.session.get('user'))
            )
            order.save()
            prod.stock -= int(form.data.get('quantity'))
            prod.save()
        
        return super().form_valid(form)


    def form_invalid(self, form):
        return redirect('/product/' + str(form.data.get('product')))


    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({ 'request' : self.request})
        return kw



@method_decorator(login_required, name= 'dispatch')
class OrdertList(ListView): 
    #모델을 order 로 지정하면 모든 계정에서 주문한 정보까지 다 리스트업 함
    #model = Order
    template_name = 'order.html'
    context_object_name = 'order_list'

    #세션에서 로그인한 계정의 주문만 리스트업해야함
    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(fcuser__email=self.request.session.get('user'))
        return queryset
