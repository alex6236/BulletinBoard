# from django.shortcuts import render, redirect

from django.views.generic import DetailView, UpdateView
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from allauth.account.views import SignupView, LoginView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Profile
from .forms import  ProfileUpdateForm, MailRegisterForm, UserUpdateForm, MailLoginForm

User = get_user_model()

class ProfileDetailView(DetailView):
    
    model = Profile
    context_object_name = 'profile'
    template_name = 'users/profile_detail.html'
    queryset = model.objects.all().select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        if self.object.avatar:
            context['has_avatar'] = True
        else:
            context['has_avatar'] = False
        return context


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/profile_edit.html'
    # success_url = reverse_lazy('ad_list')
    success_message = 'Профиль обновлён'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if form.is_valid() and user_form.is_valid():
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})


class MailRegisterView(SignupView):
    model = User
    form_class = MailRegisterForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('ad_list')
    
class MailLoginView(LoginView):
    model = User
    form_class = MailLoginForm
    template_name = 'account/login.html'
    success_url = reverse_lazy('ad_list')
    

