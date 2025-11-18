from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from core.middleware import get_current_request, get_current_user
from core.models import AuditLog


def extract_ip(request):
    if not request:
        return None
    return request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')


def safe_user(user):
    return user if user and getattr(user, 'is_authenticated', False) else None


@receiver(post_save)
def model_post_save(sender, instance, created, **kwargs):
    # Evitar logging de nuestro modelo AuditLog
    if sender.__name__ == 'AuditLog':
        return

    app_label = getattr(sender._meta, 'app_label', '')
    if app_label not in ('clients', 'suppliers'):
        return

    request = get_current_request()
    user = get_current_user()
    ct = ContentType.objects.get_for_model(sender)

    AuditLog.objects.create(
        actor=safe_user(user),
        action='create' if created else 'update',
        content_type=ct,
        object_pk=str(getattr(instance, 'pk', None)),
        object_repr=str(instance)[:255],
        changes=None,
        ip_address=extract_ip(request),
        path=(getattr(request, 'path', None) if request else None),
        user_agent=(request.META.get('HTTP_USER_AGENT')[:512] if request and request.META.get('HTTP_USER_AGENT') else None),
    )


@receiver(pre_delete)
def model_pre_delete(sender, instance, **kwargs):
    if sender.__name__ == 'AuditLog':
        return

    app_label = getattr(sender._meta, 'app_label', '')
    if app_label not in ('clients', 'suppliers'):
        return

    request = get_current_request()
    user = get_current_user()
    ct = ContentType.objects.get_for_model(sender)

    AuditLog.objects.create(
        actor=safe_user(user),
        action='delete',
        content_type=ct,
        object_pk=str(getattr(instance, 'pk', None)),
        object_repr=str(instance)[:255],
        changes=None,
        ip_address=extract_ip(request),
        path=(getattr(request, 'path', None) if request else None),
        user_agent=(request.META.get('HTTP_USER_AGENT')[:512] if request and request.META.get('HTTP_USER_AGENT') else None),
    )


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    AuditLog.objects.create(
        actor=safe_user(user),
        action='login',
        content_type=None,
        object_pk=None,
        object_repr=str(user)[:255],
        ip_address=extract_ip(request),
        path=getattr(request, 'path', None),
        user_agent=(request.META.get('HTTP_USER_AGENT')[:512] if request and request.META.get('HTTP_USER_AGENT') else None),
    )


@receiver(user_logged_out)
def on_user_logged_out(sender, request, user, **kwargs):
    AuditLog.objects.create(
        actor=safe_user(user),
        action='logout',
        content_type=None,
        object_pk=None,
        object_repr=str(user)[:255] if user else None,
        ip_address=extract_ip(request),
        path=getattr(request, 'path', None) if request else None,
        user_agent=(request.META.get('HTTP_USER_AGENT')[:512] if request and request.META.get('HTTP_USER_AGENT') else None),
    )


@receiver(user_login_failed)
def on_user_login_failed(sender, credentials, request, **kwargs):
    AuditLog.objects.create(
        actor=None,
        action='login_failed',
        content_type=None,
        object_pk=None,
        object_repr=str(credentials)[:255],
        ip_address=extract_ip(request),
        path=getattr(request, 'path', None) if request else None,
        user_agent=(request.META.get('HTTP_USER_AGENT')[:512] if request and request.META.get('HTTP_USER_AGENT') else None),
    )
