from rest_framework import serializers

class OutgoingMailSerializer(serializers.Serializer):
    from_ = serializers.CharField(source='from_email')  # mapping from 'from_email'
    to = serializers.CharField(source='to_address')     # mapping from 'to_address'
    status = serializers.CharField()
    message_id = serializers.CharField(required=False)


class MailStatusSummarySerializer(serializers.Serializer):
    sent = serializers.IntegerField()
    deferred = serializers.IntegerField()
    bounced = serializers.IntegerField()
    received = serializers.IntegerField()