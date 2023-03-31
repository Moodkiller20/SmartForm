from django.apps import AppConfig




class SmartEmailappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "smart_emailApp"

    def ready(self):
        from apscheduler.schedulers.background import BackgroundScheduler
        from django_apscheduler.jobstores import DjangoJobStore, register_events
        from scheduler.scheduler import Start

        from scheduler.tasks_scheduler import check_for_task, update_model
        # scheduler = BackgroundScheduler()
        # scheduler.add_jobstore(DjangoJobStore(), "default")
        # scheduler.add_job(check_for_task, 'interval', seconds=50, name="Check_for_tasks")
        # register_events(scheduler)
        # scheduler.start()

        check_for_task()
        #tart()
        #update_model(job)


