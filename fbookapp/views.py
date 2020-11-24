from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import User, book
from django.views.decorators.csrf import csrf_exempt
import bcrypt

def index(request):
    return render(request,'index.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        email =  request.POST['email']
        errors = User.objects.basic_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST["pass"]
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            User.objects.create(firstname = request.POST['firstname'], lastname =request.POST['lastname'], email = email,
            password  = pw_hash)
            request.session["login_user"] = { "status": True, "login_id": User.objects.get(email=request.POST["email"]).id }
            print(" added to database")
            return redirect("/books")

def log(request):
    
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        request.session["login_user"] = { "status" : True, "login_id" : User.objects.get(email=request.POST["email"]).id }
        return redirect("/books")

def books(request):
        # login status check
    try:
        if request.session["login_user"]["status"]:
            this_user = User.objects.get(id=request.session["login_user"]["login_id"])

            books = book.objects.all()
            context = {
                "first_name" : this_user.firstname,
                "last_name" : this_user.lastname,
                "id"         : this_user.id,

                "objs"        : books,

            }
            return render(request, "books.html", context)
        
        else:
            messages.error(request, "Login error")
            return redirect("/")

        return render(request,'books.html', context )
    except:
         return redirect("/")
 
@csrf_exempt  
def emailvalidate(request):
    is_taken =User.objects.filter(email=request.POST['email']).exists()
    data = {'is_taken': is_taken}
    return JsonResponse(data)

def addbook(request):
    if request.method == 'POST':
        errors = book.objects.book_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/new')
        else:
            this_user = User.objects.get(id=request.session["login_user"]["login_id"])
            print("the user who want to add the book is", this_user.id )
            this_book = book.objects.create(title = request.POST['title'], desc =request.POST['desc'], uploaded_by =  this_user )
            this_book.User_who_like.add(this_user)

            return redirect("/books")

def edit(request, id):
    context = {}
    this_book_ = book.objects.get(id = int(id))
    print(this_book_.uploaded_by.id)
    user_of_this_book = this_book_.uploaded_by.id
    context["objs"]= book.objects.get(id = int(id))
    if user_of_this_book == request.session["login_user"]["login_id"]:
        return render(request, "editform.html", context )
    else:
        return render(request, "viewbook.html", context )


def update (request, id):
        errors = book.objects.book_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/books'+str(id))
        else:       
            this_book = book.objects.get(id = int(id))
            this_book.title =  request.POST['title']
            this_book.desc = request.POST['desc']
            this_book.save()
            return redirect("/books")
def favorite(request, id):
    this_user = User.objects.get(id=request.session["login_user"]["login_id"])
    this_book = book.objects.get ( id = int (id))
    this_user.Liked_book.add(this_book)
    return redirect("/books")

def delete(request, id):
    this_book = book.objects.get (id = int(id))
    this_book.delete()
    return redirect("/books")


def unfavoriet(request, id):
    this_user = User.objects.get(id=request.session["login_user"]["login_id"])
    this_user.Liked_book.remove()
    return redirect("/books")





def logout(request):
    del request.session["login_user"]
    return redirect("/")

