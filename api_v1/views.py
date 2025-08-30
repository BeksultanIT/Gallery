from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from webapp.models import Photo, Album



@login_required
@require_POST
def add_photo_to_favorites(request, photo_id):
    try:
        photo = get_object_or_404(Photo, id=photo_id)
        if not photo.is_public:
            return JsonResponse({'success': False,'error': 'Нельзя добавить приватное фото в избранное'}, status=400)
        user = request.user
        if user in photo.favorited_by.all():
            return JsonResponse({'success': False, 'error': 'Фото уже в избранном'  }, status=400)
        photo.favorited_by.add(user)
        return JsonResponse({'success': True,'message': 'Фото добавлено в избранное','favorites_count': photo.favorites_count})
    except Exception as e:
        return JsonResponse({'success': False,'error': str(e)}, status=500)

@login_required
@require_POST
def remove_photo_from_favorites(request, photo_id):
    try:
        photo = get_object_or_404(Photo, id=photo_id)
        user = request.user
        if user not in photo.favorited_by.all():
            return JsonResponse({'success': False,'error': 'Фото не в избранном'}, status=400)
        photo.favorited_by.remove(user)
        return JsonResponse({'success': True,'message': 'Фото удалено из избранного','favorites_count': photo.favorites_count})
    except Exception as e:
        return JsonResponse({'success': False,'error': str(e)}, status=500)


@login_required
@require_POST
def add_album_to_favorites(request, album_id):
    try:
        album = get_object_or_404(Album, id=album_id)
        if not album.is_public:
            return JsonResponse({'success': False,'error': 'Нельзя добавить приватный альбом в избранное'}, status=400)
        user = request.user
        if user in album.favorited_by.all():
            return JsonResponse({'success': False,'error': 'Альбом уже в избранном'}, status=400)
        album.favorited_by.add(user)
        favorites_count = album.favorited_by.count()
        return JsonResponse({'success': True,'message': 'Альбом добавлен в избранное','favorites_count': favorites_count})
    except Exception as e:
        return JsonResponse({'success': False,'error': str(e)}, status=500)


@login_required
@require_POST
def remove_album_from_favorites(request, album_id):
    try:
        album = get_object_or_404(Album, id=album_id)
        user = request.user
        if user not in album.favorited_by.all():
            return JsonResponse({'success': False,'error': 'Альбом не в избранном'}, status=400)
        album.favorited_by.remove(user)
        favorites_count = album.favorited_by.count()
        return JsonResponse({'success': True, 'message': 'Альбом удален из избранного', 'favorites_count': favorites_count})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)