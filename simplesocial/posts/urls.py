from django.conf.urls import url

from . import views

app_name='posts'

urlpatterns = [
    url(r"^$", views.PostList.as_view(), name="all"),
    url(r"new/$", views.CreatePost.as_view(), name="create"),
    url(r"by/(?P<username>[-\w]+)/(?P<pk>\d+)/$",views.PostDetail.as_view(),name="single"),
    #url(r"like/(?P<slug>[-\w]+)/$",views.LikeView.as_view(),name="like"),
    url(r"delete/(?P<pk>\d+)/$",views.DeletePost.as_view(),name="delete"),
    url(r"like/<int:pk>/$",views.LikeView.as_view(),name="post_like"),
    #url(r"dislike/(?P<pk>\d+)/$",views.UnlikeView.as_view(),name="disliking"),

]
