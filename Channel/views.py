from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from Channel.models import Channel
from Video.models import Video

# Channel Views

@login_required
def channel_index_view(request):
    channels = Channel.objects.filter(owner=request.user)
    return render(request, 'channels/index.html', {'channels': channels})


@login_required
def channel_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        logo = request.FILES.get('logo')

        channel = Channel.objects.create(
            owner=request.user,
            name=name,
            description=description,
            logo=logo
        )
        messages.success(request, "Channel created successfully")
        return redirect('channel_show', channel.id)

    return render(request, 'channels/create.html')


@login_required
def channel_show_view(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)
    videos = Video.objects.filter(channel=channel)
    return render(request, 'channels/show.html', {
        'channel': channel,
        'videos': videos
    })


@login_required
def channel_edit_view(request, channel_id):
    channel = get_object_or_404(Channel, id=channel_id)

    if channel.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        channel.name = request.POST.get('name')
        channel.description = request.POST.get('description')

        if 'logo' in request.FILES:
            channel.logo = request.FILES['logo']

        channel.save()
        messages.success(request, "Channel updated successfully")
        return redirect('channel_show', channel.id)

    return render(request, 'channels/edit.html', {'channel': channel})

