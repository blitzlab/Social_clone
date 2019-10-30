from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse

class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("test"))
        return super().get(request, *args, **kwargs)

class TestPage(TemplateView):
    template_name = 'test.html'

class ThankPage(TemplateView):
    template_name = 'thanks.html'
