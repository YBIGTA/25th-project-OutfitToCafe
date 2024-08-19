from typing import Any
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .utils import upload_file_to_s3  # S3 업로드 유틸리티 함수 임포트
from django.conf import settings

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
from .models import *
from .forms import *
from django.db.models import Q,Count
from django.http import JsonResponse

class CafeAutocomplete(View):
    def get(self, request, *args, **kwargs):
        if 'term' in request.GET:
            qs = Cafe.objects.filter(name__icontains=request.GET.get('term'))
            names = list(qs.values_list('name', flat=True))
            return JsonResponse(names, safe=False)
        return JsonResponse([], safe=False)
class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}

        # 드립샷 리뷰 가져오기
        context['drip_shot_review'] = Dripshot.objects.all()[0:20]

        # 키워드 빈도순으로 가져오기
        context['cafe_keywords'] = Cafe.objects.values_list('cafe_keywords', flat=True).distinct()[:9]

        # 현재 로그인한 사용자
        user = self.request.user

        if user.is_authenticated:
            # 사용자의 스타일 키워드 가져오기
            user_keywords = user.style_keywords.all()

            # Q 객체를 사용하여 조건 생성
            query = Q()
            for keyword in user_keywords:
                query |= Q(style_keywords=keyword)
            
            # 2개 이상의 키워드가 일치하는 카페 필터링
            matching_cafes = Cafe.objects.filter(query).annotate(
                matching_keywords_count=Count('style_keywords')
            ).filter(matching_keywords_count__gte=2).distinct()

            context['matching_cafes'] = matching_cafes

            # 사용자가 팔로우한 작성자의 최신 리뷰 가져오기
            context['latest_following_reviews'] = Cafe.objects.filter(author__followers=user)[:4]

            # 사용자의 추천 위치와 일치하는 주변 카페 필터링
            if user.recommend_location:
                nearby_cafes = Cafe.objects.filter(location__icontains=user.recommend_location)
                context['nearby_cafes'] = nearby_cafes
        
        return render(request, 'coplate/index.html', context)
    
class FollowingReviewListView(LoginRequiredMixin, ListView):
    model = Cafe
    context_object_name = 'following_reviews'
    template_name = 'coplate/following_review_list.html'
    paginate_by = 8

    def get_queryset(self):
        return Cafe.objects.filter(author__followers=self.request.user)



class SearchView(ListView):
    model = Cafe
    context_object_name = 'search_results' # 해당 템플릿에서 search_results로 사용가능 
    template_name = 'coplate/search_result.html'
    paginate_by = 8 

    def get_queryset(self): # listview에서 보여줄 객체의 리스트를 반환하는 역할 
        query = self.request.GET.get('query','')
        return Cafe.objects.filter(
            Q(title__icontains=query) # icontains > 대소문자 구분없이 
            | Q(restaurant_name__icontains=query)
            | Q(content__icontains=query)
        )
    
    def get_context_data(self, **kwargs): # 템플릿에 전달할 추가적인 데이터 전달 
        context = super().get_context_data(**kwargs) # 이거는 사용자가 입력한 query도 같이 넘김 
        context['query'] = self.request.GET.get('query','')
        return context 

class Style_CafeListView(ListView):
    model = Cafe
    context_object_name = 'style_cafe'
    template_name = 'coplate/style_cafe_list.html'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user

        # 사용자가 선택한 스타일 키워드 가져오기
        user_keywords = user.style_keywords.all()

        # Q 객체를 사용하여 카페를 필터링
        query = Q()
        for keyword in user_keywords:
            query |= Q(style_keywords=keyword)

        # 사용자의 스타일 키워드 중 하나라도 일치하는 카페를 반환
        return Cafe.objects.filter(query).distinct()

class Style_CafeMainListView(ListView):
    model = Cafe
    context_object_name = 'style_cafe'
    template_name = 'coplate/style_cafe_main_list.html'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user

        # 사용자가 선택한 스타일 키워드 가져오기
        user_keywords = user.style_keywords.all()

        # Q 객체를 사용하여 카페를 필터링
        query = Q()
        for keyword in user_keywords:
            query |= Q(style_keywords=keyword)

        # 사용자의 스타일 키워드 중 하나라도 일치하는 카페를 반환
        return Cafe.objects.filter(query).distinct()


class CafeDetailView(DetailView): 
    model = Cafe
    template_name = 'coplate/cafe_detail.html'
    pk_url_kwarg = 'cafe_id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['cafe_ctype_id'] = ContentType.objects.get(model='cafe').id
        context['comment_ctype_id'] = ContentType.objects.get(model='comment').id

        user = self.request.user
        if user.is_authenticated:
            cafe = self.object
            context['likes_cafe'] = Like.objects.filter(user=user, content_type=context['cafe_ctype_id'], object_id=cafe.id).exists()
            context['liked_comments'] = Comment.objects.filter(cafe=cafe).filter(likes__user=user)

        return context

class CafeListView(ListView):
    model = Cafe
    context_object_name = 'cafe'
    template_name = 'coplate/cafe_list.html'
    paginate_by = 12


class DripshotListView(ListView):
    model = Dripshot
    context_object_name = 'dripshot'
    template_name = 'coplate/dripshot_list.html'
    paginate_by = 12


class DripshotMainListView(ListView):
    model = Dripshot
    context_object_name = 'dripshot'
    template_name = 'coplate/dripshot_main_list.html'
    paginate_by = 12

class DripshotDetailView(DetailView):
    model = Dripshot
    template_name = 'coplate/dripshot_detail.html'
    pk_url_kwarg = 'dripshot_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm() # 이렇게 하면 detail.html에서 form.comment 이런식으로 접근가능 
        context['dripshot_ctype_id'] = ContentType.objects.get(model='dripshot').id
        context['comment_ctype_id'] = ContentType.objects.get(model='comment').id

        user = self.request.user
        if user.is_authenticated :
            dripshot = self.object
            context['dripshot_review'] = Like.objects.filter(user=user, dripshot=dripshot).exists()
            context['liked_comments'] = Comment.objects.filter(dripshot=dripshot).filter(likes__user=user)

        return context 


class DripshotCreateView(LoginAndverificationRequiredMixin, CreateView):
    model = Dripshot
    form_class = DripshotForm
    template_name = 'coplate/dripshot_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        # 이미지 필드 목록
        image_fields = ['image1', 'image2', 'image3', 'image4','image5']

        for image_field in image_fields:
            image = self.request.FILES.get(image_field)
            if image:
                # S3에 파일 업로드하고 URL을 모델 필드에 저장
                image_url = upload_file_to_s3(image, settings.AWS_STORAGE_BUCKET_NAME, 'drip-shot')
                setattr(form.instance, f"{image_field}_url", image_url)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dripshot-detail', kwargs={'dripshot_id': self.object.id})

class DripshotDeleteView(LoginAndOwnershipRequiredMixin,DeleteView):
    model = Dripshot
    template_name = 'coplate/dripshot_confirm_delete.html'
    pk_url_kwarg = 'dripshot_id'

    def get_success_url(self):
        return reverse('index') 

    def test_func(self, user):
        cafe = self.get_object()
        return cafe.author == user

    
class DripshotUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Dripshot
    form_class = DripshotForm
    template_name = 'coplate/dripshot_form.html'
    pk_url_kwarg = 'dripshot_id'

    redirect_unauthenticated_users = False
    raise_exception = True

    def get_success_url(self):
        return reverse('dripshot-detail', kwargs={'dripshot_id': self.object.id})

    def test_func(self, user):
        cafe = self.get_object()
        return cafe.author == user 


class CafeAroundListView(ListView): # index 파일에 보이는거
    model = Cafe
    context_object_name = 'caffes'
    template_name = 'coplate/around_list.html'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.recommend_location:
            recommend_location = user.recommend_location
            return Cafe.objects.filter(location__icontains=recommend_location)
        else:
            return Cafe.objects.none()  # 추천 장소가 없으면 빈 쿼리셋 반환
        
class CafeAroundMainListView(ListView):# 더보기 누르고 보이는 거 
    model = Cafe
    context_object_name = 'cafes'
    template_name = 'coplate/around_main_list.html'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.recommend_location:
            recommend_location = user.recommend_location
            return Cafe.objects.filter(location__icontains=recommend_location)
        else:
            return Cafe.objects.none()  # 추천 장소가 없으면 빈 쿼리셋 반환


class CafeCreateView(LoginAndverificationRequiredMixin, CreateView):
    model = Cafe
    form_class = CafeForm
    template_name = 'coplate/cafe_form.html'
    # 버튼을 클릭하면 이 url로 가고 성공하면 밑에 url로 감 
    # form_valid 는 폼이 유효하면 실행됨 
    def form_valid(self, form):
        form.instance.author = self.request.user

        # 이미지 필드 목록
        image_fields = ['image1', 'image2', 'image3', 'image4','image5']

        for image_field in image_fields:
            image = self.request.FILES.get(image_field)
            if image:
                # S3에 파일 업로드하고 URL을 모델 필드에 저장
                image_url = upload_file_to_s3(image, settings.AWS_STORAGE_BUCKET_NAME, 'drip-shot')
                setattr(form.instance, f"{image_field}_url", image_url)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cafe-detail', kwargs={'cafe_id': self.object.id})
        
class CafeDetailView(DetailView):
    model = Cafe
    template_name = 'coplate/cafe_detail.html'
    pk_url_kwarg = 'cafe_id'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['cafe_ctype_id'] = ContentType.objects.get(model='cafe').id
        context['comment_ctype_id'] = ContentType.objects.get(model='comment').id

        user = self.request.user
        if user.is_authenticated:
            cafe = self.object
            context['likes_cafe'] = Like.objects.filter(user=user, content_type=context['cafe_ctype_id'], object_id=cafe.id).exists()
            context['liked_comments'] = Comment.objects.filter(cafe=cafe).filter(likes__user=user)

        return context

# class CaffeDetailView(DetailView):
#     model = Caffe
#     template_name = 'coplate/review_detail.html'
#     pk_url_kwarg = 'caffe_id'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = CommentForm() # 이렇게 하면 detail.html에서 form.comment 이런식으로 접근가능 
#         context['caffe_ctype_id'] = ContentType.objects.get(model='caffe').id
#         context['comment_ctype_id'] = ContentType.objects.get(model='comment').id

#         user = self.request.user
#         if user.is_authenticated :
#             caffe = self.object
#             context['likes_caffe'] = Like.objects.filter(user=user, caffe=caffe).exists()
#             context['liked_comments'] = Comment.objects.filter(caffe=caffe).filter(likes__user=user)

#         return context 


# class ReviewCreateView(LoginAndverificationRequiredMixin, CreateView):
#     model = Review
#     form_class = ReviewForm
#     template_name = 'coplate/review_form.html'

#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('review-detail', kwargs={'review_id': self.object.id})
 
# class CaffeDetailView(DetailView):
#     model = Caffe
#     template_name = 'coplate/review_detail.html'
#     pk_url_kwarg = 'caffe_id'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = CommentForm()
#         context['caffe_ctype_id'] = ContentType.objects.get(model='caffe').id
#         context['comment_ctype_id'] = ContentType.objects.get(model='comment').id

#         user = self.request.user
#         if user.is_authenticated:
#             caffe = self.object
#             context['likes_caffe'] = Like.objects.filter(user=user, content_type=context['caffe_ctype_id'], object_id=caffe.id).exists()
#             context['liked_comments'] = Comment.objects.filter(caffe=caffe).filter(likes__user=user)

#         return context


class CafeDeleteView(LoginAndOwnershipRequiredMixin,DeleteView):
    model = Cafe
    template_name = 'coplate/cafe_confirm_delete.html'
    pk_url_kwarg = 'cafe_id'

    def get_success_url(self):
        return reverse('index') 

    def test_func(self, user):
        cafe = self.get_object()
        return cafe.author == user

    
class CafeUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Cafe
    form_class = CafeForm
    template_name = 'coplate/cafe_form.html'
    pk_url_kwarg = 'cafe_id'

    redirect_unauthenticated_users = False
    raise_exception = True

    def get_success_url(self):
        return reverse('cafe-detail', kwargs={'cafe_id': self.object.id})

    def test_func(self, user):
        cafe = self.get_object()
        return cafe.author == user


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
        form.instance.review = Cafe.objects.get(id=self.kwargs.get('review_id'))
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
        context['user_reviews'] = Cafe.objects.filter(author_id=profile_user_id)[:4]
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
    model = Cafe
    template_name = 'coplate/user_review_list.html'
    context_object_name = 'user_reviews'
    paginate_by = 4

    def get_queryset(self):
        return Cafe.objects.filter(author__id=self.kwargs.get('user_id'))

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




class CafeCreateView(LoginAndverificationRequiredMixin, CreateView):
    model = Cafe
    form_class = CafeForm
    template_name = 'coplate/cafe_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        # 이미지 필드 목록
        image_fields = ['image1', 'image2', 'image3', 'image4']

        for image_field in image_fields:
            image = self.request.FILES.get(image_field)
            if image:
                # S3에 파일 업로드하고 URL을 모델 필드에 저장
                image_url = upload_file_to_s3(image, settings.AWS_STORAGE_BUCKET_NAME, 'drip-shot')
                setattr(form.instance, f"{image_field}_url", image_url)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cafe-detail', kwargs={'cafe_id': self.object.id})
    


class CafeUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Cafe
    form_class = CafeForm
    template_name = 'coplate/cafe_form.html'
    pk_url_kwarg = 'cafe_id'

    redirect_unauthenticated_users = False
    raise_exception = True

    def get_success_url(self):
        return reverse('cafe-detail', kwargs={'cafe_id': self.object.id})

    def test_func(self, user):
        cafe = self.get_object()
        return cafe.author == user
    
class CafeDeleteView(LoginAndOwnershipRequiredMixin,DeleteView):
    model = Cafe
    template_name = 'coplate/cafe_confirm_delete.html'
    pk_url_kwarg = 'cafe_id'

    def get_success_url(self):
        return reverse('index') 

    def test_func(self, user):
        cafe = self.get_object()
        return cafe.author == user
