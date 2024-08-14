from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    View,
    ListView, 
    DetailView, 
    CreateView, 
    UpdateView, 
    DeleteView
)

from braces.views import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.contenttypes.models import ContentType
from allauth.account.views import PasswordChangeView
from .mixins import LoginAndverificationRequiredMixin ,LoginAndOwnershipRequiredMixin
from .models import Review, User , Comment , Like
from .forms import ReviewForm, ProfileForm ,CommentForm
from django.db.models import Q
class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['latest_reviews'] = Review.objects.all()[0:20] # index에 보여지는거 몇개 보내줄지 
        context['restaurant_names'] = Review.objects.values_list('restaurant_name', flat=True).distinct()[:9] 
        # 위에 코드를 빈도가 제일 많은 키워드로 검색되게 만들어야 함 > review_keyword라는 모델을 만들어서 거기서 제일 많이 빈출되는 단어 넣어주고 그거 뽑아오기 
        user = self.request.user
        if user.is_authenticated:
            context['latest_following_reviews'] = Review.objects.filter(author__followers=user)[:4]
        return render(request, 'coplate/index.html', context)

class FollowingReviewListView(LoginRequiredMixin, ListView):
    model = Review
    context_object_name = 'following_reviews'
    template_name = 'coplate/following_review_list.html'
    paginate_by = 8

    def get_queryset(self):
        return Review.objects.filter(author__followers=self.request.user)



class SearchView(ListView):
    model = Review
    context_object_name = 'search_results' # 해당 템플릿에서 search_results로 사용가능 
    template_name = 'coplate/search_result.html'
    paginate_by = 8 

    def get_queryset(self): # listview에서 보여줄 객체의 리스트를 반환하는 역할 
        query = self.request.GET.get('query','')
        return Review.objects.filter(
            Q(title__icontains=query) # icontains > 대소문자 구분없이 
            | Q(restaurant_name__icontains=query)
            | Q(content__icontains=query)
        )
    
    def get_context_data(self, **kwargs): # 템플릿에 전달할 추가적인 데이터 전달 
        context = super().get_context_data(**kwargs) # 이거는 사용자가 입력한 query도 같이 넘김 
        context['query'] = self.request.GET.get('query','')
        return context 

class ReviewListView(ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'coplate/review_list.html'
    paginate_by = 12

class ClothesListView(ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'coplate/clothes_list.html'
    paginate_by = 12
class ClothesMainListView(ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'coplate/clothes_main_list.html'
    paginate_by = 12

class CaffeAroundListView(ListView): # index 파일에 보이는거
    model = Review
    context_object_name = 'reviews'
    template_name = 'coplate/clothes_list.html'
    paginate_by = 8
class CaffeAroundMainListView(ListView):# 더보기 누르고 보이는 거 
    model = Review
    context_object_name = 'reviews'
    template_name = 'coplate/clothes_main_list.html'
    paginate_by = 8


class ReviewDetailView(DetailView):
    model = Review
    template_name = 'coplate/review_detail.html'
    pk_url_kwarg = 'review_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm() # 이렇게 하면 detail.html에서 form.comment 이런식으로 접근가능 
        context['review_ctype_id'] = ContentType.objects.get(model='review').id
        context['comment_ctype_id'] = ContentType.objects.get(model='comment').id

        user = self.request.user
        if user.is_authenticated :
            review = self.object
            context['likes_review'] = Like.objects.filter(user=user, review=review).exists()
            context['liked_comments'] = Comment.objects.filter(review=review).filter(likes__user=user)

        return context 


class ReviewCreateView(LoginAndverificationRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'coplate/review_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('review-detail', kwargs={'review_id': self.object.id})
 

class ReviewUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'coplate/review_form.html'
    pk_url_kwarg = 'review_id'

    redirect_unauthenticated_users = False
    raise_exception = True

    def get_success_url(self):
        return reverse('review-detail', kwargs={'review_id': self.object.id})

    def test_func(self, user):
        review = self.get_object()
        return review.author == user


# 이미 detail 부분에 다 보내놓고 (좋아요와 댓글할 수 있는거를 ) > url설정 해 놓고 > 그 칸을 클릭하고 그 안에 값을 
# 넣으면 이게 실행이되서 다시 값이 보이게 되는거 
    # url이 두가지 기능인거 같은데 하나는 직접 html에 연결해주는거랑 하나는 기능을 연결해주는거 view를 실행시켜주는 
    # 아닌가 url을 설정하는 이유가 뭐지 

class CommentCreateView(LoginAndverificationRequiredMixin, CreateView):
    http_method_names = ['post']
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.review = Review.objects.get(id=self.kwargs.get('review_id'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('review-detail', kwargs={'review_id':self.object.id})

class CommentUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'coplate/comment_update_form.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('review-detail', kwargs={'review_id': self.object.review.id})


class CommentDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Comment
    template_name = 'coplate/comment_confirm_delete.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('review-detail', kwargs={'review_id': self.object.review.id})


class ReviewDeleteView(LoginAndOwnershipRequiredMixin,DeleteView):
    model = Review
    template_name = 'coplate/review_confirm_delete.html'
    pk_url_kwarg = 'review_id'

    def get_success_url(self):
        return reverse('index') 

    def test_func(self, user):
        review = self.get_object()
        return review.author == user

class ProcessLikeView(LoginAndverificationRequiredMixin, View):
    http_method_names = ['post'] # post만 처리 되게 끔 
    # args 위치 인자 들의 튜플을 의미 함수에 몇개의 인자가 전달될지 알 수 없을 때 > 튜플로 묶어줌 
    # 키워드 인자가 들의 딕셔너리 > 마찬가지로 알 수 없을 때 딕셔너리로 묶어줌 
    # 동시에 사용하면 위치 인자 , 키워드 인자 모두 받을 수 있음 
    # example_function(1, 2, 3, a=4, b=5) 이런식으로 
    def post(self, request, *args, **kwargs): # post에 대한 정의 
        like, created = Like.objects.get_or_create( # 객체가 없다면 생성 
            user=self.request.user, # 이련식으로 
            content_type_id = self.kwargs.get('content_type_id'),
            object_id = self.kwargs.get('object_id')
        )
        if not created:
            like.delete()
        
        return redirect(self.request.META['HTTP_REFERER']) # 요청이 들어온 페이지 url을 참조하여 다시 보냄 


class ProfileView(DetailView):
    model = User
    template_name = 'coplate/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile_user_id = self.kwargs.get('user_id')
        if user.is_authenticated :
            context['is_following']=user.following.filter(id=profile_user_id).exists()
        context['user_reviews'] = Review.objects.filter(author_id=profile_user_id)[:4]
        return context


class ProcessFollowView(LoginAndverificationRequiredMixin, View):
    http_method_names = ['post']

    def post(self,request, *args, **kwargs):
        user = self.request.user
        profile_user_id = self.kwargs.get('user_id')
        if user.following.filter(id=profile_user_id).exists():
            user.following.remove(profile_user_id)
        else :
            user.following.add(profile_user_id)
        return redirect('profile',user_id=profile_user_id)

class UserReviewListView(ListView):
    model = Review
    template_name = 'coplate/user_review_list.html'
    context_object_name = 'user_reviews'
    paginate_by = 4

    def get_queryset(self):
        return Review.objects.filter(author__id=self.kwargs.get('user_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, id=self.kwargs.get('user_id'))
        return context



class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'coplate/profile_set_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('index')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'coplate/profile_update_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('profile', kwargs={'user_id': self.request.user.id})


class FollowingListView(ListView):
    model = User
    template_name = 'coplate/following_list.html'
    context_object_name = 'following'
    paginate_by = 10

    def get_queryset(self):
        profile_user = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        return profile_user.following.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user_id'] = self.kwargs.get('user_id')
        return context


class FollowerListView(ListView):
    model = User
    template_name = 'coplate/follower_list.html'
    context_object_name = 'followers'
    paginate_by = 10

    def get_queryset(self):
        profile_user = get_object_or_404(User, pk=self.kwargs.get('user_id'))
        return profile_user.followers.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user_id'] = self.kwargs.get('user_id')
        return context
