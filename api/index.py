import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_blog.settings')

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel handler
def handler(request):
    try:
        return application(request)
    except Exception as e:
        from django.http import HttpResponse
        return HttpResponse(f"Error: {str(e)}", status=500)
