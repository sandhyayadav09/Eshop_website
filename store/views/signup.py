from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.views import View
from store.models.customer import Customer


class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)
        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            # return HttpResponse("Account Created")
            # return HttpResponse(request.POST.get('email'))  #Post returns a dictionary keys. using get we can
            # access value of keys
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value

            }
            return render(request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if not customer.first_name:
            error_message = "First name required !!"
        elif len(customer.first_name) < 4:
            error_message = "First name must be four character long or more!!"

        if not customer.last_name:
            error_message = "Last name required !!"
        elif len(customer.first_name) < 4:
            error_message = "Last name must be four character long or more!!"
        elif not customer.phone:
            error_message = "Phone number is required!!"
        elif len(customer.phone) < 10:
            error_message = "Valid phone number is required!!"
        elif len(customer.password) < 6:
            error_message = "Password must be 6 char long or more!!"
        elif customer.isExists():
            error_message = "Email address is already registered. Try with another one."
        return error_message
        # saving
