from django.shortcuts import render, redirect
from django.http import HttpResponse
from store.models.product import Product
from store.models.category import Category
from store.models.customer import Customer
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from django.views import View


# print(make_password('1234'))
# print(
#     check_password('1234', 'pbkdf2_sha256$600000$1KdwI8FsHi1zehDOeHJw1k$GopCn89DdRlLl0P4yguktcANtvhCvr3F65GW+6djybU='))

# Create your views here.
class Index(View):

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1
            # cart[product]=1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart', request.session['cart'])
        return redirect('homepage')

    def get(self, request):
        # //func to serve index.html page
        products = None

        # print(product)
        # return render(request , 'orders/orders.html')
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        print('you are : ', request.session.get('email'))
        return render(request, 'index.html', data)
