import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from Channel.models import Channel
from LibertyWave import settings
from Video.models import Video


# Video Views

@login_required
def video_index_view(request):
    # Get videos from all channels owned by the user
    videos = Video.objects.filter(channel__owner=request.user)
    return render(request, 'videos/index.html', {'videos': videos})


@login_required
def video_create_view(request, channel_id):
    user_channels = Channel.objects.filter(owner=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        thumbnail = request.FILES.get('thumbnail')
        channel_id = request.POST.get('channel')

        channel = get_object_or_404(Channel, id=channel_id)

        if channel.owner != request.user:
            raise PermissionDenied

        video = Video.objects.create(
            channel=channel,
            title=title,
            description=description,
            video_file=video_file,
            thumbnail=thumbnail
        )
        messages.success(request, "Video uploaded successfully")
        return redirect('video_show', video.id)

    # If channel_id is provided, preselect that channel
    initial_channel = None
    if channel_id:
        initial_channel = get_object_or_404(Channel, id=channel_id)
        if initial_channel.owner != request.user:
            raise PermissionDenied

    return render(request, 'videos/edit.html', {
        'user_channels': user_channels,
        'initial_channel': initial_channel
    })


@login_required
def video_show_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.increment_views()
    return render(request, 'videos/show.html', {'video': video})


@login_required
def video_edit_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user_channels = Channel.objects.filter(owner=request.user)

    if video.channel.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        video.title = request.POST.get('title')
        video.description = request.POST.get('description')
        video.channel = get_object_or_404(Channel, id=request.POST.get('channel'))

        if 'thumbnail' in request.FILES:
            video.thumbnail = request.FILES['thumbnail']

        if 'video_file' in request.FILES:
            video.video_file = request.FILES['video_file']

        video.save()
        messages.success(request, "Video updated successfully")
        return redirect('video_show', video.id)

    return render(request, 'videos/edit.html', {
        'video': video,
        'user_channels': user_channels
    })


@login_required
def protected_media(request, path):
    # Construct the full file path
    file_path = os.path.join(settings.PRIVATE_MEDIA_ROOT, path)

    # Check if file exists and user has permission
    if os.path.exists(file_path):
        # Here you can add additional permission checks
        # For example, check if user owns the video
        return FileResponse(open(file_path, 'rb'))
    raise Http404("File not found")
