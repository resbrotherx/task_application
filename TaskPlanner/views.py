from django.shortcuts import render,get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from users.models import *
from django.http import JsonResponse


# Create your views here.

def index(request):
    return render(request, "index.html")

@login_required
def task(request):
    user = request.user
    tasks = Task.objects.filter(creator=user)
    users = User.objects.all()
    total_low = Task.objects.filter(creator=user,pri_status="low").count()
    total_high = Task.objects.filter(creator=user,pri_status="high").count()
    total_medium = Task.objects.filter(creator=user,pri_status="medium").count()
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        due_time = request.POST.get('due_time')
        pri_status = request.POST.get('pri_status')
        completed = False

        if title != "" and due_date != "" and due_time !="":
            task = Task(
                creator=user,
                title=title,
                description=description,
                due_date=due_date,
                due_time=due_time,
                pri_status=pri_status,
                completed=completed
            )
            task.save()
            return redirect('/task/')
    # else:
    #     return render(request, 'add_task.html')
    return render(request,"dashbaord/task.html", {
        'tasks': tasks,
        'user':users,
        'total_high':total_high,
        'total_low':total_low,
        'total_medium':total_medium,
    })

@login_required
def emoji_send(request):
    if request.method == 'POST':
        try:
            task_id = request.POST['task_id']
            emojis = request.POST['emojis']  # Fix the parameter name here
            task = get_object_or_404(Task, pk=task_id)
            # to_user = get_object_or_404(User, pk=to_user_id)

            task.emoji = emojis
            task.save()

            success = "emoji saved successfully."
            return JsonResponse({"success": success})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method"})

@login_required
def shead_task(request):
    if request.method == 'POST':
        try:
            task_id = request.POST['task_id']
            to_user_id = int(request.POST['to_users'])  # Fix the parameter name here
            task = get_object_or_404(Task, pk=task_id)
            to_user = get_object_or_404(User, pk=to_user_id)
            task.shared_with.add(to_user)
            task.save()

            success = "Task shared successfully."
            return JsonResponse({"success": success})
        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method"})
        
        # if form.is_valid():

    # return render(request, 'share_task.html', {'form': form})
def shared_task(request):
    user = request.user
    users = User.objects.all()
    tasks = Task.objects.filter(shared_with=user)
    total_low = Task.objects.filter(creator=user,pri_status="low").count()
    total_high = Task.objects.filter(creator=user,pri_status="high").count()
    total_medium = Task.objects.filter(creator=user,pri_status="medium").count()
    return render(request, 'dashbaord/shead_task.html', {'tasks': tasks,'user':users,
        'total_high':total_high,
        'total_low':total_low,
        'total_medium':total_medium})

@login_required
def completed(request):
    # Filter tasks based on the logged-in user and completed status
    user = request.user
    completed_tasks = Task.objects.filter(creator=request.user, completed=True)
    users = User.objects.all()
    total_low = Task.objects.filter(creator=user,pri_status="low").count()
    total_high = Task.objects.filter(creator=user,pri_status="high").count()
    total_medium = Task.objects.filter(creator=user,pri_status="medium").count()
    return render(request, 'dashbaord/completed_task.html', {
        'tasks': completed_tasks,
        'user':users,
        'total_high':total_high,
        'total_low':total_low,
        'total_medium':total_medium,
    })

def remaining(request):
    remaining_tasks = Task.objects.filter(completed=False)
    return render(request, 'remaining.html', {
        'tasks': remaining_tasks,
    })

# def add_task(request):
#     if request.method == "POST":
#         title = request.POST.get('title')
#         description = request.POST.get('description')
#         due_date = request.POST.get('due_date')
#         due_time = request.POST.get('due_time')
#         completed = False

#         if title != "" and due_date != "" and due_time !="":
#             task = Task(
#                 title=title,
#                 description=description,
#                 due_date=due_date,
#                 due_time=due_time,
#                 completed=completed
#             )
#             task.save()
#             return redirect('home')
#     else:
#         return render(request, 'add_task.html') 
#     return render(request, 'add_task.html')


def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    return render(request, 'task_detail.html', {
        "task": task,
    })


def toggle_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    if task:
        task.completed = not task.completed
        task.save()
        return redirect('home')

@login_required
def remove_task(request, task_id):
    user = request.user
    task = Task.objects.get(creator=user,id=task_id)
    if task:
        task.delete()
        return redirect('/task/')

@login_required
def dashboard(request):
    user = request.user

    # 1. Use filter for counting tasks
    total_task = Task.objects.filter(creator=user).count()
    total_received_task = Task.objects.filter(shared_with=user).count()
    total_shared_task = Task.objects.filter(creator=user, shared_with__isnull=False).count()
    total_shared_completed_task = Task.objects.filter(creator=user, shared_with__isnull=False,completed=True).count()
    total_completed_task = Task.objects.filter(creator=user, completed=True).count()

    # Assuming total_medium should be something specific to your implementation
    total_medium = 0  # Replace with your logic for total_medium

    messages = Messages.get_message(user=request.user)
    active_direct = None
    directs = Messages.objects.none()  # Initialize as an empty queryset

    if messages:
        message = messages[0]
        active_direct = message['user'].username
        directs = Messages.objects.filter(user=request.user, reciepient=message['user'])
        # directs.update(is_read=True)

    print(total_shared_task)
    return render(request,'dashbaord/dashboard.html', {
        'total_completed_task': total_completed_task,
        'total_received_task': total_received_task,
        'friends': directs.count(),
        'total_task': total_task,
        'total_shared_completed_task':total_shared_completed_task,
        'total_shared_task':total_shared_task,
        'total_medium': total_medium,
    })



@login_required
def chat(request):
    if request.user.is_authenticated:
        user = request.user
        messages = Messages.get_message(user=request.user)
        active_direct = None
        directs = None
        profile = get_object_or_404(Profile, user=user)

        all_users = User.objects.all()

        if messages:
            message = messages[0]
            active_direct = message['user'].username
            directs = Messages.objects.filter(user=request.user, reciepient=message['user'])
            directs.update(is_read=True)

            for message in messages:
                if message['user'].username == active_direct:
                    message['unread'] = 0

        context = {

            "all_users": all_users,
            'directs':directs,
            'messages': messages,
            'active_direct': active_direct,
            'profile': profile,
            
            }
        return render(request, "dashbaord/chat.html", context)


@login_required
def Directs(request, username):
    user  = request.user
    messages = Messages.get_message(user=user)
    active_direct = username
    directs = Messages.objects.filter(user=user, reciepient__username=username)  
    directs.update(is_read=True)


    q = request.GET.get("q").strip() if request.GET.get("q") != None else ""

    all_users = User.objects.all()


    for message in messages:
            if message['user'].username == username:
                message['unread'] = 0
    context = {
        'all_users': all_users,
        'directs': directs,
        'messages': messages,
        'active_direct': active_direct,
        "user" : user,
        
    }
    return render(request, "dashbaord/chat.html", context)

def SendDirect(request):
    
    if request.method == "POST":
        from_user = request.user
        to_user_username = request.POST['to_user']
        body = request.POST['body']

        to_user = User.objects.get(username=to_user_username)
        Messages.sender_message(from_user, to_user, body)
        # return redirect('message')
        success = "Message Sent."
        return HttpResponse(success)



def deleteMessage(request, pk):
    messages = Messages.objects.get(id=pk)
    messages.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



@login_required
def calendar(request):
    return render(request,"dashbaord/calendar.html")


