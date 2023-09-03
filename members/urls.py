# url to the /hello path
from . import views
from django.urls import path

urlpatterns = [
    path('all/', views.all),
    path('members/', views.get_members),
    path('activities/', views.activities),
    path('login/', views.login),
    path('assign-member/', views.assign),
    path('unassign-member/', views.unassign),
    path('finish-activity/', views.finish_activity),
    path("activities/active/", views.active_activities),
    path("activity/<int:activity_id>/", views.activity)
]
