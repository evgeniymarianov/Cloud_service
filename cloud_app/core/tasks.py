from cloud_app.celery import app

from .service import create_report

@app.task
def create_report_task(user_id):
    print('!!!!!!!!!!!!!!task')
    create_report(user_id)
    pass
