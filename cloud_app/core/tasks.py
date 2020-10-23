from cloud_app.celery import app
from celery import shared_task

from .service import create_report, CreateReportService, CreateDataService
from .models import User, Report, VirtualMachine, AdditionalHdd


@shared_task
def hello():
    print('Hello there!')


# @shared_task
# def create_data():
#     print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< create_data task start')
#     data = CreateDataService()


# @app.task
@shared_task
def create_reports_task():
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< create_data')
    #data = CreateDataService()
    print('!!!!!!!!!!!!!!create_reports_task start')
    reports = CreateReportService()
