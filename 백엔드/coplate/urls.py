from django.urls import path

from . import views
from django.views.generic import RedirectView
from django.urls import reverse_lazy
urlpatterns = [

    # login
    path('', RedirectView.as_view(url=reverse_lazy('account_login'), permanent=False)), # 처음 페이지를 로그인 화면으로 바꾸기 
    # review
    path('index', views.IndexView.as_view(), name='index'),
    path('caffe/', views.CaffeListView.as_view(), name='caffe-list'),
    path('caffe/<int:caffe_id>/', views.CaffeDetailView.as_view(), name='caffe-detail'),
    path('caffe/new/', views.CaffeCreateView.as_view(), name='caffe-create'),
    path('caffe/<int:review_id>/edit/', views.CaffeUpdateView.as_view(), name='caffe-update'),
    path('search/',views.SearchView.as_view(), name='search'),
    path('caffe/<int:caffe_id>/delete/', views.CaffeDeleteView.as_view(), name='caffe-delete'),
    path('caffe/following/', views.FollowingReviewListView.as_view(), name='following-review-list'),
   
    # profile
    path('users/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    path('users/<int:user_id>/reviews/', views.UserReviewListView.as_view(), name='user-review-list'),
    path('set-profile/', views.ProfileSetView.as_view(), name='profile-set'),
    path('edit-profile/', views.ProfileUpdateView.as_view(), name='profile-update'),

    # dripshot
    path('dripshot/',views.DripshotsListView.as_view(),name='clothes-list'),
    path('drip_shot/list/',views.DripshotsMainListView.as_view(),name='clothes-main-list'), # 여기까지 만듬 
    path('caffes/<int:caffe_id>/', views.ReviewDetailView.as_view(), name='dripshot-detail'),
    path('caffes/new/', views.ReviewCreateView.as_view(), name='dripshot-create'),
    path('caffes/<int:review_id>/edit/', views.ReviewUpdateView.as_view(), name='dripshot-update'),
    path('caffes/<int:caffe_id>/delete/', views.ReviewDeleteView.as_view(), name='dripshot-delete'),
    path('caffes/following/', views.FollowingReviewListView.as_view(), name='following-review-list'),

    # around 
    path('around/',views.CaffeAroundListView.as_view(),name='around-list'), 
    path('around/list',views.CaffeAroundMainListView.as_view(),name='around-main-list'),
    path('caffes/<int:caffe_id>/', views.ReviewDetailView.as_view(), name='around-detail'),
    path('caffes/new/', views.ReviewCreateView.as_view(), name='around-create'),
    path('caffes/<int:review_id>/edit/', views.ReviewUpdateView.as_view(), name='around-update'),
    path('caffes/<int:caffe_id>/delete/', views.ReviewDeleteView.as_view(), name='around-delete'),
    path('caffes/following/', views.FollowingReviewListView.as_view(), name='following-review-list'),


    # comment
    path(
        'reviews/<int:review_id>/comments/create/',
        views.CommentCreateView.as_view(),
        name='comment-create',
    ),

    path('comments/<int:comment_id>/edit/', 
         views.CommentUpdateView.as_view(), 
         name='comment-update'),
    path('comments/<int:comment_id>/delete/', 
         views.CommentDeleteView.as_view(), 
         name='comment-delete'),

    # like
    path(
        'like/<int:content_type_id>/<int:object_id>/', # 이미 그 좋아요에는 contetn_type 이 이미 있는거임 
        views.ProcessLikeView.as_view(),
        name='process-like'
    ),
    # follow
    path(
        'users/<int:user_id>/follow/',
        views.ProcessFollowView.as_view(),
        name='process-follow',
    ),
    path('users/<int:user_id>/following/', 
         views.FollowingListView.as_view(),
           name='following-list'),
    path('users/<int:user_id>/followers/', 
         views.FollowerListView.as_view(),
           name='follower-list'),


]
