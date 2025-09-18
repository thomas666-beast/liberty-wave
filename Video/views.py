import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.files import File
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from Channel.models import Channel
from LibertyWave import settings
from Video.models import Video
from Video.utils import generate_thumbnail_from_video


# Video Views

@login_required
def video_index_view(request):
    # Get videos from all channels owned by the user
    videos = Video.objects.filter(channel__owner=request.user)
    return render(request, 'videos/index.html', {'videos': videos})


@login_required
def video_create_view(request, channel_id=None):
    user_channels = Channel.objects.filter(owner=request.user)

    # If channel_id is provided, preselect that channel
    initial_channel = None
    if channel_id:
        initial_channel = get_object_or_404(Channel, id=channel_id)
        if initial_channel.owner != request.user:
            raise PermissionDenied

    if request.method == 'POST':
        # Handle AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                title = request.POST.get('title')
                description = request.POST.get('description')
                video_file = request.FILES.get('video_file')
                thumbnail = request.FILES.get('thumbnail')
                channel_id = request.POST.get('channel')

                channel = get_object_or_404(Channel, id=channel_id)

                if channel.owner != request.user:
                    return JsonResponse({'error': 'Permission denied'}, status=403)

                # Create video instance
                video = Video(
                    channel=channel,
                    title=title,
                    description=description,
                    video_file=video_file,
                    thumbnail=thumbnail
                )

                video.save()

                # Generate thumbnail from video if no thumbnail provided and video was uploaded
                if video_file and not thumbnail:
                    try:
                        thumbnail_path = generate_thumbnail_from_video(video.video_file.path)
                        with open(thumbnail_path, 'rb') as f:
                            from django.core.files import File
                            video.thumbnail.save(
                                f"thumbnail_{video.id}.jpg",
                                File(f),
                                save=True
                            )
                        # Clean up temporary file
                        os.remove(thumbnail_path)
                    except Exception as e:
                        # Log error but don't break the flow
                        print(f"Error generating thumbnail: {e}")

                # Return success with video ID
                return JsonResponse({
                    'success': True,
                    'video_id': video.id,
                    'redirect_url': reverse('video_show', kwargs={'video_id': video.id})
                })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        # Regular form submission (non-AJAX)
        else:
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

            # Generate thumbnail from video if no thumbnail provided and video was uploaded
            if video_file and not thumbnail:
                try:
                    thumbnail_path = generate_thumbnail_from_video(video.video_file.path)
                    with open(thumbnail_path, 'rb') as f:
                        from django.core.files import File
                        video.thumbnail.save(
                            f"thumbnail_{video.id}.jpg",
                            File(f),
                            save=True
                        )
                    # Clean up temporary file
                    os.remove(thumbnail_path)
                except Exception as e:
                    # Log error but don't break the flow
                    print(f"Error generating thumbnail: {e}")

            messages.success(request, "Video uploaded successfully")
            return redirect('video_show', video.id)

    return render(request, 'videos/edit.html', {
        'user_channels': user_channels,
        'initial_channel': initial_channel,
        'is_create': True  # Flag to indicate this is a create view
    })


@login_required
def video_edit_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    user_channels = Channel.objects.filter(owner=request.user)

    if video.channel.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        # Handle AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                video.title = request.POST.get('title')
                video.description = request.POST.get('description')
                video.channel = get_object_or_404(Channel, id=request.POST.get('channel'))

                # Handle thumbnail upload
                if 'thumbnail' in request.FILES:
                    video.thumbnail = request.FILES['thumbnail']

                # Handle video file upload
                video_file_uploaded = False
                if 'video_file' in request.FILES:
                    video.video_file = request.FILES['video_file']
                    video_file_uploaded = True

                video.save()

                # Generate thumbnail from video if no thumbnail provided and video was uploaded
                if video_file_uploaded and not video.thumbnail:
                    try:
                        thumbnail_path = generate_thumbnail_from_video(video.video_file.path)
                        with open(thumbnail_path, 'rb') as f:
                            from django.core.files import File
                            video.thumbnail.save(
                                f"thumbnail_{video.id}.jpg",
                                File(f),
                                save=True
                            )
                        # Clean up temporary file
                        os.remove(thumbnail_path)
                    except Exception as e:
                        # Log error but don't break the flow
                        print(f"Error generating thumbnail: {e}")

                # Return success with video ID
                return JsonResponse({
                    'success': True,
                    'video_id': video.id,
                    'redirect_url': reverse('video_show', kwargs={'video_id': video.id})
                })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        # Regular form submission (non-AJAX)
        else:
            video.title = request.POST.get('title')
            video.description = request.POST.get('description')
            video.channel = get_object_or_404(Channel, id=request.POST.get('channel'))

            if 'thumbnail' in request.FILES:
                video.thumbnail = request.FILES['thumbnail']

            video_file_uploaded = False
            if 'video_file' in request.FILES:
                video.video_file = request.FILES['video_file']
                video_file_uploaded = True

            video.save()

            # Generate thumbnail from video if no thumbnail provided and video was uploaded
            if video_file_uploaded and not video.thumbnail:
                try:
                    thumbnail_path = generate_thumbnail_from_video(video.video_file.path)
                    with open(thumbnail_path, 'rb') as f:
                        from django.core.files import File
                        video.thumbnail.save(
                            f"thumbnail_{video.id}.jpg",
                            File(f),
                            save=True
                        )
                    # Clean up temporary file
                    os.remove(thumbnail_path)
                except Exception as e:
                    # Log error but don't break the flow
                    print(f"Error generating thumbnail: {e}")

            messages.success(request, "Video updated successfully")
            return redirect('video_show', video.id)

    return render(request, 'videos/edit.html', {
        'video': video,
        'user_channels': user_channels,
        'is_create': False  # Flag to indicate this is an edit view
    })


@login_required
def video_show_view(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.increment_views()
    return render(request, 'videos/show.html', {'video': video})


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


def all_videos(request):
    search_query = request.GET.get('q', '')

    video_list = Video.objects.all().order_by('-created_at')

    if search_query:
        video_list = video_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    paginator = Paginator(video_list, 12)  # Show 12 videos per page
    page_number = request.GET.get('page')
    videos = paginator.get_page(page_number)

    return render(request, 'videos/all_videos.html', {
        'videos': videos,
        'search_query': search_query
    })

