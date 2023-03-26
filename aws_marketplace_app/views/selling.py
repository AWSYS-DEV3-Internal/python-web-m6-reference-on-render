from ..forms import PostingForm, PostingImageForm
from ..models import Posting, PostingImage, Order

from datetime import datetime

from django.contrib import messages
from django.forms import modelformset_factory
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView


class SellerDashboardTemplateView(TemplateView):
    template_name = 'selling/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class SellerListingsListView(TemplateView):
    template_name = 'selling/listings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        posting_list = Posting.objects.filter(
            is_deleted=False, created_by=self.request.user.id)
        for posting in posting_list:
            posting.cover_images = posting.postingimage_set.filter(
                is_deleted=False).all()
        context['posting_list'] = posting_list
        return context


class SellerListingDetailTemplateView(TemplateView):
    template_name = 'selling/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        listing = Posting.objects.get(pk=self.kwargs["pk"])
        context['listing'] = listing
        images = PostingImage.objects.filter(
            posting=self.kwargs["pk"], is_deleted=False)
        context['images'] = images
        return context


class SellerListingCreateView(CreateView):
    template_name = 'selling/create.html'
    form_class = PostingForm
    image_formset = modelformset_factory(
        PostingImage, form=PostingImageForm, extra=10)

    def form_valid(self, form):
        posting = form.save(commit=False)
        posting.created_at = datetime.now()
        posting.created_by = self.request.user
        posting.save()

        messages.success(self.request, 'Listing has been created successfully.')

        formset = self.image_formset(
            self.request.POST, self.request.FILES, queryset=PostingImage.objects.none())
        if formset.is_valid():
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = PostingImage(posting=posting, image=image)
                    photo.created_at = datetime.now()
                    photo.created_by = self.request.user
                    photo.save()

        return redirect('marketplace:selling_listings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['formset'] = self.image_formset(
            queryset=PostingImage.objects.none())
        return context


class SellerListingUpdateView(UpdateView):
    template_name = 'selling/edit.html'
    model = Posting
    form_class = PostingForm
    image_formset = modelformset_factory(
        PostingImage, form=PostingImageForm, extra=10, can_delete=True)

    def form_valid(self, form):
        posting = form.save(commit=False)
        posting.updated_at = datetime.now()
        posting.updated_by = self.request.user
        posting.save()

        messages.success(self.request, 'Listing has been updated successfully.')

        formset = self.image_formset(self.request.POST, self.request.FILES,
                                     queryset=PostingImage.objects.filter(posting=posting, is_deleted=False))
        if formset.is_valid():
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = form['id']
                    is_delete = form['DELETE']
                    if(photo == None):
                        photo = PostingImage(posting=posting, image=image)
                        photo.created_at = datetime.now()
                        photo.created_by = self.request.user
                        photo.save()
                    elif(is_delete):
                        photo.is_deleted = True
                        photo.deleted_at = datetime.now()
                        photo.deleted_by = self.request.user
                        photo.save()
                    else:
                        photo.image = image
                        photo.updated_at = datetime.now()
                        photo.updated_by = self.request.user
                        photo.save()

        return redirect('marketplace:selling_listings')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['formset'] = self.image_formset(queryset=PostingImage.objects.filter(
            posting=context["posting"], is_deleted=False))
        return context


class SellerListingDeleteView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        posting = get_object_or_404(Posting, pk=pk)
        posting.is_deleted = True
        posting.deleted_at = datetime.now()
        posting.deleted_by = request.user
        posting.save()
        messages.success(request, 'Listing has been deleted successfully.')
        return redirect('marketplace:selling_listings')


class SellerListingPublishView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        posting = get_object_or_404(Posting, pk=pk)
        posting.is_draft = False
        posting.updated_at = datetime.now()
        posting.updated_by = request.user
        posting.save()
        messages.success(request, 'Listing has been published successfully.')
        return redirect('marketplace:selling_listing_detail', pk)


class SellerListingUnpublishView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        posting = get_object_or_404(Posting, pk=pk)
        posting.is_draft = True
        posting.updated_at = datetime.now()
        posting.updated_by = request.user
        posting.save()
        messages.success(request, 'Listing has been unpublished successfully.')
        return redirect('marketplace:selling_listing_detail', pk)


class SellerListingReserveView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        posting = get_object_or_404(Posting, pk=pk)
        posting.is_reserved = True
        posting.updated_at = datetime.now()
        posting.updated_by = request.user
        posting.save()
        messages.success(
            request, 'Listing has been marked as reserved successfully.')
        return redirect('marketplace:selling_listing_detail', pk)


class SellerListingUnreserveView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        posting = get_object_or_404(Posting, pk=pk)
        posting.is_reserved = False
        posting.updated_at = datetime.now()
        posting.updated_by = request.user
        posting.save()
        messages.success(
            request, 'Listing has been marked as not reserved successfully.')
        return redirect('marketplace:selling_listing_detail', pk)


class SellerListingSoldView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        posting = get_object_or_404(Posting, pk=pk)
        posting.is_sold = True
        posting.updated_at = datetime.now()
        posting.updated_by = request.user
        posting.save()
        messages.success(
            request, 'Listing has been marked as sold out successfully.')
        return redirect('marketplace:selling_listing_detail', pk)


class SellerListingUnsoldView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        posting = get_object_or_404(Posting, pk=pk)
        posting.is_sold = False
        posting.updated_at = datetime.now()
        posting.updated_by = request.user
        posting.save()
        messages.success(
            request, 'Listing has been marked as not sold out successfully.')
        return redirect('marketplace:selling_listing_detail', pk)


class SellerFulfillmentsTemplateView(TemplateView):
    template_name = 'selling/fulfillments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        order_list = Order.objects.filter(
            posting__created_by=self.request.user)
        context['order_list'] = order_list
        return context


class SellerFulfillmentDetailsTemplateView(TemplateView):
    template_name = 'selling/fulfillment_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        order = get_object_or_404(Order, pk=kwargs['pk'])
        context['order'] = order
        images = PostingImage.objects.filter(
            posting=order.posting, is_deleted=False)
        context['images'] = images
        return context


class SellerFulfillmentPackView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.OrderStatus.PACKED
        order.updated_at = datetime.now()
        order.updated_by = request.user
        order.save()
        messages.success(
            request, 'Order has been changed to packed status successfully.')
        return redirect('marketplace:selling_fulfillment_details', pk)


class SellerFulfillmentShipView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.OrderStatus.SHIPPED
        order.updated_at = datetime.now()
        order.updated_by = request.user
        order.save()
        messages.success(
            request, 'Order has been changed to shipped status successfully.')
        return redirect('marketplace:selling_fulfillment_details', pk)


class SellerFulfillmentDeliverView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.OrderStatus.DELIVERED
        order.updated_at = datetime.now()
        order.updated_by = request.user
        order.save()
        messages.success(
            request, 'Order has been changed to delivered status successfully.')
        return redirect('marketplace:selling_fulfillment_details', pk)


class SellerFulfillmentCancelView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.OrderStatus.CANCELLED_BY_SELLER
        order.updated_at = datetime.now()
        order.updated_by = request.user
        order.save()
        messages.success(
            request, 'Order has been changed to cancelled by seller status successfully.')
        return redirect('marketplace:selling_fulfillment_details', pk)
