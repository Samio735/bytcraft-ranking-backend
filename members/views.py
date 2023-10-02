from django.shortcuts import render
from .models import Member, Activities
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MemberSerializer , NewActivitySerializer, ActivitySerializer
import os

# Create your views here.


@api_view(["GET"])
def all(request):
    querty_set = MemberSerializer(Member.objects.all().order_by("-points"), many=True).data
    return Response({"members": querty_set})

@api_view(["GET"])
def get_members(request):
    if request.method == "GET":
        if request.GET["department"] == "all":
            querty_set = MemberSerializer(Member.objects.all().order_by("-points"), many=True).data
            return Response({"members": querty_set})
        else:
            querty_set = MemberSerializer(Member.objects.filter(department=request.GET["department"]).order_by("-points"), many=True).data
            return Response({"members": querty_set})


@api_view(["GET","POST","DELETE"])
def activities(request):
    if request.method == "GET":
        if request.GET.get("department", None) == None:
                    query_set = ActivitySerializer(Activities.objects.all().prefetch_related("members"), many=True).data
                    return Response({"activities": query_set})
        else:
            query_set = ActivitySerializer(Activities.objects.filter(department=request.GET["department"]).prefetch_related("members"), many=True).data
            return Response({"activities": query_set})
    elif request.method == "POST":
        if check_credentials(request.data["department"], request.data["password"]):
            data = request.data
            points = 0
            if data["type"] == "meet":
                points = 10
            elif data["type"] == "task":
                points = 5
                if data["importance"] == "important":
                    points = points + 5
                if data["time"] == "takes-time":
                    points = points + 5
                if data["time"] == "ongoing":
                    points = points + 10
            elif data["type"] == "part":
                points = 30
            else:
                return Response({"error": "wrong activity type"})
            data["points"] = points
            serializer = NewActivitySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            resp = ActivitySerializer(Activities.objects.filter(department=request.data["department"],status="active").prefetch_related("members"), many=True).data
            return Response({"activities": resp})
        else:
            return Response({"error": "session expired"})
    elif request.method == "DELETE":
        if check_credentials(request.data["department"], request.data["password"]):
            activity = Activities.objects.get(id=request.data["activity"])
            activity.delete()
            resp = ActivitySerializer(Activities.objects.filter(department=request.data["department"],status="active").prefetch_related("members"), many=True).data
            return Response({"activities": resp})
        else:
            return Response({"error": "session expired"})
            

def check_credentials(department, password):
    
    if (department == "development" and password == os.environ.get("DEV_PASSWORD")) | (department == "design" and password == os.environ.get("DESIGN_PASSWORD")) | (department == "communication" and password == os.environ.get("COM_PASSWORD")) | (department == "relex-logistics" and password == os.environ.get("RELEX_PASSWORD")) | (department == "multimedia" and password == os.environ.get("MULTI_PASSWORD")):
        return True
    else:
        return False        

@api_view(["POST"])
def login(request):
    if request.method == "POST":
        if check_credentials(request.data["department"], request.data["password"]):
            return Response({"isLogedin": True,
                             "department": request.data["department"],
                             "password": request.data["password"]})
        else:
            return Response({"isLogedin": False,
                             "department": request.data["department"],
                             "password": request.data["password"],
                             "error": "wrong password or department",
                            "real": os.environ.get("DEV_PASSWORD")})
    
# assign a member to an activity

@api_view(["POST"])
def assign(request):
    if request.method == "POST":
        if check_credentials(request.data["department"], request.data["password"]):
            activity = Activities.objects.get(id=request.data["activity"])
            member = Member.objects.get(id=request.data["member"])
            activity.members.add(member)
            activity.save()
            return Response({"activities": ActivitySerializer(Activities.objects.filter(department=request.data["department"],status="active"), many=True).data ,
                             "activity": ActivitySerializer(activity).data})
        else:
            return Response({"error": "session expired"})
        

@api_view(["POST"])
def unassign(request):
    if request.method == "POST":
        if check_credentials(request.data["department"], request.data["password"]):
            activity = Activities.objects.get(id=request.data["activity"])
            member = Member.objects.get(id=request.data["member"])
            activity.members.remove(member)
            activity.save()
            return Response({"activities": ActivitySerializer(Activities.objects.filter(department=request.data["department"],status="active"), many=True).data ,
                             "activity": ActivitySerializer(activity).data})
        else:
            return Response({"error": "session expired"})
        
@api_view(["POST"])
def finish_activity(request):
    if request.method == "POST":
        if check_credentials(request.data["department"], request.data["password"]):
            activity = Activities.objects.get(id=request.data["activity"])
            if activity.status == "finished":
                return Response({"error": "activity already finished"})
            activity.status = "finished"
            members = Member.objects.filter(activities__id=request.data["activity"])
            if (activity.type == "meet" and activity.importance == "obligatory"):
                for member in members:
                    member.points = member.points + 20
                    member.save()
                all_members = Member.objects.all()
                for member in all_members:
                    member.points = member.points + -10
                    member.save()
            else:
                
                for member in members:
                    member.points = member.points + activity.points
                    member.save()
            activity.save()
            return Response({"activities": ActivitySerializer(Activities.objects.filter(department=request.data["department"],status="active"), many=True).data ,
                                "activity": ActivitySerializer(activity).data})
        else:
            return Response({"error": "session expired"})
        
@api_view(["GET"])
def active_activities(request):
    if request.method == "GET":
        if request.GET.get("department", None) == None:
            query_set = ActivitySerializer(Activities.objects.filter(status="active"), many=True).data
            return Response({"activities": query_set})
        else:
            query_set = ActivitySerializer(Activities.objects.filter(status="active", department=request.GET["department"]), many=True).data
            return Response({"activities": query_set})
        
@api_view(["GET"])
def activity(request, activity_id):
    if request.method == "GET":
        activity = Activities.objects.get(id=activity_id)
        return Response({"activity": ActivitySerializer(activity).data})
    
