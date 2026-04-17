from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import Note
import json

def login(request):
    if request.method == "POST":
        action = request.POST.get("action")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if action == "signup":
            if User.objects.filter(username=username).exists():
                return render(request, "MyNotesFrontend/login.html", {"error": "User exists"})
            User.objects.create_user(
            username=username,
            password=password
            )
            return redirect("")
        
        elif action == "login":
            user = authenticate(request, username = username, password = password)

            if user is not None:
                auth_login(request, user)
                return redirect("/dashboard/")
            else:
                return render(request, "MyNotesFrontend/login.html", {"error": "invalid credentials"})
        return render(request, "MyNotesFrontend/login.html", {"error": "Invalid credentials"})
    
    return render(request, "MyNotesFrontend/login.html")

def logout(request):
    auth_logout(request)
    return redirect("login")

@login_required(login_url="/login/")
def dashboard(request):
    notes = Note.objects.filter(user = request.user).order_by("-created_at")
    data = []
    for note in notes:
        data.append(
            {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "subject_key": note.subject_key,
                "is_favourite": note.is_favourite,
                "attachment_name": note.attachment_name,
                "created_at": note.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                "updated_at": note.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
            }
        )

    return render(request, "MyNotesFrontend\\dashboard.html", {"data":data})

@login_required(login_url="/login/")
def create_note(request):
    if request.method == "POST":
        data = json.loads(request.body)
        note = Note.objects.create(
            user = request.user,
            title = data.get("title"),
            content = data.get("content"),
            subject_key = data.get("subject_key"),
            is_favourite = data.get("is_favourite"),
            attachment_name = data.get("attachment_name"),
            created_at = data.get("created_at"),
            updated_at = data.get("updated_at")
        )
        return JsonResponse(data={"message": "success"})
    return render(request, "MyNotesFrontend\\notes_creation_page.html")

@login_required(login_url="/login/")
def edit_note(request, noteid):
    note = Note.objects.get(id=noteid)
    note_data = []
    note_data.append(
            {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "subject_key": note.subject_key,
                "is_favourite": note.is_favourite,
                "attachment_name": note.attachment_name,
                "created_at": note.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                "updated_at": note.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
            }
    )

    if request.method == "GET":
        return render(request, "MyNotesFrontend\\notes_edit_page.html", {"data":note_data, "noteid":noteid})
    elif request.method == "PUT":
        data = json.loads(request.body)
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        note.subject_key = data.get('subject_key', note.subject_key)
        note.is_favourite = data.get('is_favourite', note.is_favourite)
        note.updated_at = data.get('updated_at', note.updated_at)
        note.save()
        return JsonResponse({"message":"success"})
    
@login_required(login_url="/login/")
def view_note(request, noteid):
    note = Note.objects.get(id=noteid)
    note_data = {
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "subject_key": note.subject_key,
        "is_favourite": note.is_favourite,
        "attachment_name": note.attachment_name,
        "created_at": note.created_at.strftime("%d/%m/%Y %H:%M:%S"),
        "updated_at": note.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
    }
    return render(request, "MyNotesFrontend\\notes_view_page.html", {"data": note_data})

@login_required(login_url="/login/")
def delete_note(request, noteid):
    if request.method == "DELETE":
        try:
            note = Note.objects.get(id=noteid)
            note.is_deleted = True
            note.save()
            return JsonResponse({"message": "success"})
        except Note.DoesNotExist:
            return JsonResponse({"message": "Not found"}, status = 404)
    return JsonResponse({"message": "Method not allowed"}, status = 405)