from django.shortcuts import render, get_object_or_404
from pyexpat import features

from .models import Room

def room_list(request):
    rooms = Room.objects.all()

    room_type = request.GET.get('type', '')
    sort_by = request.GET.get('sort', '')

    if room_type:
        rooms = rooms.filter(room_type=room_type)

    if sort_by == 'price_asc':
        rooms = rooms.order_by('price_per_day')
    elif sort_by == 'price_desc':
        rooms = rooms.order_by('-price_per_day')
    elif sort_by == 'capacity':
        rooms = rooms.order_by('-capacity')

    room_types = Room.ROOM_TYPES

    context = {
        'rooms': rooms,
        'room_types': room_types,
        'selected_type': room_type,
        'selected_sort': sort_by,
    }
    return render(request, 'rooms/room_list.html', context)

def room_detail(request, slug):
    room = get_object_or_404(Room, slug=slug)
    return render(request, 'rooms/room_detail.html', {'room': room})

def index(request):
    features_rooms = Room.objects.filter(status='available')[:6]
    context = {'featured_rooms': features_rooms}
    return render(request, 'index.html', context)