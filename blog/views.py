from django.shortcuts import render
from django.forms.models import BaseModelForm

from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,UpdateView,DeleteView)
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.


# posts=[
#     {
#         "author":"youssef",
#         "title":"test1",
#         "content":" skdsjkhfsfhsdf ",
#         "date_posted":"August 27 ,2018",
#     },
#     {
#         "author":"nader",
#         "title":" welcome",
#         "content":"second post content ",
#         "date_posted":"August 27 ,2018",
#     }
# ]
@login_required
def home(request):
    # context={"posts":posts}
    context={"posts":Post.objects.all()}

    return render(request,"blog/home.html",context)

def about(request):
    return render(request,"blog/about.html",{"title":"about"})


class PostListView(LoginRequiredMixin,ListView):
    model=Post
    template_name ="blog/home.html" #<app>/<model>_<viewtype>.html
    context_object_name="posts"
    ordering=["-date_posted"]

class PostDetailView(DetailView): #    template_name_suffix = "_detail"
    model=Post

class PostCreateView(LoginRequiredMixin,CreateView):#    template_name_suffix = "_form" ex:post_form 
    model=Post  
    fields=['title','content']
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author=self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):#template_name_suffix = "_form" ex:post_form 
    model=Post  
    fields=['title','content']
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author=self.request.user
        return super().form_valid(form)    
    
    def test_func(self) -> bool | None:
        post =self.get_object()
        if (self.request.user==post.author):
            return True
        return False
        


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):#   template_name_suffix = "_confirm_delete" ex:post_confirm_delete.html
    model=Post
    success_url="/"
    def test_func(self) -> bool | None:
        post =self.get_object()
        if (self.request.user==post.author):
            return True
        return False
