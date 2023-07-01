from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.loged, name="login"),
    path('csv', views.csv, name="csv"),
    path('survey', views.survey, name="survey"),
    path('master', views.master, name="master"),
    path('alljson', views.alljson, name="alljson"),
    path('jsonchart/<int:id>', views.jsonchart),
    path('edit/<int:id>', views.editmaster),
    path('start/<int:id>', views.start),
    path('delete/<str:act>/<int:id>', views.delete),
    path('editjson/<int:id>', views.editjson),
    path('json/<int:id>', views.json),
    path('detail/<int:id>', views.masterdetail),
    

]