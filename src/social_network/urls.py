from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, ProfileViewSet, profile, register  
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi
from django.http import HttpResponseRedirect
from django.contrib import messages
from rest_framework.permissions import IsAdminUser

# START - code was developed with the help of documentation and other external research, please see referenced links. 

# handles validation if user is superuser/admin, this is for access to Swagger and ReDoc
# https://docs.djangoproject.com/en/3.2/topics/auth/default/#permissions
# https://www.django-rest-framework.org/api-guide/permissions/
class AdminAcessPermission(IsAdminUser):
    def has_permission(self, request, view):
        return request.user.is_superuser

# creates schema for Swagger and ReDoc
schema_view = get_schema_view(
    openapi.Info(
        title="Social Network Web Application",
        default_version="version 1",
        description="A user-friendly Web Application for users to express their ideas and communicate with friends in a secure manner.",
    ),
    public=True,
    permission_classes=[AdminAcessPermission],
)

# only admin can access Swagger, standard users will be denied access
# https://swagger.io
# https://github.com/swagger-api/swagger-ui
# https://github.com/swagger-api/swagger-editor
# https://swagger.io/tools/swaggerhub/
def admin_swagger(request, *args, **kwargs):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have authorization to view Swagger page.', extra_tags='error_for_swagger')
        return HttpResponseRedirect('/')
    return schema_view.with_ui('swagger', cache_timeout=0)(request, *args, **kwargs)

# only admin can access ReDoc, standard users will be denied access
# https://github.com/Redocly/redoc
# https://redocly.com
def admin_redoc(request, *args, **kwargs):
    if not request.user.is_superuser:
        messages.error(request, 'You do not have authorization to view ReDoc page.', extra_tags='error_for_redoc')
        return HttpResponseRedirect('/')
    return schema_view.with_ui('redoc', cache_timeout=0)(request, *args, **kwargs)


router = DefaultRouter()

router.register(r'profile', ProfileViewSet, basename='profile')
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [

    path('api/', include(router.urls)), 

    path('register/', register, name='register'),  
    path('profile/', profile, name='profile'), 

    path('admin/', admin.site.urls),

    # login/logout-related views
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('', user_views.index_redirect, name='index_redirect'),  
    path('', include('social.urls')),
    
    # performace measurements with Silk
    # https://github.com/jazzband/django-silk
    # https://pypi.org/project/django-silk/
    path('silk/', include('silk.urls', namespace='silk')),
    
    # API Documentation
    path('swagger/', admin_swagger, name='admin-swagger-ui'),
    path('redoc/', admin_redoc, name='admin-redoc-ui'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# END - code was developed with the help of documentation and other external research, please see referenced links. 


