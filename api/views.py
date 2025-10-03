from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User, ClassInfo, Assignment, Student
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout


@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")

        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Email already exists"}, status=400)

        user = User.objects.create(
            full_name=full_name,
            email=email,
            password=make_password(password),
        )

        return JsonResponse({"success": True, "message": "User created successfully"})
    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return JsonResponse({
                    "success": True,
                    "message": "Login successful",
                    "user": {
                        "user_id": user.user_id,
                        "full_name": user.full_name,
                        "email": user.email
                    }
                })
            else:
                return JsonResponse({"success": False, "message": "Incorrect password"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "message": "User not found"}, status=404)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


@csrf_exempt
def add_class(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            instructor_id = data.get("InstructorID")
            instructor = get_object_or_404(User, pk=instructor_id)

            new_class = ClassInfo.objects.create(
                ClassName=data.get("ClassName"),
                ClassCode=data.get("ClassCode"),
                Description=data.get("Description"),
                InstructorID=instructor,
                YearLevel=data.get("YearLevel"),
                ScheduleDays=data.get("ScheduleDays"),
                ScheduleTime=data.get("ScheduleTime"),
            )

            return JsonResponse({
                "success": True,
                "message": "Class added successfully",
                "class_id": new_class.ClassID
            })

        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": str(e)
            }, status=500)

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


@csrf_exempt
def get_classes(request):
    if request.method == "GET":
        classes = ClassInfo.objects.all().order_by('-DateCreated').values(
            'ClassID', 'ClassName', 'ClassCode', 'Description',
            'YearLevel', 'ScheduleDays', 'ScheduleTime'
        )
        return JsonResponse(list(classes), safe=False)
    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)


@csrf_exempt
def edit_class(request, class_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            class_obj = ClassInfo.objects.get(ClassID=class_id)

            class_obj.ClassName = data.get("ClassName", class_obj.ClassName)
            class_obj.ClassCode = data.get("ClassCode", class_obj.ClassCode)
            class_obj.Description = data.get("Description", class_obj.Description)
            class_obj.YearLevel = data.get("YearLevel", class_obj.YearLevel)
            class_obj.ScheduleDays = data.get("ScheduleDays", class_obj.ScheduleDays)
            class_obj.ScheduleTime = data.get("ScheduleTime", class_obj.ScheduleTime)

            class_obj.save()
            return JsonResponse({"success": True, "message": "Class updated successfully"})
        except ClassInfo.DoesNotExist:
            return JsonResponse({"success": False, "message": "Class not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


@csrf_exempt
def delete_class(request, class_id):
    if request.method == "DELETE":
        try:
            class_to_delete = ClassInfo.objects.get(ClassID=class_id)
            class_to_delete.delete()
            return JsonResponse({"success": True, "message": "Class deleted successfully"})
        except ClassInfo.DoesNotExist:
            return JsonResponse({"success": False, "message": "Class not found"}, status=404)
    return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)


@csrf_exempt
def add_assignment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            class_id = data.get('ClassID')
            title = data.get('Title')
            instructions = data.get('Instructions')
            date_posted_str = data.get('DatePosted')
            date_of_submission_str = data.get('DateOfSubmission')

            if not all([class_id, title, instructions, date_of_submission_str]):
                return JsonResponse({'error': 'Missing required fields.'}, status=400)

            if date_posted_str:
                date_posted = parse_datetime(date_posted_str)
                if date_posted is None:
                    return JsonResponse({'error': 'Invalid DatePosted format.'}, status=400)
            else:
                date_posted = timezone.now()

            date_of_submission = parse_datetime(date_of_submission_str)
            if date_of_submission is None:
                return JsonResponse({'error': 'Invalid DateOfSubmission format.'}, status=400)

            try:
                cls = ClassInfo.objects.get(pk=class_id)
            except ClassInfo.DoesNotExist:
                return JsonResponse({'error': 'Class not found.'}, status=404)

            assignment = Assignment.objects.create(
                ClassID=cls,
                Title=title,
                Instructions=instructions,
                DatePosted=date_posted,
                DateOfSubmission=date_of_submission
            )

            return JsonResponse({
                'success': True,
                'message': 'Assignment added successfully!',
                'assignment': {
                    'AssignmentID': assignment.AssignmentID,
                    'ClassID': assignment.ClassID.ClassID,
                    'Title': assignment.Title,
                    'Instructions': assignment.Instructions,
                    'DatePosted': assignment.DatePosted.isoformat(),
                    'DateOfSubmission': assignment.DateOfSubmission.isoformat()
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_assignments(request):
    if request.method == "GET":
        class_id = request.GET.get("class_id")

        if not class_id:
            return JsonResponse({"error": "Missing class_id"}, status=400)

        try:
            cls = ClassInfo.objects.get(pk=class_id)
        except ClassInfo.DoesNotExist:
            return JsonResponse({"error": "Class not found"}, status=404)

        assignments = Assignment.objects.filter(ClassID=cls).values(
            "AssignmentID",
            "Title",
            "Instructions",
            "DatePosted",
            "DateOfSubmission"
        )

        return JsonResponse(list(assignments), safe=False)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def update_assignment(request, pk):
    if request.method == "PUT":
        try:
            assignment = Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            return JsonResponse({"error": "Assignment not found."}, status=404)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

        assignment.Title = data.get("Title", assignment.Title)
        assignment.Instructions = data.get("Instructions", assignment.Instructions)
        assignment.DateOfSubmission = data.get("DateOfSubmission", assignment.DateOfSubmission)
        assignment.save()

        return JsonResponse({
            "id": assignment.id,
            "Title": assignment.Title,
            "Instructions": assignment.Instructions,
            "DateOfSubmission": assignment.DateOfSubmission.strftime("%Y-%m-%d")
        }, status=200)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
@api_view(['DELETE'])
def delete_assignment(request, assignment_id):
    try:
        assignment = Assignment.objects.get(AssignmentID=assignment_id)
        assignment.delete()
        return Response({"message": "Assignment deleted successfully"}, status=status.HTTP_200_OK)
    except Assignment.DoesNotExist:
        return Response({"message": "Assignment not found"}, status=status.HTTP_404_NOT_FOUND)


def dashboard_summary(request):
    total_classes = ClassInfo.objects.count()
    total_assignments = Assignment.objects.count()

    class_schedules = []
    classes = ClassInfo.objects.all()
    for cls in classes:
        assignment_count = Assignment.objects.filter(ClassID=cls).count()
        class_schedules.append({
            "ClassName": cls.ClassName,
            "ClassCode": cls.ClassCode,
            "ScheduleDays": cls.ScheduleDays,
            "ScheduleTime": cls.ScheduleTime.strftime("%H:%M"),
            "AssignmentCount": assignment_count   # 👈 add per-class assignments
        })

    data = {
        "total_classes": total_classes,
        "total_assignments": total_assignments,
        "class_schedules": class_schedules
    }

    return JsonResponse(data)


@csrf_exempt
def add_student(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    try:
        data = json.loads(request.body)

        first_name = data.get("FirstName")
        last_name = data.get("LastName")
        sex = data.get("Sex")
        department = data.get("Department")
        year_level = data.get("YearLevel")
        class_id = data.get("ClassID")

        if not all([first_name, last_name, sex, department, year_level, class_id]):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        try:
            class_instance = ClassInfo.objects.get(pk=class_id)
        except ClassInfo.DoesNotExist:
            return JsonResponse({"error": "Class not found"}, status=404)

        student = Student.objects.create(
            FirstName=first_name,
            LastName=last_name,
            Sex=sex,
            Department=department,
            YearLevel=year_level,
            ClassID=class_instance
        )

        return JsonResponse({
            "message": "Student added successfully",
            "StudentID": student.StudentID
        })

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def get_students(request):
    class_id = request.GET.get("class_id")
    if not class_id:
        return JsonResponse({"error": "class_id is required"}, status=400)

    try:
        class_instance = ClassInfo.objects.get(pk=class_id)
    except ClassInfo.DoesNotExist:
        return JsonResponse({"error": "Class not found"}, status=404)

    students = Student.objects.filter(ClassID=class_instance)
    student_list = []
    for s in students:
        student_list.append({
            "StudentID": s.StudentID,
            "FirstName": s.FirstName,
            "LastName": s.LastName,
            "Sex": s.Sex,
            "Department": s.Department,
            "YearLevel": s.YearLevel,
        })

    return JsonResponse(student_list, safe=False)


@csrf_exempt
def api_logout(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"success": True, "message": "Successfully logged out"})
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)