from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
from core.models import Course ,CourseContent ,CourseMember,Comment
from django.db.models import Max, Min, Avg ,Count
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
    allCourse = Course.objects.select_related('teacher').all()
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

def userCourses(request):
    user = User.objects.get(pk=3)
    courses = Course.objects.filter(teacher=user.id)
    course_data = []
    for course in courses:
        record = {'id': course.id, 'name': course.name, 
                  'description': course.description, 'price': course.price}
        course_data.append(record)
    result = {'id': user.id, 'username': user.username, 'email': user.email, 
              'fullname': f"{user.first_name} {user.last_name}", 
              'courses': course_data}
    return JsonResponse(result, safe=False)

def courseStat(request):
    courses = Course.objects.all()
    stats = courses.aggregate(max_price=Max('price'),
                                min_price=Min('price'),
                                avg_price=Avg('price'))
    result = {'course_count': len(courses), 'courses': stats}
    return JsonResponse(result, safe=False)

def courseMemberStat(request):
    courses = Course.objects.filter(description__contains='python') \
                            .annotate(member_num=Count('coursemember'))
    course_data = []
    for course in courses:
        record = {'id': course.id, 'name': course.name, 'price': course.price, 
                  'member_count': course.member_num}
        course_data.append(record)
    result = {'data_count': len(course_data), 'data':course_data}
    return JsonResponse(result)

# statistik semua course
def courseStat(request):
  courses = Course.objects.all()
  stats = courses.aggregate(max_price=Max('price'),
                              min_price=Min('price'),
                              avg_price=Avg('price'))
  cheapest = Course.objects.filter(price=stats['min_price'])
  expensive = Course.objects.filter(price=stats['max_price'])
  popular = Course.objects.annotate(member_count=Count('coursemember'))\
                          .order_by('-member_count')[:5]
  unpopular = Course.objects.annotate(member_count=Count('coursemember'))\
                          .order_by('member_count')[:5]

  result = {'course_count': len(courses), 'courses': stats,
            'cheapest': serializers.serialize('python', cheapest), 
            'expensive': serializers.serialize('python', expensive),
            'popular': serializers.serialize('python', popular), 
            'unpopular': serializers.serialize('python', unpopular)}
  return JsonResponse(result, safe=False)

def courseDetail(request, course_id):
   course = Course.objects.annotate(member_count=Count('coursemember'), 
                                 content_count=Count('coursecontent'),
                                 comment_count=Count('coursecontent__comment'))\
                           .get(pk=course_id)
   contents = CourseContent.objects.filter(course_id=course.id)\
               .annotate(count_comment=Count('comment'))\
               .order_by('-count_comment')[:3]
   result = {"name": course.name, 'description': course.description, 'price': course.price, 
             'member_count': course.member_count, 'content_count': course.content_count,
             'teacher': {'username': course.teacher.username, 'email': 
                         course.teacher.email, 'fullname': course.teacher.first_name},
             'comment_stat': {'comment_count': course.comment_count, 
                              'most_comment':[{'name': content.name, 
			                               'comment_count': content.count_comment} 
			                               for content in contents]},
             }

   return JsonResponse(result)

def userCourseStats(request):
    user_with_courses = User.objects.annotate(course_count=Count('course')).filter(course_count__gt=0).count()
    user_without_courses = User.objects.annotate(course_count=Count('course')).filter(course_count=0).count()
    avg_courses_per_user = CourseMember.objects.values('user_id').annotate(course_count=Count('course_id')).aggregate(avg=Avg('course_count'))['avg']
    top_user = CourseMember.objects.values('user_id', 'user_id__username').annotate(course_count=Count('course_id')).order_by('-course_count').first()

    result = {
        'user_with_courses': user_with_courses,
        'user_without_courses': user_without_courses,
        'avg_courses_per_user': avg_courses_per_user,
        'top_user': top_user
    }
    return JsonResponse(result)

def usersWithoutCourses(request):
    users = User.objects.exclude(id__in=CourseMember.objects.values_list('user_id', flat=True))
    user_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]

    result = {'user_count': len(user_data), 'users': user_data}
    return JsonResponse(result)