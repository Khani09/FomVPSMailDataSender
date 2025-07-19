# api/views.py
import os
import re
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from .serializers import OutgoingMailSerializer
import os, re
from datetime import datetime


# class HasAPIKeyPermission(BasePermission):
#     def has_permission(self, request, view):
#         return request.headers.get("X-API-KEY") == "your-secure-api-key"  # Replace with your actual API key check logic

class MailLogsView(APIView):
    # permission_classes = [HasAPIKeyPermission]

    def get(self, request):
        # log_file = "/var/log/mail.log"
        log_file = "mail.txt"  # Adjust this path as needed
        if not os.path.exists(log_file):
            return Response({"error": "Log file not found"}, status=404)

        with open(log_file, "r") as f:
            lines = f.readlines()[-100:]
        return Response({"logs": lines})




class OutgoingMailsView(APIView):
    # permission_classes = [HasAPIKeyPermission]

    def get(self, request):
        # log_file = "/var/log/mail.log"
        log_file = "mail.txt"  # Adjust this path as needed
        queue_map = {}
        outgoing = []

        if not os.path.exists(log_file):
            return Response({"error": "Log file not found"}, status=404)

        with open(log_file, "r") as f:
            lines = f.readlines()

        # Parse timestamps and senders
        for line in lines:
            timestamp_match = re.match(r'^([A-Za-z]{3} \d{1,2} \d{2}:\d{2}:\d{2})', line)
            timestamp = datetime.now()  # Fallback
            if timestamp_match:
                try:
                    timestamp = datetime.strptime(timestamp_match.group(1), "%b %d %H:%M:%S").replace(year=datetime.now().year)
                except:
                    pass

            sender_match = re.search(r'postfix/qmgr.*?(\w+): from=<([^>]+)>', line)
            if sender_match:
                queue_id, sender = sender_match.groups()
                queue_map[queue_id] = {"from_email": sender, "timestamp": timestamp}

        # Match recipients + statuses
        status_counts = {"sent": 0, "deferred": 0, "bounced": 0, "rejected": 0, "other": 0}

        for line in lines:
            timestamp_match = re.match(r'^([A-Za-z]{3} \d{1,2} \d{2}:\d{2}:\d{2})', line)
            timestamp = datetime.now()
            if timestamp_match:
                try:
                    timestamp = datetime.strptime(timestamp_match.group(1), "%b %d %H:%M:%S").replace(year=datetime.now().year)
                except:
                    pass

            match = re.search(r'postfix/.*?(\w+): to=<([^>]+)>, .*status=(\w+)', line)
            if match:
                queue_id, recipient, status_text = match.groups()
                status = status_text.lower()

                if queue_id in queue_map:
                    mail = queue_map[queue_id].copy()
                    mail.update({
                        "to_address": recipient,
                        "status": status,
                        "timestamp": timestamp
                    })
                    outgoing.append(mail)

                    if status in status_counts:
                        status_counts[status] += 1
                    else:
                        status_counts["other"] += 1

        serialized = OutgoingMailSerializer(outgoing[-50:], many=True)
        return Response({
            "summary": status_counts,
            "outgoing_mails": serialized.data
        })


class ReceivedMailsView(APIView):
    # permission_classes = [HasAPIKeyPermission]

    def get(self, request):
        # log_file = "/var/log/mail.log"
        log_file = "mail.txt"  # Adjust this path as needed
        queue_map = {}
        received = []

        with open(log_file, "r") as f:
            lines = f.readlines()

        for line in lines:
            match = re.search(r'postfix/qmgr.*?(\w+): from=<([^>]+)>', line)
            if match:
                queue_id, sender = match.groups()
                queue_map[queue_id] = {"from": sender}

        for line in lines:
            match = re.search(r'postfix/.*?(\w+): to=<([^>]+)>, .*status=(\w+)', line)
            if match:
                queue_id, recipient, status_text = match.groups()
                if queue_id in queue_map:
                    data = queue_map[queue_id]
                    data.update({"to": recipient, "status": status_text})
                    received.append(data)

        return Response({"received_mails": received[-50:]})


class MailQueueView(APIView):
    # permission_classes = [HasAPIKeyPermission]

    def get(self, request):
        try:
            result = subprocess.run([
                "postqueue", "-p"
            ], capture_output=True, text=True, timeout=5)

            if result.returncode == 0:
                lines = result.stdout.strip().splitlines()
                if not lines or "Mail queue is empty" in lines[0]:
                    return Response({"mail_queue": [], "message": "Mail queue is empty."})
                return Response({"mail_queue": lines})
            else:
                return Response({"error": result.stderr}, status=500)
        except subprocess.TimeoutExpired:
            return Response({"error": "Timeout while checking mail queue"}, status=504)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class PostfixStatusView(APIView):
    # permission_classes = [HasAPIKeyPermission]

    def get(self, request):
        try:
            result = subprocess.run(["systemctl", "is-active", "postfix"], capture_output=True, text=True)
            return Response({"postfix_status": result.stdout.strip()})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class MailErrorsView(APIView):
    # permission_classes = [HasAPIKeyPermission]

    def get(self, request):
        log_file = "mail.txt"  # Adjust this path as needed
        # log_file = "/var/log/mail.log"
        errors = {"bounced": [], "deferred": [], "rejected": [], "error": []}

        with open(log_file, "r") as f:
            for line in f:
                l = line.lower()
                if "bounced" in l:
                    errors["bounced"].append(line)
                elif "deferred" in l:
                    errors["deferred"].append(line)
                elif "reject" in l:
                    errors["rejected"].append(line)
                elif "error" in l:
                    errors["error"].append(line)

        return Response({k: v[-50:] for k, v in errors.items()})