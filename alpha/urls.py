from django.urls import path,reverse_lazy
from . import views


app_name='alpha'
urlpatterns = [
path('', views.index, name='index'),
path('createuser/',views.createuser.as_view(),name='createuser'),
path('indata/',views.indata),
path('dashboard/',views.dashboard.as_view(),name='dashboard'),
path('createwarehouse/',views.createwarehouse.as_view(success_url=reverse_lazy('alpha:dashboard')),name='createwarehouse'),
path('editwarehouse/<int:pk>/',views.editwarehouse.as_view(success_url=reverse_lazy('alpha:dashboard')),name='editwarehouse'),
path('deletewarehouse/<int:pk>/',views.deletewarehouse.as_view(success_url=reverse_lazy('alpha:dashboard')),name='deletewarehouse')
]
