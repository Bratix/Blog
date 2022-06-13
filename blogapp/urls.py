from django.urls import path
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
    path('blog/<pk>/subscribe', views.BlogSubscribe.as_view(), name="blog_subscribe" ),
    path('blog/<pk>/add-moderators', views.AddModerators.as_view(), name="add_moderators" ),
    path('blog/<pk>/remove-moderator/<moderator_pk>', views.RemoveModerator.as_view(), name="remove_moderator" ),

    #Post
    path('blog/<blog_pk>/post/create', views.PostCreate.as_view(), name = "post_create"),
    path('post/<pk>', views.PostDetail.as_view(), name = "post_detail"),
    path('post/<pk>/delete', views.PostDelete.as_view(), name = "post_delete"),
    path('post/<pk>/update', views.PostUpdate.as_view(), name = "post_update"),
    #like url
    path('posts/<pk>/like', views.PostLike.as_view(), name = "post_like"),

    #Comment
    path('post/<pk>/comment/create', views.CommentCreate.as_view(), name = "comment_create"),
    path('comment/<pk>/delete', views.CommentDelete.as_view(), name = "comment_delete"),
    path('comment/<pk>/update', views.CommentUpdate.as_view(), name = "comment_update"),

    #Profile
    path('profile/<pk>', views.ProfileDetail.as_view(), name = "profile_detail"),
    path('profile/<pk>/update', views.ProfileEdit.as_view(), name = "profile_update"),

    #Category
    path('view/categories/<pk>', views.CategoryDetail.as_view(), name = "category_detail"),

    #Search
    path('search', views.IndexSearch.as_view(), name="search_index"),
    path('search/blog', views.BlogSearch.as_view(), name="search_blog"),
    path('search/post', views.PostSearch.as_view(), name="search_post"),
    path('search/profile', views.ProfileSearch.as_view(), name="search_profile"),

    #Friend request
    path('friends', views.FriendList.as_view(), name="friend_list" ),
    path('friend-request/recieved', views.RecievedFriendRequestList.as_view(), name="recieved_friend_requests" ),
    path('friend-request/sent', views.SentFriendRequestList.as_view(), name="sent_friend_requests" ),
    path('friend-request/accept/<pk>',  views.AcceptFriendRequest.as_view(), name="accept_friend_request" ),
    path('friend-request/cancel/<pk>',  views.CancelFriendRequest.as_view(), name="cancel_friend_request" ),
    path('friend-request/send/<pk>',  views.SendFriendRequest.as_view(), name="send_friend_request" ),
    path('friend-request/delete/<pk>',  views.DeleteFriend.as_view(), name="delete_friend" ),
   
    #Notifications
    path('notifications',  views.GetNotifications.as_view(), name="notifications"),
    path('notifications/new/<last_time>', views.NewNotifications.as_view() , name="new_notifications"),
    path('notification/delete/<pk>', views.DeleteNotification.as_view() ,name="delete_notifications")


]

