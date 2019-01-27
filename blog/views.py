from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post, Comment
from .forms import CommentForm


class PostListView(ListView):
    """a class-based view to display the list of posts."""
    queryset = Post.published.all()  # object list
    context_object_name = 'posts'  # context variable for query results, defaults to object_list
    paginate_by = 1  # number of posts per page
    template_name = 'blog/post/list.html'  # rendering template


def post_list(request):
    """a view to display the list of posts."""
    object_list = Post.published.all()
    paginator = Paginator(object_list, 1)  # number of posts per page
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # deliver first page if page is not an integer
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # deliver last page if page is out of range

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})


def post_detail(request, year, month, day, post):
    """a view to display details of a single post."""
    post = get_object_or_404(
        Post,
        slug=post,
        status='published',
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    # active comments for this post
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # comment posted
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            # don't save comment to database yet
            new_comment = comment_form.save(commit=False)

            # assign the current post to the comment
            new_comment.post = post

            # finally, save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})
