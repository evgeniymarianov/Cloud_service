from cloud_app.celery import app

from .service import create_report

@app.task
def create_report(request):
    pass
