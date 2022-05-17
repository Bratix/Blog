from django.urls import path
from django.conf.urls import url
from . import views

app_name = "blog"

urlpatterns = [
    #home page
    path('', views.IndexView.as_view(), name = "index"),

    #Blog
    path('blog/create', views.BlogCreate.as_view(), name = "blog_create"),
    path('blog/<pk>', views.BlogDetail.as_view(), name = "blog_detail"),
    path('blog/<pk>/delete', views.BlogDelete.as_view(), name = "blog_delete"),
    path('blog/<pk>/update', views.BlogUpdate.as_view(), name = "blog_update"),

    #Post
    path('blog/<blog_pk>/post/create', views.PostCreate.as_view(), name = "post_create"),
    path('post/<pk>', views.PostDetail.as_view(), name = "post_detail"),
    path('post/<pk>/delete', views.PostDelete.as_view(), name = "post_delete"),
    path('post/<pk>/update', views.PostUpdate.as_view(), name = "post_update"),
    #like url
    path('posts/<pk>/like', views.PostLike.as_view(), name = "post_like"),


    # #view/categories
    # path('view/categories', views.CategoryView.as_view(), name = "category"),
    # #view/categories/1
    # path('view/categories/<pk>', views.BlogsbyCategoryView.as_view(), name = "category_detail"),

    # #view/search/tags
    # path('view/search/tags', views.PostSearchByTag.as_view(), name = 'search_tag'),
 
    # #create/1/comment
    # path('create/<pk>/comment', views.CommentCreate.as_view(), name = "comment_create"),
    # #delete/blog/1
    # path('delete/comment/<pk>', views.CommentDelete.as_view(), name = "comment_delete"),
    # #update/blog/1
    # path('update/<pk>/comment', views.CommentUpdate.as_view(), name = "comment_update"),

]

