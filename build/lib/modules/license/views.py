from utils.base import PublicView


# Create your views here.


class LicensePageView(PublicView):
    template_name = "license/license.html"

    def get_context_data(self, **kwargs):
        context = super(LicensePageView, self).get_context_data(**kwargs)
        return context
