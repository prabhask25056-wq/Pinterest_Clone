import uuid

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from supabase import create_client

_client = None


def get_client():
    global _client
    if not _client:
        url = getattr(settings, 'SUPABASE_URL', '').strip()
        key = (
            getattr(settings, 'SUPABASE_KEY', '').strip()
            or getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '').strip()
            or getattr(settings, 'SUPABASE_ANON_KEY', '').strip()
            or getattr(settings, 'SUPABASE_PUBLISHABLE_KEY', '').strip()
        )

        if not url or not key:
            raise ImproperlyConfigured(
                'Supabase is not configured. Add SUPABASE_URL and a valid SUPABASE_KEY/SUPABASE_SERVICE_ROLE_KEY in your .env file.'
            )

        _client = create_client(url, key)
    return _client


def upload_image(file):
    bucket_name = getattr(settings, 'SUPABASE_BUCKET', 'pins').strip() or 'pins'
    ext = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else 'jpg'
    path = f'{uuid.uuid4().hex}.{ext}'
    bucket = get_client().storage.from_(bucket_name)
    bucket.upload(path=path, file=file.read(), file_options={'content-type': file.content_type})
    return bucket.get_public_url(path)