from rest_framework import serializers
from .models import Member , Activities


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"

class NewActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = ["name","points","type","department","importance","time"]
    
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = "__all__"
        