from django.shortcuts import render
from django.http.response import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json,base64
from django.utils.datastructures import MultiValueDict
from httpcore import request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.http import QueryDict

from .Serializers import *
# Create your views here.

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def loginprofile(request):

    if request.method == "OPTIONS":
        return JsonResponse({}, status=200)

  

    data = json.loads(request.body)

    profile = LoginProfile.objects.create(
        name=data.get("name"),
        company=data.get("company"),
        designation=data.get("designation")
    )

    return JsonResponse({
        "status": "success",
        "id": profile.id
    }, status=201)

@csrf_exempt 
@require_http_methods(['GET'])
def get_loginer(request):
    profiles = LoginProfile.objects.all().order_by("-id")
    data = []
    for p in profiles:
        data.append({
            "id": p.id,
            "name": p.name,
            "company": p.company,
            "designation": p.designation
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def blog_list_create(request):

    if request.method == "GET":
        blogs = BlogPost.objects.all().order_by("-created_at")
        data = []

        for b in blogs:
            image_base64 = None
            if b.image:
                image_base64 = f"data:{b.image_type};base64," + base64.b64encode(b.image).decode()

            data.append({
                "id": b.id,
                "title": b.title,
                "description": b.description,
                "content": b.content,
                "image": image_base64,
                "created_at": b.created_at
            })

        return JsonResponse(data, safe=False)

    # CREATE
    body = json.loads(request.body)

    image_binary = None
    image_type = None

    if body.get("image"):
        header, encoded = body["image"].split(",", 1)
        image_type = header.split(":")[1].split(";")[0]
        image_binary = base64.b64decode(encoded)

    blog = BlogPost.objects.create(
        title=body["title"],
        description=body.get("description", ""),
        content=body["content"],
        image=image_binary,
        image_type=image_type
    )

    return JsonResponse({"message": "Blog created", "id": blog.id})



@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
def blog_update_delete(request, blog_id):

    try:
        blog = BlogPost.objects.get(id=blog_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "PUT":
        body = json.loads(request.body)

        blog.title = body["title"]
        blog.description = body.get("description", "")
        blog.content = body["content"]

        if body.get("image"):
            header, encoded = body["image"].split(",", 1)
            blog.image_type = header.split(":")[1].split(";")[0]
            blog.image = base64.b64decode(encoded)

        blog.save()
        return JsonResponse({"message": "Blog updated"})

    if request.method == "DELETE":
        blog.delete()
        return JsonResponse({"message": "Blog deleted"})

@api_view(['GET', 'POST'])
def skills_list_create(request):
    if request.method == 'GET':
        skills = SkillsMaster.objects.all().order_by('-id')
        serializer = SkillsMasterSerializer(skills, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = SkillsMasterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def skills_detail(request, pk):
    try:
        skill = SkillsMaster.objects.get(pk=pk)
    except SkillsMaster.DoesNotExist:
        return Response({"error": "Skill not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SkillsMasterSerializer(skill)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = SkillsMasterSerializer(skill, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        skill.delete()
        return Response({"message": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    



@api_view(['GET', 'POST'])
def project_list_create(request):
    if request.method == 'GET':
        projects = Project.objects.all().order_by('-id')
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Retrieve, update, or delete a single project
@api_view(['GET', 'PUT', 'DELETE'])
def project_detail(request, pk):
    try:
        project = Project.objects.get(pk=pk)
    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def profile(request):
    profile, _ = Profile.objects.get_or_create(id=1)

    if request.method == "GET":
        return JsonResponse({
            "name": profile.name,
            "location": profile.location,
            "phone": profile.phone,
            "ug_degree": profile.ug_degree,
            "ug_university": profile.ug_university,
            "ug_years": profile.ug_years,
            "pg_degree": profile.pg_degree,
            "pg_university": profile.pg_university,
            "pg_years": profile.pg_years,
            "photo": profile.photo_base64()
        })

    if request.method == "POST":  # Use POST instead of PUT
        # Text fields
        profile.name = request.POST.get("name", "")
        profile.location = request.POST.get("location", "")
        profile.phone = request.POST.get("phone", "")

        profile.ug_degree = request.POST.get("ug_degree", "")
        profile.ug_university = request.POST.get("ug_university", "")
        profile.ug_years = request.POST.get("ug_years", "")

        profile.pg_degree = request.POST.get("pg_degree", "")
        profile.pg_university = request.POST.get("pg_university", "")
        profile.pg_years = request.POST.get("pg_years", "")

        # PHOTO: file upload
        if "photo" in request.FILES:
            profile.photo = request.FILES["photo"].read()
        elif "photo" in request.POST and request.POST["photo"].startswith("data:image"):
            photo_b64 = request.POST["photo"].split(",")[1]
            profile.photo = base64.b64decode(photo_b64)

        profile.save()

        return JsonResponse({
            "status": "updated",
            "name": profile.name,
            "location": profile.location,
            "phone": profile.phone,
            "ug_degree": profile.ug_degree,
            "ug_university": profile.ug_university,
            "ug_years": profile.ug_years,
            "pg_degree": profile.pg_degree,
            "pg_university": profile.pg_university,
            "pg_years": profile.pg_years,
            "photo": profile.photo_base64()
        })