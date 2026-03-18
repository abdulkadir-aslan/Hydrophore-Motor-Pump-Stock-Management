from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        # Kullanıcının okundu ve okunmamış bildirimlerinin sayısı
        active_notifications_count = Notification.objects.filter( is_read=False).count()
        return {
            'active_notifications_count': active_notifications_count,
        }
    return {}