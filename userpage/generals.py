import time
from .models import *

def setting(request):
    try:
        setting_data = Setting.objects.last()
    except Exception:
        setting_data = None

    context = {
        'data': setting_data,
        'cache_buster': int(time.time()),
    }
    return context