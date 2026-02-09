# middleware.py in your Django app
class RemoveServerHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Method 1: Delete the Server header
        if 'Server' in response:
            del response['Server']
        # Method 2: Set empty value
        response['Server'] = ''
        return response