from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, FormView, ListView
from django.core.paginator import Paginator

# Create your views here.
from django.views.generic.edit import FormMixin, DeleteView

import blog.models
from blog.forms import CommentForm
from blog.models import Blog


# def index(request):
#     # context = {'blogs': blogs}
#     # return render(request, 'blog/index.html', context)
#     try:
#         blogs = Blog.objects.all()
#     except Blog.DoesNotExist:
#         raise Http404("Blog does not exist")
#     return render(request, 'blog/index.html', {'blogs': blogs})


def about(request):
    return render(request, 'blog/about.html')


# def detail(request, id):
#     blog = Blog.objects.get(id=id)
#     context = {'blog': blog}
#     return render(request, 'blog/detail.html', context)


class BlogListView(ListView):
    model = Blog
    paginate_by = 6
    ordering = ['-updated']
    # return object name : object_list


class BlogDetailView(DetailView):
    model = Blog
    # 디테일뷰에서 오브젝트를 가져와서 리턴하는 내용 설명


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog/blog_create_form.html'

    def form_valid(self, form):
        # *** from 인스턴스 blog_user를 요청 유저로 저장해야 함 ***
        form.instance.blog_user = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog/blog_update_form.html'

    def form_valid(self, form):
        # 권한 검증
        user = self.request.user
        form_blog = Blog.objects.get(pk=self.kwargs.get("pk"))

        if user == form_blog.blog_user:
            return super().form_valid(form)
        else:
            return HttpResponse("<h3>You dont have a permission</h3>")


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog-index')

    def form_valid(self, form):
        # 권한 검증
        user = self.request.user
        form_blog = Blog.objects.get(pk=self.kwargs.get("pk"))
        if user == form_blog.blog_user:
            return super().form_valid(form)
        else:
            return HttpResponse("<h3>You dont have a permission</h3>")


class BlogFormView(LoginRequiredMixin, FormView):
    template_name = 'blog/blog_comment.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'pk': self.kwargs.get("pk")})

    def form_valid(self, form):
        form.instance.blog = Blog.objects.get(pk=self.kwargs.get("pk"))
        # comment user를 설정해야 함 ***
        form.instance.comment_user = self.request.user
        form.save()
        return super().form_valid(form)