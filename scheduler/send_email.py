from SmartForm import settings
from smart_emailApp.models import Emails, EmailTask
import ast

def send_once_email( email):
    # send a confirmation mail
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email,]

    subject, from_email, to = 'NewsLetter Subscription', email_from, email

    context = {'first_name':"ELG-Fireamrs Member",
               'last_name':"",
               'body': 'Just testing water maybe this will work but it may not work'}

    message_html = render_to_string('email_templates/thankyou.html', context)


    email_message = EmailMessage(subject, '', from_email, recipient_list)
    email_message.content_subtype = "html"
    email_message.body = message_html
    email_message.send()


    print("Email was Sent!!")
    return True

def welcome_email(email, first_name, last_name):
    try:
        # send a confirmation mail
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]

        subject, from_email, to = 'NewsLetter Subscription', email_from, email

        context = {'first_name':first_name,
                   'last_name':last_name,
                   'body': 'Just testing water maybe this will work but it may not work'}

        message_html = render_to_string('email_templates/thankyou.html', context)
        email_message = EmailMessage(subject, '', from_email, recipient_list)
        email_message.content_subtype = "html"
        email_message.body = message_html
        email_message.send()

        print("Email was Sent!!################################")
        return True
    except:
        return False

def request_review(email, first_name):
    try:
        # send a confirmation mail
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]

        subject, from_email, to = 'ELG-Community', email_from, email

        context = {'first_name':first_name,

                   }

        message_html = render_to_string('email_templates/request_review.html', context)
        email_message = EmailMessage(subject, '', from_email, recipient_list)
        email_message.content_subtype = "html"
        email_message.body = message_html
        email_message.send()

        print("Email was Sent!!################################")

        return True
    except:
        return False

from django.core.mail import EmailMessage
from django.conf import settings

# def buildEmail(email_task_id, email_id):
#     print("Built Email is running")
#     email_task = EmailTask.objects.get(id=email_task_id)
#     email_s = Emails.objects.get(id=email_id)
#     email_from = settings.EMAIL_HOST_USER
#
#     # convert email_task.recipients to a list, because the outputted data from the database is a string of emails.
#     email_list = ast.literal_eval(email_task.recipients)
#     print(email_list)
#
#     subject, from_email = email_s.subject, email_from
#
#     context = {}
#     picture_urls = []
#
#     if email_s.product1_image:
#         picture_urls.append(email_s.product1_image.url)
#     if email_s.product2_image:
#         picture_urls.append(email_s.product2_image.url)
#     if email_s.product3_image:
#         picture_urls.append(email_s.product3_image.url)
#     if email_s.product4_image:
#         picture_urls.append(email_s.product4_image.url)
#
#     template_name = ""
#
#     if email_s.emailtype == "Store News":
#         context = {'receiver': "ELG-Firearms Member", 'emails': email_s}
#         template_name = "storesnews.html"
#
#     elif email_s.emailtype == "Promotional":
#         context = {'receiver': "ELG-Firearms Member", "emails": email_s}
#         template_name = "new4items.html"
#
#     elif email_s.emailtype == "Seasonal Sales":
#         context = {'receiver': "ELG-Firearms Member", 'emails': email_s}
#         template_name = "season_specials.html"
#
#     message_html = render_to_string(f'email_templates/{template_name}', context)
#
#     for recipient in email_list:
#         email_message = EmailMessage(subject, message_html, from_email, [recipient])
#         email_message.content_subtype = "html"
#         for i, picture_url in enumerate(picture_urls):
#             picture_tag = f'<img src="{picture_url}" alt="Picture {i+1}" />'
#             message_html = message_html.replace(f'{{{{ picture{i+1}_tag }}}}', picture_tag)
#         email_message.body = message_html
#         email_message.send()
#
#     print("Built email was sent! Email was Sent!!")
#     return True



from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from smart_emailApp.models import Emails  # Assuming the Emails model is defined in myapp



def buildEmail(email_task_id, email_id):
    print("Built Email is running")
    email_task = EmailTask.objects.get(id=email_task_id)
    email_s = Emails.objects.get(id=email_id)
    email_from = settings.EMAIL_HOST_USER

    # convert email_task.recipients to a list, because the outputted data from the database is a string of emails.
    # email_list = ast.literal_eval(email_task.recipients)
    email_list = ast.literal_eval(email_task.recipients)


    print(email_list)

    subject, from_email = email_s.subject, email_from

    context = {}
    picture_urls = []
    domain = "http://127.0.0.1:8000/"
    template_name = ""
    email_head =f"http://{domain}media/email_assets/images/ELG_Header_i1aFdsr.png"
    email_signature =f"http://{domain}media/email_assets/images/Email_Signature.png"



    if email_s.product1_image:
        picture_urls.append(f"http://{domain}media/{email_s.product1_image}")
    if email_s.product2_image:
        picture_urls.append(f"http://{domain}media/{email_s.product2_image}")
    if email_s.product3_image:
        picture_urls.append(f"http://{domain}media/{email_s.product3_image}")
    if email_s.product4_image:
        picture_urls.append(f"http://{domain}media/{email_s.product4_image}")




    if email_s.emailtype == "Store News":
        context = {
            'receiver': "ELG-Firearms Member",
            'emails': email_s,
            'picture_urls': picture_urls,
            'email_head':email_head,
            'email_signature':email_signature,
        }
        template_name = "storesnews.html"

    # elif email_s.emailtype == "Promotional":
    #     context = {'receiver': "ELG-Firearms Member", "emails": email_s, 'picture_urls': picture_urls}
    #     template_name = "new4items.html"

    elif email_s.emailtype == "Promotional":
        context = {'receiver': "ELG-Firearms Member", "emails": email_s, 'picture_urls': picture_urls,
            'email_head':email_head,
            'email_signature':email_signature,}
        template_name = "new4items.html"

    elif email_s.emailtype == "Seasonal Sales":
        context = {'receiver': "ELG-Firearms Member", 'emails': email_s, 'picture_urls': picture_urls,
            'email_head':email_head,
            'email_signature':email_signature,}
        template_name = "season_specials.html"

    message_html = render_to_string(f'email_templates/{template_name}', context)

    for recipient in email_list:
        email_message = EmailMessage(subject, message_html, from_email, [recipient])
        email_message.content_subtype = "html"
        email_message.send()



    print("Built email was sent! Email was Sent!!")
    return True
