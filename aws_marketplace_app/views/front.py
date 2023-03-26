from django.shortcuts import redirect
from django.views.generic import TemplateView


class FrontHomeTemplateView(TemplateView):
    template_name = 'front/index.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/buying/browse')
        return super().dispatch(*args, **kwargs)
