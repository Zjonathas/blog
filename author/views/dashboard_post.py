from django.views import View
from django.views.generic import DetailView
from django.http.response import Http404
from blog.models import Post
from author.forms.post_form import PostForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required(
    login_url='blog:home', redirect_field_name='next'), name='dispatch')
class DashboardPost(View):
    def get_post(self, id=None):
        post = None

        if id is not None:
            try:
                post = Post.objects.filter(
                    author=self.request.user, pk=id
                ).first()
            except Post.DoesNotExist:
                raise Http404('Post not found')
        return post

    def render_post(self, form):
        return render(
            self.request, 'author/page/dashboard_post.html', {'form': form}
        )

    def get(self, request, id=None):
        post = self.get_post(id)
        form = PostForm(instance=post)
        return self.render_post(form)

    def post(self, request, id=None):
        post = self.get_post(id)
        form = PostForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=post
            )

        if form.is_valid():
            post = form.save(commit=False)

            post.author = request.user
            post.is_published = False

            post.save()

            messages.success(request, 'Post saved successfully')
            return redirect(reverse('blog:home'))
        return self.render_post(form)


@method_decorator(login_required(
    login_url='blog:home', redirect_field_name='next'), name='dispatch')
class DetailPostUnpublished(DetailView):
    model = Post
    template_name = 'blog/page/detail_post.html'
    context_object_name = 'post'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=False
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'is_detail_page': True
        })
        return context
