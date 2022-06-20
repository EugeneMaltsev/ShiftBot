from django.urls import path
from shift import views

urlpatterns = [
    path('project_list/', views.ProjectList.as_view()),
    path('project_create/', views.ProjectCreate.as_view()),
    path('project/<int:id>', views.ProjectDetail.as_view()),
    path('project_shift_list/', views.ShiftList.as_view()),
    path('project_shift_create/', views.ShiftCreate.as_view()),
    path('project_shift/<int:id>', views.ShiftDetail.as_view()),
    path('shift_statistic/', views.ShiftStatisticView.as_view()),
    path('project_statistic/', views.ProjectStatisticView.as_view())
]
