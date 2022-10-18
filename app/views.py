from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import customer, cart, product,orderplaced
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q      
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
      def get(self,request):
            topwears=product.objects.filter(category='TW')
            bottomwears=product.objects.filter(category = 'BW')
            mobiles=product.objects.filter(category='M')
            return render (request , 'app/home.html',{
            'topwear':topwears ,'bottomwears':bottomwears,
            'mobiles':mobiles
      })            






class productDetailView(View):
      def get(self,request,pk):
            product1=product.objects.get(pk=pk)
            item_already_in_cart1=False
            if request.user.is_authenticated:
               item_already_in_cart1=cart.objects.filter(Q(product=product1.id)&Q(user=request.user)).exists()
            return render(request,'app/productdetail.html',
            {'product':product1,'item_already_in_cart1':item_already_in_cart1})

@login_required
def add_to_cart(request):
      user=request.user
      product_id= request.GET.get('prod_id')
      product1= product.objects.get(id=product_id)
      cart(user=user,product=product1).save()
      print(product1)
      return redirect('/cart')

@login_required
def show_cart(request):
      if request.user.is_authenticated:
            user =request.user
            cart1 =cart.objects.filter(user= user)
            print(cart1)
            amount =0.0
            shipping_amount=70.0
            total_amount =0.0
            cart_product=[p for p in cart.objects.all() if p.user==user]
            print(cart_product)
      if cart_product:
            for p in cart_product:
                  tempamount = (p.quantity* p.product.discount_price)
                  amount += tempamount 
                  totalamount = amount + shipping_amount 

            return render(request, 'app/addtocart.html',{'carts':cart1,'totalamount':totalamount ,'amount':amount})
      else:
            return render(request,'app/empty.html')


def plus_cart(request):
      if request.method == 'GET':
           prod_id = request.GET['prod_id']
      #      print(prod_id)
           c=cart.objects.get(Q(product=prod_id) & Q(user=request.user))
           c.quantity+=1
           c.save()
           amount =0.0
           shipping_amount=70.0
           cart_product=[p for p in cart.objects.all() if p.user == request.user]
           for  p in cart_product:
                  tempamount = (p.quantity* p.product.discount_price)
                  amount += tempamount 
            
           data={
             'quantity' :  c.quantity,
             'amount':  amount,
             'totalamount': amount+shipping_amount

           }
           return JsonResponse(data)

def minus_cart(request):
      if request.method == 'GET':
           prod_id = request.GET['prod_id']
           c=cart.objects.get(Q(product=prod_id) & Q(user=request.user))
           c.quantity-=1
           c.save()
           amount =0.0
           shipping_amount=70.0
           cart_product=[p for p in cart.objects.all() if p.user == request.user]
           for  p in cart_product:
                  tempamount = (p.quantity* p.product.discount_price)
                  amount += tempamount 
            
           data={
                  'amount':  amount,
                  'totalamount':amount+shipping_amount

           }
           return JsonResponse(data)

def remove_cart(request):
      if request.method == 'GET':
           prod_id = request.GET['prod_id']
           c=cart.objects.get(Q(product=prod_id) & Q(user=request.user))
           c.delete()
           amount =0.0
           shipping_amount=70.0
           cart_product=[p for p in cart.objects.all() if p.user == request.user]
           for  p in cart_product:
                  tempamount = (p.quantity* p.product.discount_price)
                  amount += tempamount 
            
           data={
             'amount':  amount,
             'totalamount':  amount + shipping_amount 

             }  
           return JsonResponse(data)


def buy_now(request):
      return render(request, 'app/buynow.html')



def address(request):
      add= customer.objects.filter(user=request.user)
      return render( request, 'app/address.html',{'add': add,'active' :'btn-primary'})
@login_required
def orders(request):
     op=orderplaced.objects.filter(user=request.user)
     return render(request, 'app/orders.html',{'order_placed':op})


# def mobile(request ,data=None):
#       if data == None :
#         mobiles =product.objects.filter(category='M')
#       elif  data   =='Redmi' or data =='Samsung'  :
#          mobiles  =product.objects.filter(category='M').filter(brand=data)
#       return  render(request , 'app/mobile.html',{'mobiles': mobiles})

class CustomerRegistrationView(View):
      def get(self ,request):
              form = CustomerRegistrationForm( )
              return render(request ,'app/customerregistration.html',{'form':form})
      def post(self,request):
            form=CustomerRegistrationForm(request.POST)
            if form.is_valid():
                  messages.success(request, 'congratulations!! registed successfully')
                  form.save()
            return render(request ,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):
      user= request.user
      add = customer.objects.filter(user=user)
      cart_items=cart.objects.filter(user=user)
      amount =0.0
      shipping_amount=70.0
      totalamount=0.0
      cart_product=[p for p in cart.objects.all() if p.user == request.user]
      if cart_product:
          for  p in cart_product:
                  tempamount = (p.quantity* p.product.discount_price)
                  amount += tempamount 
          totalamount=amount+shipping_amount 
      return render(request, 'app/checkout.html',{'add':add ,'cart_items':cart_items,'totalamount':totalamount}
      )


@login_required
def payment_done(request):
      user= request.user
      custid=request.GET.get('custid')
      customer1= customer.objects.get(id=custid)
      cart1= cart.objects.filter(user=user)
      for c in cart1:
            orderplaced(user=user,customer=customer1,product=c.product,quantity=c.quantity).save()
            c.delete()
      return redirect("orders")
            


@method_decorator(login_required,name='dispatch')
class ProfileView(View):
      def get(self,request):
            form= CustomerProfileForm()
            return render (request, 'app/profile.html',{'form':form, 'active' :'btn-primary'})
      def post(self,request):
            form=CustomerProfileForm(request.POST)
            if form.is_valid():
                  usr=request.user
                  name= form.cleaned_data['name']
                  locality= form.cleaned_data['locality']
                  city= form.cleaned_data['city']
                  state= form.cleaned_data['state']
                  zipcode= form.cleaned_data['zipcode']
                  reg= customer(user=usr ,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
                  reg.save()
                  messages.success(request,"contratulations!!profile updated sucefully")
                  return render(request, 'app/profile.html',{'form':form,'active' :'btn-primary'})
