from django.conf import settings
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


def enforce_csrf(request):
    check = CSRFCheck(request)
    check.process_request(request)
    reason = check.process_view(request, None, (), {})
    print("this is reason", reason)
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

    # reason = CsrfViewMiddleware().process_view(request, None, (), {})
    # if reason:
    #     raise exceptions.PermissionDenied(f'CSRF Failed: {reason}')
    
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # header = self.get_header(request)

        # if header is None:
        #     return None

        print(request.COOKIES.get("csrftoken"))
        
        raw_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE_ACCESS"])

        if raw_token is None:
            return None


        validated_token = self.get_validated_token(raw_token)
        print('fdrrdfs))))))))))))))))')
        enforce_csrf(request)
        print('-----------------------', raw_token, validated_token)
    
        return self.get_user(validated_token), validated_token