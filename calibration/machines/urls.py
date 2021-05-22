from django.conf.urls import url,include
from .views import MachinesCreateView,MachineListApi,MachinesRetrieveAPIView,MachinesUpdateAPIView,MachineDeleteView
from django.urls import path

app_name='machines'
urlpatterns = [
    path('create',MachinesCreateView.as_view()),
    path('list',MachineListApi.as_view()),
    path('<int:pk>/detail',MachinesRetrieveAPIView.as_view()),
    path('update',MachinesUpdateAPIView.as_view()),
    path('<int:id>/delete',MachineDeleteView.as_view())

]
