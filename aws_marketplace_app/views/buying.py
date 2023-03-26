from ..models import Posting, PostingImage, Wishlist, Order

from datetime import datetime

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateView, View


class BuyingWishlistTemplateView(TemplateView):
    template_name = 'buying/wishlist.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        wish_list = Wishlist.objects.filter(created_by=self.request.user).all()
        context['wish_list'] = wish_list
        return context


class BuyingWishlistUnlikeView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        posting = get_object_or_404(Posting, pk=pk)
        Wishlist.objects.filter(
            posting=pk, created_by=self.request.user).all().delete()
        messages.success(
            request, 'Listing has been deleted from your wishlist successfully.')
        return redirect('marketplace:buying_wishlist')


class BuyingOrdersTemplateView(TemplateView):
    template_name = 'buying/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        order_list = Order.objects.filter(created_by=self.request.user).all()
        context['order_list'] = order_list
        return context


class BuyingOrderDetailTemplateView(TemplateView):
    template_name = 'buying/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        order = get_object_or_404(Order, pk=kwargs['pk'])
        context['order'] = order
        images = PostingImage.objects.filter(posting=order.posting)
        context['images'] = images
        return context


class BuyingOrderCancelView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.OrderStatus.CANCELLED_BY_USER
        order.updated_at = datetime.now()
        order.updated_by = request.user
        order.save()
        messages.success(request, 'Order has been cancelled successfully.')
        return redirect('marketplace:buying_order_detail', pk)
