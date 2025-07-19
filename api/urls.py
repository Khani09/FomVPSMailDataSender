from django.urls import path
from .views import (
    MailLogsView,
    ReceivedMailsView,
    OutgoingMailsView,
    PostfixStatusView,
    MailErrorsView,
    MailQueueView
)

urlpatterns = [
    path("logs/", MailLogsView.as_view(), name="mail-logs"),
    path("received/", ReceivedMailsView.as_view(), name="received-mails"),
    path("outgoing/", OutgoingMailsView.as_view(), name="outgoing-mails"),
    path("status/", PostfixStatusView.as_view(), name="postfix-status"),
    path("errors/", MailErrorsView.as_view(), name="mail-errors"),
    path("queue/", MailQueueView.as_view(), name="mail-queue"),
]