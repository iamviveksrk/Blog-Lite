from workers import celery_app
from models import User,  Follow, Post, db, UserInfo
from datetime import datetime
from mail import mail, Message
from io import StringIO
import pandas as pd
from celery.schedules import crontab
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

import os

os.add_dll_directory(r"C:\Program Files\GTK3-Runtime Win64\bin")

environment = Environment(loader=FileSystemLoader("templates/"))

@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=19, minute=15), visit_reminder.s())
    sender.add_periodic_task(crontab(0, 0, day_of_month='2'), monthly_engagement_reminder.s(), name='engagement')

@celery_app.task()
def example_print_job():
    print('Hello Hi!')

@celery_app.task()
def user_export(username):

    user = db.session.query(User).get(username)
    
    columns = ['PostId','Title','Caption','Timestamp','Private']
    result = []
    for post in user.posts:
        result.append([post.post_id, post.title, post.caption, post.timestamp, post.private])
    
    post_export = pd.DataFrame(result, columns=columns)
    csv_stream = StringIO()
    post_export.to_csv(csv_stream, index=False)

    msg = Message(
        f'Sandigram | Post Export for user <{username}>', 
        recipients = [user.email]
    )
    msg.body = 'PFA'
    msg.attach(f'{username}.csv', 'text/csv', csv_stream.getvalue())
    mail.send(msg)

    return f'Email sent to {user.email} successfully!'

@celery_app.task()
def visit_reminder():
    current_time = datetime.today()
    today_timestamp = datetime(current_time.year, current_time.month, current_time.day).timestamp()
    
    users = db.session.query(User).filter(User.lastseen < today_timestamp)

    with mail.connect() as connection:
        for user in users:            
            subject = f"Hey {user.username}, we missed you today!"
            mail_message = Message(recipients=[user.email], 
                        body=f"All your friends are wondering what happened to you. Better visit and post asap!",
                        subject = subject)
            
            connection.send(mail_message)
    
    return 'batch-remind job done!'

@celery_app.task()
def monthly_engagement_reminder():

    
    current_time = datetime.today()
    previous_month_timestamp = datetime(current_time.year, current_time.month-1, 1).timestamp()
    today_timestamp = datetime(current_time.year, current_time.month, current_time.day-1).timestamp()

    with mail.connect() as connection:
        for user in db.session.query(User).filter(User.lastseen >= today_timestamp):
            username = user.username

            # Monthly Post Count
            month_post_count = db.session.query(Post).filter(Post.timestamp > previous_month_timestamp, Post.username == username).count()

            # Followers this month
            month_followers = db.session.query(Follow).filter(Follow.following==username, Follow.timestamp > previous_month_timestamp)
            
            # Followed this month
            month_followed = db.session.query(Follow).filter(Follow.follower==username, Follow.timestamp > previous_month_timestamp)

            template = environment.get_template("monthly_engagement_report.html")
            mail_html = template.render(username=username,month_post_count = month_post_count, month_followers=month_followers, month_followed=month_followed)

            mail_message = Message(recipients=[user.email],
                                   subject=f"Your Monthly Sandigram Engagement Report",
                                   html=mail_html)
            pdf = HTML(string=mail_html, base_url='').write_pdf()
            mail_message.attach(f'{username} MER.pdf', 'application/pdf', pdf)
            connection.send(mail_message)

    return 'batch-monthly engagement report job done!'



    

