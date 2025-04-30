
import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'simplelms.settings'
import django
django.setup()

import csv
from django.contrib.auth.models import User
from core.models import Course, CourseMember,Comment,CourseContent
import json
from random import randint

filepath = './dummy_data/'


with open(filepath+'contents.json') as jsonfile:
    comments = json.load(jsonfile)
    obj_create = []
    for num, row in enumerate(comments):
        if not CourseContent.objects.filter(pk=num+1).exists():
            obj_create.append(CourseContent(
			            course_id=Course.objects.get(pk=int(row['course_id'])), 
						 video_url=row['video_url'], name=row['name'], 
						 description=row['description'], id=num+1))
    CourseContent.objects.bulk_create(obj_create)


# with open(filepath+'comments.json') as jsonfile:
#     comments = json.load(jsonfile)
#     obj_create = []
#     for num, row in enumerate(comments):
#         if int(row['user_id']) > 50:
#             row['user_id'] = randint(5, 40)
#         if not Comment.objects.filter(pk=num+1).exists():
#             obj_create.append(Comment(
# 			            content_id=CourseContent.objects.get(pk=int(row['content_id'])), 
# 					   user_id=User.objects.get(pk=int(row['user_id'])), id=num+1,
# 					   comment=row['comment']))
#     Comment.objects.bulk_create(obj_create)