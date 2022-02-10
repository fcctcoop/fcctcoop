from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

app_name = 'mmaptsp2'
urlpatterns = [
    path('', views.index, name='index'),    
    path('loadclient', views.loadclient, name='loadclient'),
    path('search', views.search, name='search'),
    path('searchclient',views.searchclient, name='searchclient'),
    path('<int:profile_id>/addmmap', views.addmmap, name='addmmap'),
    path('<int:profile_id>/mmapdetail/',views.mmapdetail, name='mmapdetail'),
    path('<int:mmap_id>/mmapedit/',views.mmapedit, name='mmapedit'),
    path('<int:mmap_id>/processmmapedit/',views.processmmapedit, name='processmmapedit'),
    path('processaddmmap', views.processaddmmap, name='processaddmmap'),
    path('filterby', views.filterby, name='filterby'),
    path('processfilterby', views.processfilterby, name='processfilterby'),
    path('exportdata/<str:exporttype>',views.exportdata, name='exportdata'),
    path('csv-upload/',views.csv_upload, name='csv_upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)