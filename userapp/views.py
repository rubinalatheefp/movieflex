from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.urls import reverse_lazy
from movieapp.models import MovieDetails,Category
from userapp.forms import MovieForm
from django.views.generic.edit import UpdateView
# Create your views here.
def Register(request):
    if request.method=='POST':
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request,"User already taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email already taken")
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
                user.save()
                return redirect('../login/')
        else:
            messages.info(request,'Password error')
            return redirect('register')
        return  redirect('/')
    return render(request,'register.html')

def Login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('movieapp:allMoviedetails')
        else:
            messages.info(request,'Not a Valid User')
    return render(request,'login.html')

def Logout(request):
    auth.logout(request)
    return redirect('movieapp:allMoviedetails')

def AddMovies(request):
    if request.method=='POST':
        title=request.POST.get('title',)
        m_slug=request.POST.get('slug',)
        description = request.POST.get('description',)
        trailer_Link = request.POST.get('trailer_Link',)
        release_date = request.POST.get('release_date',)
        category_name = request.POST.get('category',)
        poster = request.FILES['poster']
        category=Category.objects.get(name=category_name)
        cinema=MovieDetails(title=title,slug=m_slug,category=category,description=description,release_date=release_date,poster=poster,trailer_Link=trailer_Link)
        cinema.save()
        return redirect('movieapp:allMoviedetails')
    return render(request,'addmovies.html')

class ToDoUpdateView(UpdateView):
    model = MovieDetails
    template_name = 'update.html'
    fields = ('title','description','actors','poster','release_date','trailer_Link')
    def get_success_url(self):
        return  reverse_lazy('userapp:updatedetails',kwargs={'pk':self.object.id})

def Update(request,id):
    movie_dat=MovieDetails.objects.get(id=id)
    formdat=MovieForm(request.POST or None,request.FILES,instance=movie_dat)
    if formdat.is_valid():
        formdat.save()
        return redirect('movieapp:allMoviedetails')
    return render(request,'update.html',{'form':formdat,'movie':movie_dat})
def Delete(request,id):
    if request.method=='POST':
        Movie=MovieDetails.objects.get(id=id)
        Movie.delete()
        return redirect('movieapp:allMoviedetails')
    return render(request,'delete.html')
