from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,HttpResponseRedirect
from datetime import datetime
from .models import Property , Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMessage,send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from django.views import View
from django.views.generic import UpdateView
from django.contrib.auth import update_session_auth_hash
from .serializers import ProfileSerializer 
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            profile.birth_date= profile_form.data['birth_date']
            profile.gender= profile_form.data['gender']
            profile.profile_pic = request.FILES['profile_pic']
            profile.role= profile_form.data['role']
            profile.user = user
            profile.phone = profile_form.data['phone']
            profile.save()
            return redirect('login')
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'register.html', {'user_form':user_form,'profile_form':profile_form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('home')    
        else:
            message = "Wrong username and password"
        return render(request,'login.html',{'error': message })
    if request.method =="GET":
        return render(request,'login.html')

@login_required(login_url='/login/')
def home(request):
    properties = Property.objects.all().order_by('-created_at')
    profiles= Profile.objects.all().order_by('-created_at')
    profile = Profile.objects.get(user__username=request.user.username)
    if profile.role == 'Propertyowner':
        return render(request, 'home.html', {'properties':properties ,'profiles':profiles})
    else:
        return render(request, 'rentalhome.html', {'properties':properties ,'profiles':profiles})


@login_required(login_url='/login/')
def profile_page(request, profile_id):
    if request.method == "GET":
        profile= Profile.objects.get(pk=profile_id)
        properties = Property.objects.all().order_by('-created_at')
        return render(request, 'profile_page.html', {'properties':properties ,'profile':profile})

@login_required(login_url='/login/')
def profile_page_rental(request):
    if request.method == "GET":
        profiles= Profile.objects.all().order_by('-created_at')
        properties = Property.objects.all().order_by('-created_at')
        return render(request, 'profile_page_rental.html', {'properties':properties ,'profiles':profiles})



@login_required(login_url='/login/')
def property(request):
    if request.method == 'GET':
        return  render(request, 'property.html')
    if request.method == 'POST':
        title = request.POST['title']
        property_pic = request.FILES['property_pic']
        description = request.POST['description']
        address =request.POST['address']
        price=request.POST['price']
        sqft=request.POST['sqft']
        property= Property(title=title, property_pic=property_pic, description=description , address=address, price=price ,sqft=sqft , user=request.user)
        property.save()
        return redirect('home')

@login_required(login_url='/login/')
def delete_property(request,property_id):
    property_to_delete=Property.objects.get(id=property_id)
    property_to_delete.delete()
    return HttpResponseRedirect('/home/')

@login_required(login_url='/login/')
def property_detail(request,property_id):
    if request.method == "GET":
        property = Property.objects.get(pk=property_id)
        profile = Profile.objects.get(user__username=request.user.username)
        if profile.role == 'Propertyowner':
            return render(request, 'property_detail.html', {'property':property })
        else:
            return render(request, 'property_detail_rental.html', {'property':property })

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form })

class PropertyUpdateView(UpdateView):
    model = Property
    form_class = PropertyUpdateForm
    template_name = "property_update_form.html"
    #gar integer na ho to reverse_lazy use kar skte hai
    # success_url = reverse_lazy('property_detail')
    
    def get_success_url(self, **kwargs):
        return ('/artical/'+str(self.kwargs['pk'])+'/') 

class ForgotPassword(View):
    def get(self, request):
        # if request.method =="GET":
        return render(request,'forgot_password.html',)
    def post(self,request):
        try:
            if request.method == 'POST':
                email = request.POST['email']
                # try:
                user = User.objects.get(email=email)
                # except Exception as e:
                #     messages.error(self.request, 'Email Not Exist')
                #     return HttpResponseRedirect('/forgot-password/')
                password = User.objects.make_random_password(length=8, allowed_chars='123456789')
                user.set_password(password)
                user.save()
                body = "this is OTP "+password+""
                send_mail = EmailMessage("Forgot password",body,settings.FROM_EMAIL,to=[user.email])
                send_mail.send()
                messages.success(self.request, 'Check Password In Mail')
                return HttpResponseRedirect('/login/')
        except Exception as e:
                messages.error(request, e)
                return HttpResponseRedirect('/forgot_password/')

@login_required(login_url='/login/')
def apply_for_property(request,property_id):
    property = Property.objects.get(pk=property_id)
    property_title=property.title
    owner_email=property.user.email
    applier_contact_no=request.user.profile.phone
    user_profile= " http://127.0.0.1:8000/profile/ "
    body = "Hey, i am interested in your property.  ("+property_title+") "+ "contact me over here"+"( "+applier_contact_no+" )  , Click on the below link to check more detail or my profile" + user_profile
    send_mail = EmailMessage("APPLIED",body,settings.FROM_EMAIL,to=[owner_email])
    send_mail.send()
    messages.success(request, 'Applied successfully')
    return HttpResponseRedirect('/home/')
    


#1 way by class:-

class ProfileList(APIView):

    def get(self,request):
            profile = Profile.objects.all()
            serializer = ProfileSerializer(profile, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
         



# #2 way by method :-

# def profile_list(request):
#         profile = Profile.objects.all()
#         serializer = ProfileSerializer(profile, many=True)
#         return JsonResponse(serializer.data, safe=False)





# #3 way by api_view decorator

# from rest_framework.decorators import api_view

# @api_view()
# def profile_list(self):
#         # user_data = User.objects.all()
#         profile = Profile.objects.all()
#         serializer = ProfileSerializer(profile, many=True)
#         # serializer_user = UserSerializer(user_data, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)