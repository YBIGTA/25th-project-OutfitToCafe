from django.urls import path

from . import views
from django.views.generic import RedirectView
from django.urls import reverse_lazy
urlpatterns = [

    # # login
    # path('', RedirectView.as_view(url=reverse_lazy('account_login'), permanent=False)), # 처음 페이지를 로그인 화면으로 바꾸기 
    # # review
    # path('index', views.IndexView.as_view(), name='index'),
    # path('style_cafe/', views.Style_CafeListView.as_view(), name='style-cafe-list'),
    # path('style_cafe/<int:cafe_id>/', views.CafeDetailView.as_view(), name='style-cafe-detail'),
    # # path('style_cafee/<int:cafe_id>/', views.CafeDetailView.as_view(), name='cafe-detail'),
    # path('cafes/<int:pk>/', views.CafeDetailView.as_view(), name='cafe-detail'),
    # path('cafes/<int:pk>/delete/', views.CafeDeleteView.as_view(), name='cafe-delete'),

    # path('cafes/', views.CafeListView.as_view(), name='cafe-list'),
    # path('cafes/<int:pk>/update/', views.CafeUpdateView.as_view(), name='cafe-update'),

    # path('style_cafe/new/', views.CafeCreateView.as_view(), name='cafe-create'),
    # path('style_cafe/<int:review_id>/edit/', views.CafeUpdateView.as_view(), name='style-cafe-update'),
    # path('style_search/',views.SearchView.as_view(), name='search'),
    # path('style_cafe/<int:pk>/delete/', views.CafeDeleteView.as_view(), name='style-cafe-delete'),
    # path('style_cafe/following/', views.FollowingReviewListView.as_view(), name='style-following-review-list'),
   
    # # profile
    # path('users/<int:user_id>/', views.ProfileView.as_view(), name='profile'),
    # path('users/<int:user_id>/reviews/', views.UserReviewListView.as_view(), name='user-review-list'),
    # path('set-profile/', views.ProfileSetView.as_view(), name='profile-set'),
    # path('edit-profile/', views.ProfileUpdateView.as_view(), name='profile-update'),

     path('', RedirectView.as_view(url=reverse_lazy('account_login'), permanent=False)), # 로그인 페이지로 리디렉션

    # cafe
    path('index/', views.IndexView.as_view(), name='index'),
    path('cafes/', views.CafeListView.as_view(), name='cafe-list'),
    path('cafes/<int:pk>/', views.CafeDetailView.as_view(), name='cafe-detail'),
    path('cafes/<int:pk>/update/', views.CafeUpdateView.as_view(), name='cafe-update'),
    path('cafes/<int:pk>/delete/', views.CafeDeleteView.as_view(), name='cafe-delete'),
    
    # style cafe
    path('style_cafe/', views.Style_CafeListView.as_view(), name='style-cafe-list'),
    path('style_cafe/new/', views.CafeCreateView.as_view(), name='cafe-create'),
    path('style_cafe/<int:pk>/', views.CafeDetailView.as_view(), name='style-cafe-detail'),
    path('style_cafe/<int:pk>/edit/', views.CafeUpdateView.as_view(), name='style-cafe-update'),
    path('style_cafe/<int:pk>/delete/', views.CafeDeleteView.as_view(), name='style-cafe-delete'),
    path('style_search/', views.SearchView.as_view(), name='search'),
    path('style_cafe/following/', views.FollowingReviewListView.as_view(), name='style-following-review-list'),

    # profile
    path('users/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('users/<int:user_id>/reviews/', views.UserReviewListView.as_view(), name='user-review-list'),
    path('set-profile/', views.ProfileSetView.as_view(), name='profile-set'),
    path('edit-profile/', views.ProfileUpdateView.as_view(), name='profile-update'),


     path('users/<int:pk>/liked-cafes/', views.LikedCafeListView.as_view(), name='liked-cafe-list'),
    path('users/<int:pk>/liked-dripshots/', views.LikedDripshotListView.as_view(), name='liked-dripshot-list'),


    # dripshot
   # path('dripshot/',views.DripshotListView.as_view(),name='dripshot-list'),
   # path('dripshot/list/',views.DripshotMainListView.as_view(),name='dripshot-main-list'), # 여기까지 만듬 
   # path('cafes/<int:cafe_id>/', views.DripshotDetailView.as_view(), name='dripshot-detail'),
   # path('cafes/new/', views.DripshotCreateView.as_view(), name='dripshot-create'),
   # path('cafes/<int:review_id>/edit/', views.DripshotUpdateView.as_view(), name='dripshot-update'),
   # path('cafes/<int:cafe_id>/delete/', views.DripshotDeleteView.as_view(), name='dripshot-delete'),
   # path('cafes/following/', views.FollowingReviewListView.as_view(), name='following-review-list'),
    path('dripshot/', views.DripshotListView.as_view(), name='dripshot-list'),
    path('dripshot/list/', views.DripshotMainListView.as_view(), name='dripshot-main-list'),
    path('dripshot/<int:dripshot_id>/', views.DripshotDetailView.as_view(), name='dripshot-detail'),
    path('dripshot/new/', views.DripshotCreateView.as_view(), name='dripshot-create'),
    path('dripshot/<int:dripshot_id>/edit/', views.DripshotUpdateView.as_view(), name='dripshot-update'),
    path('dripshot/<int:dripshot_id>/delete/', views.DripshotDeleteView.as_view(), name='dripshot-delete'),
    # around 
    path('around/',views.CafeAroundListView.as_view(),name='around-list'), 
    path('around/list',views.CafeAroundMainListView.as_view(),name='around-main-list'),
    # path('cafes/<int:cafe_id>/', views.ReviewDetailView.as_view(), name='around-detail'),
    # path('cafes/new/', views.ReviewCreateView.as_view(), name='around-create'),
    # path('cafes/<int:review_id>/edit/', views.ReviewUpdateView.as_view(), name='around-update'),
    # path('cafes/<int:cafe_id>/delete/', views.ReviewDeleteView.as_view(), name='around-delete'),
    path('cafes/following/', views.FollowingReviewListView.as_view(), name='following-review-list'),

    #js
    path('cafe-autocomplete/', views.cafe_autocomplete, name='cafe-autocomplete'),


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
