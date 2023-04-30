from datetime import datetime

from django.shortcuts import render, redirect


from scheduler.send_email import welcome_email
from smart_emailApp.models import MyJobModel, ErrorReport
from .forms import *
from .models import User


from datetime import datetime

now = datetime.now()


def user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Check if email already exists in database
            if User.objects.filter(email=user.email).exists():
                # send_it(request, user.email, user.first_name, user.last_name)
                welcome_email(user.email, user.first_name, user.last_name)
                my_job = MyJobModel(name="New User Email Sent", decription="" + str(now))
                print("Email already exists")
                return redirect('user_created')  # redirect to a different page, or display an error message
            else:
                # If email does not exist, send the welcome email and save the user to database
                if welcome_email(user.email, user.first_name, user.last_name):
                    user.welcome_email = True
                    user.save()
                    my_job = MyJobModel(name="New User Email Sent", decription="" + str(now))
                    my_job.save()
                    print("Email Sent views.py")
                    return redirect('user_created')
                else:
                    print("Email was not sent")
                    err = ErrorReport(name = "Email Not Sent", decription= f"New User email failed to send for user {user.email} {user.first_name} at {now()}")
                    err.save()
    else:
        form = UserForm()


    return render(request, 'smartform/user_form.html', {'form': form})


def user_created(request):
    latest_user = User.objects.latest('created_at')
    context = {
        'first_name': latest_user.first_name,
        'last_name': latest_user.last_name,
    }
    return render(request, 'smartform/user_created.html', context=context)


def unsubscribe(request):
    email = request.GET.get('user-email') or ''
    user = User.objects.filter(email=email)
    user.update(subscribe_to_newsletter=False)
    user.save()

    print(email)
    # context = {'tasks': tasks}
    return render(request, 'smartform/unsubscribe_form.html')
