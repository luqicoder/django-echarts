from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('showall/', views.showall),
    path('show/', views.show, name='show'),
    path('country/', views.show1, name='country'),
    path('school/', views.school, name='school'),
    path('school_detail/', views.school_detail, name='school_detail'),
    path('login_admin/', views.login_admin),
    path('admin/', views.admin),
    path('leader/', views.leader, name='leader'),
    path('young/', views.young, name='young'),
    path('addPerson/', views.addPerson, name='addPerson'),
    path('delPerson/', views.delPerson, name='delPerson'),
    path('updatePerson/', views.updatePerson, name='updatePerson'),
    path('query/', views.query, name='query'),
    path('up_excel/', views.up_excel, name='up_excel'),
    path('subjects/', views.subjects, name='subjects'),
    path('addsubjects/', views.addsubjects, name='addsubjects'),
    path('updatesubjects/', views.updatesubjects, name='updatesubjects'),
    path('delsubjects/', views.delsubjects, name='delsubjects'),
    path('querysubjects/', views.querysubjects, name='querysubjects'),
    path('sub_select_subject/', views.sub_select_subject, name='sub_select_subject'),
    #path('add/', views.admin)
]
