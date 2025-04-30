from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from core.models import Course
# Create your views here.

def testing(request):
    user_test = User.objects.filter(username="usertesting")
    if not user_test.exists():
        user_test = User.objects.create_user(
                            username="usertesting", 
                            email="usertest@email.com", 
                            password="sanditesting")
    all_users = serializers.serialize('python', User.objects.all())

    admin = User.objects.get(pk=1)
    user_test.delete()

    after_delete = serializers.serialize('python', User.objects.all())

    response = {
            "admin_user": serializers.serialize('python', [admin])[0],
            "all_users" : all_users,
            "after_del" : after_delete,
        }
    return JsonResponse(response)
def studikasus(request):
    user_test = User.objects.filter(username="usertesting")
    if not user_test.exists():
        user_test = User.objects.create_user(
                            username="usertesting", 
                            email="usertest@email.com", 
                            password="sanditesting")
    all_users = serializers.serialize('python', User.objects.all())

    admin = User.objects.get(pk=1)
    user_test.delete()

    after_delete = serializers.serialize('python', User.objects.all())

    response = {
            "admin_user": serializers.serialize('python', [admin])[0],
            "all_users" : all_users,
            "after_del" : after_delete,
        }
    return JsonResponse(response)


def allCourse(request):
    allCourse = Course.objects.all()
    result = []
    for course in allCourse:
        record = {'id': course.id, 'name': course.name, 
                  'description': course.description, 
                  'price': course.price,
                  'teacher': {
                      'id': course.teacher.id,
                      'username': course.teacher.username,
                      'email': course.teacher.email,
                      'fullname': f"{course.teacher.first_name} {course.teacher.last_name}"
                  }}
        result.append(record)
    return JsonResponse(result, safe=False)