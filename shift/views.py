from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication

from shift import project_services
from shift.models import Project, Shift
from shift.serializers import ProjectSerializer, ShiftSerializer, ShiftStatisticSerializer, ProjectStatisticSerializer


class ProjectList(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return project_services.all_projects_by_user_queryset(self.request, self.queryset)


class ProjectCreate(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field = 'id'

    def get_queryset(self):
        return project_services.all_projects_by_user_queryset(self.request, self.queryset)


class ShiftList(generics.ListAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        return project_services.all_shifts_by_project_queryset(self.request, self.queryset)


class ShiftCreate(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            return serializer.save(user_project_id=self.request.data['user_project'])
        else:
            raise NotFound({'user_project': f'Project {self.request.data["user_project"]} does not exist'})

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user).filter(id=self.request.data['user_project'])


class ShiftDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    lookup_field = 'id'

    def get_queryset(self):
        return project_services.all_shifts_by_project_queryset(self.request, self.queryset)


class ProjectStatisticView(APIView):
    queryset = Project.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        statistic = project_services.get_projects_statistics(queryset=self.get_queryset())
        return Response(ProjectStatisticSerializer(statistic).data)

    def get_queryset(self):
        return project_services.all_projects_by_user_queryset(self.request, self.queryset)


class ShiftStatisticView(APIView):
    queryset = Shift.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        statistic = project_services.get_shift_statistics(queryset=self.get_queryset())
        return Response(ShiftStatisticSerializer(statistic).data)

    def get_queryset(self):
        return project_services.all_shifts_by_project_queryset(self.request, self.queryset)

# TODO: make [IsOwner] Permission
# TODO: Fix different exceptions in different circumstances when create the shift with invalid pk
