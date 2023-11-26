from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from main_api.views import Pr_Lg_table, Rossko_table, AsyncCatalog_table, AsyncCatalog
schema_view = get_schema_view(
   openapi.Info(
      title="Outletavto",
      default_version='v1',
      description="API работы с поставщиками запчастей",
      terms_of_service=None,
      contact=openapi.Contact(email="shamemask@ya.ru"),
      license=None,
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
      path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
      path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
      path('prlg/<str:endpoint>', Pr_Lg_table, name='prlg'),
      path('abcp/<str:endpoint>', AsyncCatalog_table.as_view(), name='abcp'),
      path('rossko/<str:endpoint>', Rossko_table, name='rossko'),
      path('catalog', AsyncCatalog.as_view(), name='catalog'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)