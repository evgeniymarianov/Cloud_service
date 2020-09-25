from cloud_app.celery import app
from celery import shared_task

from .service import create_report
from .models import User, Report


@shared_task
def hello():
    print('Hello there!')


# @app.task
@shared_task
def create_report_task():
    print('!!!!!!!!!!!!!!task start')
    for user in User.objects.all():
        new_report = Report(text="New Report of user %s" % str(user.username))
        new_report.save()
        print(new_report)
        pass
