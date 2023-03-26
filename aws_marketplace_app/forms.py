from .models import Category, Posting, UserProfile, PostingImage

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm, HiddenInput


class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = "widgets/image_widget.html"


class ImageWidgetV2(forms.widgets.ClearableFileInput):
    template_name = "widgets/image_widget_v2.html"


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UpdateUserForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
        exclude = ("password", )

    def save(self, commit=True):
        user = super(UserChangeForm, self).save(commit=False)
        if commit:
            user.save()
        return user


class CategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(
            *args, **kwargs)
        self.fields['parent'].queryset = Category.objects.exclude(
            is_deleted=True)
        if self.instance.pk:
            query = self.fields['parent'].queryset
            self.fields['parent'].queryset = query.exclude(id=self.instance.id)

    class Meta:
        model = Category
        fields = ("name", "parent")


class PostingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PostingForm, self).__init__(
            *args, **kwargs)
        self.fields['category'].queryset = Category.objects.exclude(
            is_deleted=True)
        self.fields['is_draft'].widget = HiddenInput()

    class Meta:
        model = Posting
        fields = ("category", "title", "price", "description", "address", "postal_code", "manufacturer",
                  "model_name", "length_cm", "width_cm", "height_cm", "condition", "can_meetup", "can_deliver", "is_draft")


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ("display_image", "biography", "gender",
                  "address", "postal_code", "mobile_no")
        widgets = {"display_image": ImageWidget}


class PostingImageForm(forms.ModelForm):

    class Meta:
        model = PostingImage
        fields = ("image",)
        widgets = {"image": ImageWidgetV2}
