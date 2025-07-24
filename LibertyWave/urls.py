"""
URL configuration for LibertyWave project.

The `urlpatterns` list routes URLs to  For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from Channel.views import channel_index_view, channel_create_view, channel_show_view, channel_edit_view
from Dashboard.views import dashboard_view, custom_404, custom_500
from LibertyWave import settings
from Participant.views import register_view, login_view, logout_view, settings_view, password_change_view
from Video import views
from Video.views import video_index_view, video_create_view, video_show_view, video_edit_view, protected_media

handler404 = custom_404
handler500 = custom_500

urlpatterns = [
    # path('admin/', admin.site.urls),

    path('', login_view, name='login'),
    # Auth URLs
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('settings/', settings_view, name='settings'),
    path('settings/password/', password_change_view, name='password_change'),

    # Dashboard URL
    path('dashboard/', dashboard_view, name='dashboard'),

    # Channel URLs
    path('channels/', channel_index_view, name='channel_index'),
    path('channels/new/', channel_create_view, name='channel_create'),
    path('channels/<uuid:channel_id>/', channel_show_view, name='channel_show'),
    path('channels/<uuid:channel_id>/edit/', channel_edit_view, name='channel_edit'),

    # Video URLs
    path('videos/', video_index_view, name='video_index'),
    path('videos/new/', video_create_view, name='video_create'),
    path('videos/new/<uuid:channel_id>/', video_create_view, name='video_create_for_channel'),
    path('videos/<uuid:video_id>/', video_show_view, name='video_show'),
    path('videos/<uuid:video_id>/edit/', video_edit_view, name='video_edit'),

    path('all-videos/', views.all_videos, name='all_videos'),

    # Protected media URL pattern
    re_path(r'^protected/(?P<path>.*)$', protected_media, name='protected_media'),

    path('captcha/', include('captcha.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
