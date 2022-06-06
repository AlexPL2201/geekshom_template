from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, FormView, LoginView
from django.core.mail import message, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from adminapp.mixin import BaseClassContextMixin, UserDispatchMixin
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from basket.models import Basket
from authapp.models import User
from django.conf import settings

# def login(request):

#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = auth.authenticate(username=username,password=password)
#             if user.is_active:
#                 auth.login(request,user)
#                 return HttpResponseRedirect(reverse('index'))
#         #     else:
#         #         print('Юзер не активный')
#         # # else:
#         # #     print(form.errors)

#     else:
#        form = UserLoginForm()
#     context = {
#         'title' : 'Gekshop | Авторизация',
#         'form': form
#     }
#     return render(request,'authapp/login.html',context)


class LoginGBView(LoginView, BaseClassContextMixin):
    title = 'Gekshop | Авторизация'
    form_class = UserLoginForm
    template_name = 'authapp/login.html'



class RegisterView(FormView, BaseClassContextMixin): # Закончил просмотр на 1:00:04
    model = User
    title = 'Gekshop | Регистрация'
    form_class = UserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('authapp:login')


    def post(self, request, *args, **kwargs):
        form = self. form_class(data=request.POST)
        if form.is_valid():
            user = form.save()
            if self.send_verify_link(user):
                messages.set_level(request, messages.SUCCESS)
                messages.success(request,'Вы успешно зарегистрировались')
                return HttpResponseRedirect(reverse('authapp:login'))
            else:
                messages.set_level(request, messages.ERROR)
                messages.error(request, form.errors)
        else:
            messages.set_level(request, messages.ERROR)
            messages.error(request, form.errors)
        context = {'form' : form}
        return render(request, 'authapp/register.html', context)


    def send_verify_link(self, user):
        verify_link = reverse('authapp:verify', args=[user.email, user.activation_key])
        subject = f'Для активации учётной записи {user.username} пройдите по ссылке'
        message = f'Для подтверждения учётной записи {user.username} на портале \n {settings.DOMAIN_NAME}{verify_link}'
        return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

    
    def verify(self, email, activate_key):
        try:
            user = User.objects.get(email=email)
            if user and user.activation_key == activate_key and not user.is_activation_key_expires():
                user.activation_key = ''
                user.activation_key_expires = None
                user.is_active = True
                user.save()
                auth.login(self, user)
            return render(self, 'authapp/verification.html')
        except Exception as e:
            return HttpResponseRedirect(reverse('index'))
        


# def register(request):

#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#         if form.is_valid():
#                 form.save()
#                 messages.success(request,'Вы успешно зарегистрировались')
#                 return HttpResponseRedirect(reverse('authapp:login'))
#         else:
#             print(form.errors)
#     else:
#         form = UserRegisterForm()
#     context = {
#         'title': 'Gekshop | Регистрация',
#         'form':form
#     }
#     return render(request, 'authapp/register.html', context)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user,data=request.POST,files=request.FILES)
#         if form.is_valid():
#                 form.save()
#         else:
#             print(form.errors)
#     user_select = request.user

#     baskets = Basket.objects.filter(user=user_select)

#     context = {
#         'title': 'Gekshop | Профайл',
#         'form':UserProfileForm(instance=user_select),
#         'baskets': baskets,
#     }

#     return render(request, 'authapp/profile.html', context)



class ProfileFromView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = User
    template_name = 'authapp/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('authapp:profile')
    title = 'Gekshop | Профайл'

    # def get_context_data(self, **kwargs):
    #     context = super(ProfileFromView, self).get_context_data()
    #     context['baskets'] = Basket.objects.filter(user=self.request.user)
    #     return context

    def form_valid(self, form):
        messages.set_level(self.request, messages.SUCCESS)
        messages.success(self.request, 'Вы успешно сохранили профиль!')
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_object(self, queryset=None):
        return User.objects.get(id=self.request.user.pk)
# def logout(request):
#     auth.logout(request)
#     return render(request,'mainapp/index.html')



class Logout(LogoutView):
    template_name = 'mainapp/index.html'