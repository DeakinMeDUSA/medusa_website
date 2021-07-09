
class SimpleMiddleware:
    """
    Fixes live preview of markdown, see https://github.com/agusmakmun/django-markdown-editor/issues/120
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if "martor" in request.path:
            setattr(request, "_dont_enforce_csrf_checks", True)

        response = self.get_response(request)

        return response
