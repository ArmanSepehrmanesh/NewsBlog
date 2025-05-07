from django.shortcuts import render , get_object_or_404, redirect
from django.http import HttpResponse 
from .models import *
from .forms import *
from django.http import Http404
from django.views.decorators.http import require_POST
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

def post_list(request):
    posts = Post.published.all()  
    context = {
        "posts": posts,
    }
    return render(request, 'pages/list.html', context)  


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status='PB')
    comments = post.comment.filter(active=True) 
    form = CommentForm()
    context = {
        "post": post,
        'form': form,
        'comments': comments
    }
    return render(request, 'pages/detail.html', context)

#TICKET
def ticket(request):
    if request.method == 'POST':
        ticket_obj = Ticket.objects.create()
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect('pages:index')
    else:
        form = TicketForm()
        return render(request, 'forms/ticket.html',{'form':form})  
            
#Comment
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='PB') # اگر 'PB' مقدار منتشر شده است
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        "comment": comment
    }
    return render(request, "forms/comment.html", context)

#search
def post_search(request):
    query=None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.filter(Q(description__icontains=query) | Q(title__icontains=query)) 

    context = {
        'query': query,
        'results': results,
    }

    return render(request, 'blog/search.html', context)