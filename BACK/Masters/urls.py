from django.urls import path
from .views import *

urlpatterns = [
    path('loginprofile',loginprofile,name='loginprofile'),
    path('get_loginer',get_loginer,name='get_loginer'),
     path('blogs/', blog_list_create,name='blog_list_create'),           # GET → list, POST → create
    path('blogs/<int:blog_id>/', blog_update_delete,name='blog_update_delete'),  # PUT → update, DELETE → delete
        path("skills/", skills_list_create,name="skills_list_create"),
    path("skills/<int:pk>/", skills_detail,name="skills_detail"),
       path('projects/', project_list_create, name='project-list-create'),
    path('projects/<int:pk>/', project_detail, name='project-detail'),
     path("profile/", profile, name="profile-api"),
    path("api/enquiry", enquiry, name="enquiry"),
    path('api/profiles/', all_profiles_json, name='all_profiles_json'),
    path("api/enquiries/", get_enquiries, name="get_enquiries"),
    path("api/document/<str:req_type>/<int:id>/", view_document,name='view_document'),
]
