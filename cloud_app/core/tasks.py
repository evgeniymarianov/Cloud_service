from cloud_app.celery import app

from .service import create_report
from .models import User, Report

@app.task
def create_reports_task():
    print('!!!!!!!!!!!!!!task start')
    for user in User.objects.all():
        new_report = Report(text="New Report of user %s" % str(user.username))
        new_report.save()
        print(new_report)
        pass
