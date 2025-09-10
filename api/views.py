from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import User, ClassInfo
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password

@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = json.loads(request.body)
        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "Email already exists"}, status=400)

        user = User.objects.create(
            full_name=full_name,
            email=email,
            password=make_password(password),
            role=role
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
                        "full_name": user.full_name,
                        "email": user.email,
                        "role": user.role
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
        data = json.loads(request.body)

        new_class = ClassInfo.objects.create(
            ClassName=data.get("ClassName"),
            ClassCode=data.get("ClassCode"),
            Description=data.get("Description"),
            InstructorID=data.get("InstructorID", 0),
            YearLevel=data.get("YearLevel"),
            ScheduleDays=data.get("ScheduleDays"),
            ScheduleTime=data.get("ScheduleTime"),
        )

        return JsonResponse({
            "success": True,
            "message": "Class added successfully",
            "class_id": new_class.ClassID
        })

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

