from ..models import Posting, Category, PostingImage, Wishlist, Order

from datetime import datetime

from django.contrib import messages
from django.forms.models import model_to_dict
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.base import View

from treelib import Tree

import json


def jsonConverter(o):
    if isinstance(o, datetime):
        return o.isoformat()


class ListingBrowseAllTemplateView(TemplateView):
    template_name = 'buying/browse.html'

    def get_category_tree(self):
        category_list = Category.objects.filter(is_deleted=False)
        tree = Tree()
        tree.create_node("root", float('-inf'))
        for category in category_list:
            category_dict = model_to_dict(category)
            if(category.parent == None):
                tree.create_node(category.id, category.id,
                                 parent=float('-inf'), data=category_dict)
            else:
                tree.create_node(category.id, category.id,
                                 parent=category.parent.id, data=category_dict)
        json_string = json.dumps(tree.to_dict(
            with_data=True), default=jsonConverter)
        return json.loads(json_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        posting_list = Posting.objects.filter(is_deleted=False)
        context['posting_list'] = Posting.objects.filter(
            is_deleted=False, is_draft=False)
        context['category_tree'] = self.get_category_tree()["root"]["children"]
        return context


class ListingBrowseByCategoryTemplateView(TemplateView):
    template_name = 'buying/browse.html'

    def get_category_root_tree(self):
        category_list = Category.objects.filter(is_deleted=False)
        tree = Tree()
        tree.create_node("root", float('-inf'))
        for category in category_list:
            category_dict = model_to_dict(category)
            if(category.parent == None):
                tree.create_node(category.id, category.id,
                                 parent=float('-inf'), data=category_dict)
            else:
                tree.create_node(category.id, category.id,
                                 parent=category.parent.id, data=category_dict)
        return tree

    def get_category_tree(self):
        category_list = Category.objects.filter(is_deleted=False)
        tree = Tree()
        tree.create_node("root", float('-inf'))
        for category in category_list:
            category_dict = model_to_dict(category)
            if(category.parent == None):
                tree.create_node(category.id, category.id,
                                 parent=float('-inf'), data=category_dict)
            else:
                tree.create_node(category.id, category.id,
                                 parent=category.parent.id, data=category_dict)
        json_string = json.dumps(tree.to_dict(
            with_data=True), default=jsonConverter)
        return json.loads(json_string)

    def get_category_subtree(self, category_id):
        tree = self.get_category_root_tree()
        sub_tree = tree.subtree(category_id)
        sub_tree_nodes = sub_tree.all_nodes()
        return list(node.tag for node in sub_tree_nodes)

    def get_category_path(self, category_id):
        tree = self.get_category_root_tree()
        path = tree.rsearch(category_id)
        node_path = []
        for nid in path:
            node = tree.get_node(nid)
            if(nid != float('-inf')):
                data = node.data
                if(nid == category_id):
                    data["current"] = True
                node_path.append(data)
        json_string = json.dumps(node_path[::-1], default=jsonConverter)
        return json.loads(json_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        target_categories = self.get_category_subtree(self.kwargs["pk"])
        category_crumbs = self.get_category_path(self.kwargs["pk"])
        context['category'] = Category.objects.get(pk=self.kwargs["pk"])
        context['category_crumbs'] = category_crumbs
        context['posting_list'] = Posting.objects.filter(
            is_deleted=False, is_draft=False, category__in=target_categories)
        context['category_tree'] = self.get_category_tree()["root"]["children"]
        return context


class ListingBrowseDetailTemplateView(TemplateView):
    template_name = 'buying/detail.html'

    def get_category_root_tree(self):
        category_list = Category.objects.filter(is_deleted=False)
        tree = Tree()
        tree.create_node("root", float('-inf'))
        for category in category_list:
            category_dict = model_to_dict(category)
            if(category.parent == None):
                tree.create_node(category.id, category.id,
                                 parent=float('-inf'), data=category_dict)
            else:
                tree.create_node(category.id, category.id,
                                 parent=category.parent.id, data=category_dict)
        return tree

    def get_category_path(self, category_id):
        tree = self.get_category_root_tree()
        path = tree.rsearch(category_id)
        node_path = []
        for nid in path:
            node = tree.get_node(nid)
            if(nid != float('-inf')):
                data = node.data
                node_path.append(data)
        json_string = json.dumps(node_path[::-1], default=jsonConverter)
        return json.loads(json_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        listing = Posting.objects.get(pk=self.kwargs["pk"])
        context['listing'] = listing
        images = PostingImage.objects.filter(posting=self.kwargs["pk"])
        context['images'] = images
        category_crumbs = self.get_category_path(listing.category.id)
        context['category_crumbs'] = category_crumbs
        context['user_wishlist'] = Wishlist.objects.filter(
            posting=self.kwargs["pk"], created_by=self.request.user).all()
        context['user_order'] = Order.objects.filter(
            posting=self.kwargs["pk"], created_by=self.request.user).all()
        return context


class ListingAddWishlistView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        posting = get_object_or_404(Posting, pk=pk)
        Wishlist.objects.filter(
            posting=pk, created_by=self.request.user).all().delete()
        wishlist = Wishlist()
        wishlist.posting = posting
        wishlist.created_by = self.request.user
        wishlist.created_at = datetime.now()
        wishlist.save()
        messages.success(
            request, 'Listing has been added to your wishlist successfully.')
        return redirect('marketplace:browse_listing', pk)


class ListingRemoveWishlistView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        posting = get_object_or_404(Posting, pk=pk)
        Wishlist.objects.filter(
            posting=pk, created_by=self.request.user).all().delete()
        messages.success(
            request, 'Listing has been deleted from your wishlist successfully.')
        return redirect('marketplace:browse_listing', pk)


class ListingAddOrderView(View):
    http_method_names = ['post']

    def post(self, request, pk):
        posting = get_object_or_404(Posting, pk=pk)
        order = Order()
        order.posting = posting
        order.created_by = self.request.user
        order.created_at = datetime.now()
        order.save()
        messages.success(
            request, 'Order has been placed successfully. Seller will contact you shortly.')
        return redirect('marketplace:browse_listing', pk)
