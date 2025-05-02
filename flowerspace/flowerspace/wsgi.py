import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from settings import BASE_DIR

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flowerspace.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(BASE_DIR, 'staticfiles'))
app = application
