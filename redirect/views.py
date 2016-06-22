from django.views.generic import DetailView
from django.conf import settings
from django.shortcuts import redirect

from .models import Redirect

class RedirectView(DetailView):
    queryset = Redirect.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        link = settings.LINK_BASE.format(obj.reference_id)

        return redirect(link)
