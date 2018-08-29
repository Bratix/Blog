from django.urls import path
from django.conf.urls import url
from . import views

app_name = "blog"

urlpatterns = [
    #/blogs/
    path('', views.IndexView.as_view(), name = "index"),
    #/blogs/1
    path('<pk>', views.BlogDetailView.as_view(), name = "detail"),

    #/blogs/create/blog
    path('create/blog', views.BlogCreate.as_view(), name = "blog_create"),
    #/blogs/delete/blog/1
    path('delete/blog/<pk>', views.BlogDelete.as_view(), name = "blog_delete"),
    #/blogs/update/blog/1
    path('update/blog/<pk>', views.BlogUpdate.as_view(), name = "blog_update"),

    #/blogs/create/post
    path('create/<pk>/post', views.BlogPostCreate.as_view(), name = "post_create"),
    #/blogs/delete/post/1
    path('delete/post/<pk>', views.BlogPostDelete.as_view(), name = "post_delete"),
    #/blogs/update/post/1
    path('update/<pk>/post', views.BlogPostUpdate.as_view(), name = "post_update"),

    #/blogs/create/comment
    path('create/<pk>/comment', views.CommentCreate.as_view(), name = "comment_create"),
    #/blogs/delete/blog/1
    path('delete/comment/<pk>', views.CommentDelete.as_view(), name = "comment_delete"),
    #/blogs/update/blog/1
    path('update/<pk>/comment', views.CommentUpdate.as_view(), name = "comment_update"),

    #blogs/view/categories
    path('view/categories', views.CategoryView.as_view(), name = "category"),
    #blogs/view/categories/1
    path('view/categories/<pk>', views.BlogsbyCategoryView.as_view(), name = "category_detail"),

    #blogs/search/tags
    path('view/search/tags', views.BlogsPostSearchByTag.as_view(), name = 'search_tag')
]

