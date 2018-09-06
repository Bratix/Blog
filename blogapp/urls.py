from django.urls import path
from django.conf.urls import url
from . import views

app_name = "blog"

urlpatterns = [
    #home page
    path('', views.IndexView.as_view(), name = "index"),
    #blog details page
    path('<pk>', views.BlogDetailView.as_view(), name = "detail"),
    #blog post detail page
    path('posts/<pk>', views.BlogPostDetailView.as_view(), name = "blogpost_detail"),
    #like url
    path('posts/<pk>/like', views.PostLike, name = "post_like"),



    #view/categories
    path('view/categories', views.CategoryView.as_view(), name = "category"),
    #view/categories/1
    path('view/categories/<pk>', views.BlogsbyCategoryView.as_view(), name = "category_detail"),

    #view/search/tags
    path('view/search/tags', views.BlogsPostSearchByTag.as_view(), name = 'search_tag'),


    #Create/Delete/Update views
    #create/blog
    path('create/blog', views.BlogCreate.as_view(), name = "blog_create"),
    #delete/blog/1
    path('delete/blog/<pk>', views.BlogDelete.as_view(), name = "blog_delete"),
    #update/blog/1
    path('update/blog/<pk>', views.BlogUpdate.as_view(), name = "blog_update"),

    #create/post
    path('create/<pk>/post', views.BlogPostCreate.as_view(), name = "post_create"),
    #delete/post/1
    path('delete/post/<pk>', views.BlogPostDelete.as_view(), name = "post_delete"),
    #update/post/1
    path('update/<pk>/post', views.BlogPostUpdate.as_view(), name = "post_update"),

    #create/1/comment
    path('create/<pk>/comment', views.CommentCreate.as_view(), name = "comment_create"),
    #delete/blog/1
    path('delete/comment/<pk>', views.CommentDelete.as_view(), name = "comment_delete"),
    #update/blog/1
    path('update/<pk>/comment', views.CommentUpdate.as_view(), name = "comment_update"),

]

