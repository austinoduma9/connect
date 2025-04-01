from django.urls import path
from . import views
from .views import (
    register, login_view, logout_view
)
from django.contrib.auth import views as auth_views
from .views import inventor_page
from .views import edit_profile
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings


from .views import contact

from django.views.generic import TemplateView

from .views import profile_view

urlpatterns = [

##
    # path("admin/", app_view, name="admin"),

    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    # path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path('app/', views.app_view, name='app'),
    path('about/', views.about, name='about'),
    path('networks/', views.networks, name='networks'),
    path('messages/', views.user_messages, name='messages'),
    path('events/', views.events, name='events'),
    path('services/', views.services, name='services'),
    path('jobs/', views.jobs, name='jobs'),
    path('notifications/', views.notifications, name='notifications'),
    path('inventor_page/', views.inventor_page, name='inventor_page'),
    path('search/', views.search, name='search'),

    path("post_list/",views.post_list, name="post_list"),
    # path("proposals/", investor_proposals, name="proposals"),

    ##contact form
    path("contact/", contact, name="contact"),

    #company suggestions
    # path("suggestions/", suggestions_view, name="suggestions"),
    path('edit_profile/', edit_profile, name='edit_profile'),


    # Authentication
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path("create_project/", views.create_project, name="create_project"),

    path('profile/', profile_view, name='profile'),


    path('edit_project/<int:project_id>/', views.edit_project, name='edit_project'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)