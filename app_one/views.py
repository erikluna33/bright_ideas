from django.shortcuts import render, redirect
from .models import User, Idea, Comment
import bcrypt
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def admin_page(request):
    return render(request, '/admin')

def register_user(request):
    if request.method == 'POST':
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
        current_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash,
            user_level = 0
        )
        if current_user.id == 1:
            current_user.user_level = 9
            current_user.save()
        request.session['current_user'] = current_user.first_name
        request.session['success'] = "Successful Registration, log in!"
            
    return redirect('/')

def login_user(request):
    if request.method == 'POST':
        errors = User.objects.log_validator(request.POST)
        if len(errors) != 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')
        

        user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/dashboard')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')



def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.filter(id=request.session['user_id'])
    if not user:
        return redirect('/')
    context = {
        'all_users': User.objects.all(),

    }
    if user[0].user_level !=9:
        return render(request,'dashboard.html', context)
    else:
        return render(request,'dashboard_admin.html', context)

def add_user_page(request):
    return render(request, 'add_user_page.html')

def add_new_user(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        errors = User.objects.add_validator(request.POST)
        if len(errors) != 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/add_user_page')
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash,
            user_level = 0
        )
    return redirect('/dashboard')

def update_user_page(request, uid):
    if 'user_id' not in request.session:
        return redirect('/')
    user_update = User.objects.filter(id=uid)
    if len(user_update) == 0:
        return redirect('/dashboard')
    context = {
        'user_update': user_update[0],
        'user': User.objects.get(id = request.session['user_id'])
    }

    return render(request, 'update_user_page.html', context)

def update_user(request, uid):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = User.objects.update_validator(request.POST)
        if len(errors) != 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect(f'/user/update/{uid}')
        update_user = User.objects.get(id=uid)
        update_user.first_name = request.POST['first_name']
        update_user.last_name = request.POST['last_name']
        update_user.email = request.POST['email']
        update_user.save()
    return redirect('/dashboard')

def delete_user(request, uid):
    delete_user = User.objects.get(id=uid)
    delete_user.delete()
    return redirect('/dashboard')

def ideas_page(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'all_users': User.objects.all(),
        'all_ideas': Idea.objects.all().order_by('-created_at'),
        'all_comments': Comment.objects.all() 
    }
    return render(request, 'ideas_page.html', context)

def post_idea(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == 'POST':
        errors = User.objects.idea_validator(request.POST)
        if len(errors) != 0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/ideas')
        this_user = User.objects.get(id = int(request.session['user_id']))
        Idea.objects.create(
            idea = request.POST['idea'],
            user = this_user
        )
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_users': User.objects.all(),
            'all_ideas': Idea.objects.all().order_by('-created_at'),
            'all_comments': Comment.objects.all() 
        }
        
        return render(request,'idea_list.html', context)
    return redirect('/ideas')

def delete_idea(request,iid):
    delete_idea = Idea.objects.get(id=iid)
    delete_idea.delete()
    return redirect('/ideas')

    
    
    

def post_comment(request, iid):
    if request.method == 'POST':
        this_user = User.objects.get(id = int(request.session['user_id']))
        this_idea = Idea.objects.get(id=iid)
        Comment.objects.create(
            comment = request.POST['comment'],
            poster = this_user,
            wall_idea = this_idea
        )
    return redirect('/ideas')

def user_profile(request, uid):
    context = {
        'current_user': User.objects.get(id=uid)
    }
    return render(request, 'user_profile_page.html', context)



        

        
        
        



    
    


    
    