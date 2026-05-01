from django.shortcuts import render,redirect
import razorpay
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
from cart.models import Cart,Order,OrderItems
from django.contrib.auth.decorators import login_required
from cart.forms import OrderForm


# Create your views here.
@method_decorator(login_required,name='dispatch')
class AddToCart(View):
    def get(self,request,i):
        u=request.user
        p=Product.objects.get(id=i)
        try:
            c=Cart.objects.get(user=u,product=p)
            c.quantity+=1
            c.save()
        except:
            c=Cart(user=u,product=p,quantity=1)
            c.save()
        return redirect('cart:cartview')
@method_decorator(login_required,name='dispatch')
class CartView(View):
    def get(self,request):
        u=request.user
        sum=0
        c=Cart.objects.filter(user=u)
        for i in c:
            sum+=(i.quantity*i.product.price)

        context={'cart':c,'sum':sum}
        return render(request,'cart.html',context)
@method_decorator(login_required,name='dispatch')
class CartDecrement(View):
    def get(self,request,i):
        try:
            c=Cart.objects.get(id=i)
            if c.quantity>1:
             c.quantity-=1
             c.save()
            else:
                c.delete()
        except:
             pass
        return redirect('cart:cartview')
@method_decorator(login_required,name='dispatch')

class CartRemove(View):
    def get(self,request,i):
        try:
            c=Cart.objects.get(id=i)
            c.delete()
        except:
            pass
        return redirect('cart:cartview')
import uuid
@method_decorator(login_required,name='dispatch')
class Checkout(View):
    def post(self,request):
        form_instance=OrderForm(request.POST)
        if form_instance.is_valid():
            u=form_instance.save(commit=False)
            user=request.user
            u.user=user

            c=Cart.objects.filter(user=user)
            total=0
            for i in c:
                total+=i.quantity*i.product.price
                u.amount=total
                u.save()
            if(u.payment_method=="ONLINE"):
                    client=razorpay.Client(auth=('rzp_test_SfMluChWM311bz','MNuDxV964okSGmZSQPzLr7JA'))
                    response_payment=client.order.create({'amount':int(u.amount*100),'currency':'INR'})
                    print(response_payment)
                    id=response_payment['id']
                    u.order_id=id
                    u.save()
                    context={'payment':response_payment}
                    return render(request, 'payment.html', context)
            else:
               id=uuid.uuid4().hex[:14]
               i='order_COD'+id
               u.order_id=i
               u.is_ordered=True
               u.save()
               c=Cart.objects.filter(user=user)
               for i in c:
                   item=OrderItems.objects.create(order=u,product=i.product,quantity=i.quantity)
                   item.save()
               c.delete()
               return render(request,'payment.html')
    def get(self,request):
        form_instance=OrderForm()
        context={'form':form_instance}
        return render(request,'checkout.html',context)
@method_decorator(csrf_exempt,name='dispatch')
class PaymentSuccess(View):

    def post(self,request):
        response=request.POST
        print(response)
        id=response['razorpay_order_id']
        o=Order.objects.get(order_id=id)
        o.is_ordered=True
        o.save()

        c=Cart.objects.filter(user=o.user)
        for i in c:
            items=OrderItems.objects.create(order=o,product=i.product,quantity=i.quantity)
            items.save()

        c.delete()
        return render(request,'paymentsuccess.html')
@method_decorator(login_required,name='dispatch')
class OrderSummary(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'orders':o}
        return render(request,'summary.html',context)
