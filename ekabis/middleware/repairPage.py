from django.shortcuts import redirect

from ekabis.models.Settings import Settings


class OnarimSayfasiMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if Settings.objects.get(key='maintenance').is_active:
            if not '/maintenance-page/' in request.path:
                return redirect('ekabis:view_repair_page')

        response = self.get_response(request)
        return response