from ..models import Posting, UserProfile

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView


class userProfileDetailView(TemplateView):
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        posting_list = Posting.objects.filter(
            is_deleted=False, created_by=self.request.user)
        context['posting_list'] = posting_list
        return context


class userSellerProfileDetailView(TemplateView):
    template_name = 'user/seller-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=kwargs['pk'])
        context['seller_user'] = user
        posting_list = Posting.objects.filter(
            is_deleted=False, created_by=user)
        context['posting_list'] = posting_list
        return context
