import django_filters

from .models import Attendance

class AttendanceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendance
        fields = '__all__'
        exclude = ['Faculty_Name', 'status','time','branch','section']