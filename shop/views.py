
from django.contrib.auth import authenticate,login,logout
from shop.forms import SignUpForm,LoginForm
from django.shortcuts import render,redirect
from django.contrib import messages
from shop.models import Category,Product
from shop.forms import CategoryForm,ProductForm,StockForm

from django.views import View
class Categories(View):
    def get(self, request):
        c=Category.objects.all()
        context = {'categories': c}
        return render(request, "categories.html",context)
class Productdetail(View):
    def get(self, request,i):
        p=Product.objects.get(id=i)
        context={'product':p}
        return render(request, "productdetail.html",context)
class Products(View):
    def get(self, request,i):
        pname = Category.objects.get(id=i)
        context={'category':pname}
        print(pname)
        return render(request, "products.html",context)
class Addcategory(View):
    def get(self,request):
        form_instance=CategoryForm()
        return render(request, "addcategory.html", {'form': form_instance})
    def post(self,request):
        form_instance=CategoryForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
class Addproduct(View):
    def get(self,request):
        form_instance=ProductForm()
        return render(request, "addproduct.html", {'form': form_instance})
    def post(self,request):
        form_instance=ProductForm(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
class Register(View):
    def get(self, request):
        form_instance = SignUpForm()
        context = {'form': form_instance}
        return render(request, "register.html", context)

    def post(self, request):
        form_instance = SignUpForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return render(request, "categories.html")
class Login(View):
    def post(self, request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():
            data = form_instance.cleaned_data
            print(data)
            u = data['username']
            p = data['password']
            user = authenticate(username=u, password=p)
            if user:
                login(request, user)
                return render(request, "categories.html")
            else:
                messages.error(request, "Invalid credentials")
                return redirect('shop:login')

    def get(self, request):
        form_instance = LoginForm()
        context = {'form': form_instance}
        return render(request, "login.html", context)
class Logout(View):
    def get(self, request):
      logout(request)
      return render(request, "categories.html")
class Addstock(View):
    def post(self, request,i):
        p=Product.objects.get(id=i)
        # print(request.POST)
        # print(request.FILES)
        form_instance = StockForm(request.POST,request.FILES,instance=p)
        if (form_instance.is_valid()):
            form_instance.save()
            return redirect('shop:categories')

    def get(self, request, i):
          p = Product.objects.get(id=i)

          form_instance = StockForm(instance=p)
          context = {'form': form_instance}
          return render(request, "addstock.html", context)