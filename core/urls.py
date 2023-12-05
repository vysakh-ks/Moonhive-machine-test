from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
   path('',views.index,name="index"),
   path('home/',views.home,name="home"),
   path('view_property/<int:prop>/',views.view_prop,name="view_prop"),
   path('tenant/',views.tenant_view,name="tenant"),
   path('logout/',views.logout_user,name="logout"),
   path('add_property/',views.add_property,name="add_property"),
   path('add_unit/<int:id>/',views.add_unit,name="add_unit"),
   path('allocate_tenant/<int:unit>/<int:prop>/',views.allocate_tenant,name="allocate_tenant"),
]