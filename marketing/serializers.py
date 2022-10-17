"""Switched to Graphene"""
# from rest_framework import serializers
from marketing.models import Subscriber  # , Site, Update, Incident, Uptime

# class SubscriberSerializer(serializers.HyperlinkedModelSerializer):
#     def validate_email(self, value):
#         if Subscriber.objects.filter(email=value.lower()).exists():
#             raise serializers.ValidationError("subscriber with this email already exists.")
#         return value.lower()

#     class Meta:
#         """remember ,"""
#         model = Subscriber
#         fields = ('email',)
