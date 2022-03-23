from django.contrib import admin
from django.urls import path

import blog.views

urlpatterns = [
    # path('', blog.views.index, name='blog-index'),
    path('', blog.views.BlogListView.as_view(), name='blog-index'),
    path('about/', blog.views.about, name='blog-about'),
    # path('<int:id>', blog.views.detail, name='detail'),
    path('blog/<int:pk>', blog.views.BlogDetailView.as_view(), name='blog-detail'),
    path('blog/new/', blog.views.BlogCreateView.as_view(), name='blog-create'),
    path('blog/<int:pk>/update', blog.views.BlogUpdateView.as_view(), name='blog-update'),
    path('blog/<int:pk>/delete', blog.views.BlogDeleteView.as_view(), name='blog-delete'),
    path('blog/<int:pk>/comment', blog.views.BlogFormView.as_view(), name='blog-form-comment'),
]