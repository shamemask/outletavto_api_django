from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from main_api.views import Pr_Lg_table, ABCP_table, Rossko_table, Catalog

urlpatterns = [
      path('prlg/<str:endpoint>', Pr_Lg_table, name='prlg'),
      path('abcp/<str:endpoint>', ABCP_table, name='abcp'),
      path('rossko/<str:endpoint>', Rossko_table, name='rossko'),
      path('catalog', Catalog, name='catalog'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)