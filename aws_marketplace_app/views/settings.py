from ..forms import UserProfileForm, UpdateUserForm
from ..models import UserProfile

from datetime import datetime

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect
from django.views.generic.base import TemplateView


class userSettingsDetailView(TemplateView):
    template_name = 'user/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        try:
            user_profile = UserProfile.objects.get(pk=self.request.user.id)
        except:
            user_profile = None
        context['user_profile'] = user_profile
        profile_form = UserProfileForm(
            self.request.POST or None, instance=user_profile)
        profile_form.user = self.request.user
        context['profile_form'] = profile_form
        user_form = UpdateUserForm(
            self.request.POST or None, instance=self.request.user)
        context['user_form'] = user_form
        return context

    def post(self, request):
        user_form = UpdateUserForm(request.POST or None, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            try:
                user_profile = UserProfile.objects.get(pk=request.user.id)
                profile_form = UserProfileForm(
                    request.POST or None, request.FILES, instance=user_profile)
                if profile_form.is_valid():
                    user_profile = profile_form.save(commit=False)
                    user_profile.user = request.user
                    user_profile.updated_at = datetime.now()
                    user_profile.updated_by = request.user
                    user_profile.save()
                    messages.success(
                        request, 'User profile has been updated successfully.')
                    return redirect('marketplace:user_settings')
                return self.get(self, request)
            except:
                user_profile = None
                profile_form = UserProfileForm(
                    request.POST or None, request.FILES, instance=user_profile)
                if profile_form.is_valid():
                    user_profile = profile_form.save(commit=False)
                    user_profile.user = request.user
                    user_profile.created_at = datetime.now()
                    user_profile.created_by = request.user
                    user_profile.updated_at = datetime.now()
                    user_profile.updated_by = request.user
                    user_profile.save()
                    messages.success(
                        request, 'User profile has been updated successfully.')
                    return redirect('marketplace:user_settings')
                return self.get(self, request)
        return self.get(self, request)


class userChangePasswordDetailView(TemplateView):
    template_name = 'user/change-password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        password_change_form = PasswordChangeForm(
            self.request.user, self.request.POST or None)
        context['password_change_form'] = password_change_form
        return context

    def post(self, request):
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated.')
            return redirect('marketplace:user_change_password')
        return self.get(self, request)
