import threading

# Armazenamento por thread para garantir segurança em acessos simultâneos
_thread_locals = threading.local()

def get_current_request():
    return getattr(_thread_locals, 'request', None) 

class RequestInternalMiddleware:
    """Middleware to store the current request in thread local storage."""
    def __init__(self, get_response):
        self.get_response = get_response

# Armazena a request na thread
    def __call__(self, request):
        _thread_locals.request = request

# Capturar IP do ussuário na requisição
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            request.user_ip = x_forwarded_for.split(',')[0].strip()
        else:
            request.user_ip = request.META.get('REMOTE_ADDR')
        
        response = self.get_response(request)
        return response