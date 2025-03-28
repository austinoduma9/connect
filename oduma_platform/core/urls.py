from django.urls import path
from . import views
from .views import (
    register, login_view, logout_view, dashboard, profile,
    submit_idea, express_interest, event_list, send_connection_request, 
    manage_connection_request
)
from django.contrib.auth import views as auth_views
from .views import investor_proposals
from .views import profile_view
from .views import post_list, create_post, add_comment
from .views import edit_profile
from .views import user_posts
from django.conf.urls.static import static
from django.conf import settings


from .views import post_list 

from .views import contact



urlpatterns = [

##
    # path("app/", app_view, name="app"),


    path('', views.index, name='index'),
    path('app/', views.app_view, name='app'),
    path('about/', views.about, name='about'),
    path('networks/', views.networks, name='networks'),
    path('messages/', views.user_messages, name='messages'),
    path('events/', views.events, name='events'),
    path('services/', views.services, name='services'),
    path('jobs/', views.jobs, name='jobs'),
    path('notifications/', views.notifications, name='notifications'),


    path('search/', views.search, name='search'),

    path("my-posts/", user_posts, name="user_posts"),
    path("proposals/", investor_proposals, name="proposals"),

    ##contact form
    path("contact/", contact, name="contact"),

    #company suggestions
    # path("suggestions/", suggestions_view, name="suggestions"),
    path('edit_profile/', edit_profile, name='edit_profile'),

    #Profile views
    path("profile/<str:username>/", profile_view, name="profile_view"),

    #Posts and comments

    path("posts", post_list, name="post_list"),
    path("create_post/", create_post, name="create_post"),
    path("add-comment/<int:post_id>/", add_comment, name="add_comment"),

    # path('accounts/', include('django.contrib.auth.urls')),
     path("proposals/", investor_proposals, name="proposals"),

    # Authentication
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # User Dashboard & Profile
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/<str:username>/', profile, name='profile'),

    # Idea Management
    path('ideas/submit/', submit_idea, name='submit_idea'),
    path('ideas/<int:idea_id>/interest/', express_interest, name='express_interest'),

    # Event Management
    path('events/', event_list, name='event_list'),

    # Networking & Connections
    path('connect/send/<int:user_id>/', send_connection_request, name='send_connection_request'),
    path('connect/manage/<int:request_id>/<str:action>/', manage_connection_request, name='manage_connection_request'),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)