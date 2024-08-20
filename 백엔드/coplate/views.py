from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
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
from django.db.models import Q, Count
from django.http import JsonResponse
from django.http import HttpResponse


from django.contrib.contenttypes.models import ContentType

class LikedCafeListView(ListView):
    model = Cafe
    template_name = 'coplate/liked_cafe_list.html'
    context_object_name = 'cafes'

    def get_queryset(self):
        user = self.request.user
        content_type = ContentType.objects.get_for_model(Cafe)
        return Cafe.objects.filter(
            likes__user=user,
            likes__content_type=content_type
        ).distinct()

class LikedDripshotListView(ListView):
    model = Dripshot
    template_name = 'coplate/liked_dripshot_list.html'
    context_object_name = 'dripshots'

    def get_queryset(self):
        user = self.request.user
        content_type = ContentType.objects.get_for_model(Dripshot)
        return Dripshot.objects.filter(
            likes__user=user,
            likes__content_type=content_type
        ).distinct()
# class DripshotListView(View):
#     def get(self, request, *args, **kwargs):
#         dripshots = Dripshot.objects.all()
#         return render(request, 'dripshot_list.html', {'dripshots': dripshots})
def cafe_autocomplete(request):
    if 'term' in request.GET:
        # 입력된 term 값으로 카페 이름을 검색합니다.
        qs = Cafe.objects.filter(name__icontains=request.GET.get('term'))
        # 검색 결과에서 이름만 추출하여 리스트로 만듭니다.
        names = list(qs.values_list('name', flat=True))
        # JSON 형식으로 반환합니다.
        return JsonResponse(names, safe=False)
    return JsonResponse([], safe=False)

class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {}

        # 드립샷 리뷰 가져오기
        context['drip_shot_review'] = Dripshot.objects.all()[:10]

        # 현재 로그인한 사용자
        user = self.request.user

        if user.is_authenticated:
            # 사용자의 스타일 키워드 가져오기
            user_keywords = user.style_keywords.all()
            context['user_keywords'] = user_keywords  # 스타일 키워드를 컨텍스트에 추가

            # 사용자의 스타일 키워드와 일치하는 카페들 가져오기
            style_cafe = Cafe.objects.filter(style_keywords__in=user_keywords).distinct()
            context['style_cafe'] = style_cafe

            # 사용자가 팔로우한 작성자의 최신 리뷰 가져오기
            context['latest_reviews'] = Cafe.objects.filter(author__followers=user)[:4]

            # 사용자의 추천 위치와 일치하는 주변 카페 필터링
            if user.recommend_location:
                nearby_cafes = Cafe.objects.filter(address__icontains=user.recommend_location)
                context['cafes'] = nearby_cafes

        return render(request, 'coplate/index.html', context)
class FollowingReviewListView(LoginRequiredMixin, ListView):
    model = Cafe
    context_object_name = 'following_cafe'
    template_name = 'coplate/following_cafe_list.html'
    paginate_by = 8

    def get_queryset(self):
        return Cafe.objects.filter(author__followers=self.request.user)

class SearchView(ListView):
    model = Cafe
    context_object_name = 'search_results'
    template_name = 'coplate/search_result.html'
    paginate_by = 8

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Cafe.objects.filter(
            Q(name__icontains=query) |
            Q(address__icontains=query) |
            Q(content__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        return context

class Style_CafeListView(ListView):
    model = Cafe
    context_object_name = 'style_cafe'
    template_name = 'coplate/style_cafe_list.html'
    paginate_by = 8

    def get_queryset(self):
        user = self.request.user

        # 사용자가 선택한 스타일 키워드 가져오기
        user_keywords = StyleKeyword.objects.filter(style_keywords__user=user)

        # Q 객체를 사용하여 카페를 필터링
        query = Q()
        for keyword in user_keywords:
            query |= Q(cafestylekeyword__style_keyword=keyword)

        # 쿼리셋을 필터링하고 전체 항목을 반환
        queryset = Cafe.objects.filter(query).distinct()
        return queryset[:20]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 페이지네이션에 맞게 데이터 제공
        context['style_cafe'] = self.get_queryset()
        return context

class Style_CafeMainListView(ListView):
    model = Cafe
    context_object_name = 'style_cafe'
    template_name = 'coplate/style_cafe_main_list.html'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user

        # 사용자가 선택한 스타일 키워드 가져오기
        user_keywords = StyleKeyword.objects.filter(style_keywords__user=user)

        # Q 객체를 사용하여 카페를 필터링
        query = Q()
        for keyword in user_keywords:
            query |= Q(cafestylekeyword__style_keyword=keyword)

        return Cafe.objects.filter(query).distinct()

# class CafeDetailView(DetailView): 
#     model = Cafe
#     template_name = 'coplate/cafe_detail.html'
#     pk_url_kwarg = 'cafe_id'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = CommentForm()
#         context['cafe_ctype_id'] = ContentType.objects.get(model='cafe').id
#         context['comment_ctype_id'] = ContentType.objects.get(model='comment').id

#         user = self.request.user
#         if user.is_authenticated:
#             cafe = self.object
#             context['likes_cafe'] = Like.objects.filter(user=user, content_type=context['cafe_ctype_id'], object_id=cafe.id).exists()
#             # 수정된 부분: `cafe` 필드 대신 `content_object` 사용
#             context['liked_comments'] = Comment.objects.filter(
#                 content_type=context['cafe_ctype_id'], 
#                 object_id=cafe.id
#             ).filter(likes__user=user)

#         return context

class CafeDetailView(DetailView):
    model = Cafe
    template_name = 'coplate/cafe_detail.html'
    pk_url_kwarg = 'pk'  # URL에서 사용하는 인자와 일치하도록 설정

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['cafe_ctype_id'] = ContentType.objects.get(model='cafe').id
        context['comment_ctype_id'] = ContentType.objects.get(model='comment').id

        user = self.request.user
        if user.is_authenticated:
            cafe = self.object
            context['likes_cafe'] = Like.objects.filter(user=user, content_type=context['cafe_ctype_id'], object_id=cafe.id).exists()
            # 수정된 부분: `cafe` 필드 대신 `content_object` 사용
            context['liked_comments'] = Comment.objects.filter(
                content_type=context['cafe_ctype_id'], 
                object_id=cafe.id
            ).filter(likes__user=user)

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
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['dripshot_ctype_id'] = ContentType.objects.get(model='dripshot').id
        context['comment_ctype_id'] = ContentType.objects.get(model='comment').id

        user = self.request.user
        if user.is_authenticated:
            dripshot = self.object
            context['dripshot_review'] = dripshot.likes.filter(user=user).exists()
            context['liked_comments'] = Comment.objects.filter(dripshot=dripshot).filter(likes__user=user)

        return context

class DripshotCreateView(LoginAndverificationRequiredMixin, CreateView):
    model = Dripshot
    form_class = DripshotForm
    template_name = 'coplate/dripshot_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        # 이미지 필드 목록
        image_fields = ['image1', 'image2', 'image3', 'image4', 'image5']

        for image_field in image_fields:
            image = self.request.FILES.get(image_field)
            if image:
                setattr(form.instance, image_field, image)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dripshot-detail', kwargs={'pk': self.object.id})

class DripshotDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Dripshot
    template_name = 'coplate/dripshot_confirm_delete.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('index')

    def test_func(self, user):
        cafe = self.get_object()
        return cafe.author == user

class DripshotUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Dripshot
    form_class = DripshotForm
    template_name = 'coplate/dripshot_form.html'
    pk_url_kwarg = 'pk'

    redirect_unauthenticated_users = False
    raise_exception = True

    def get_success_url(self):
        return reverse('dripshot-detail', kwargs={'pk': self.object.id})

    def test_func(self, user):
        cafe = self.get_object()
        return cafe.author == user

class CafeAroundListView(ListView):
    model = Cafe
    context_object_name = 'caffes'
    template_name = 'coplate/around_list.html'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.recommend_location:
            recommend_location = user.recommend_location
            return Cafe.objects.filter(address__icontains=recommend_location)
        else:
            return Cafe.objects.none()

class CafeAroundMainListView(ListView):
    model = Cafe
    context_object_name = 'cafes'
    template_name = 'coplate/around_main_list.html'
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.recommend_location:
            recommend_location = user.recommend_location
            return Cafe.objects.filter(address__icontains(recommend_location))
        else:
            return Cafe.objects.none()

class CafeCreateView(LoginAndverificationRequiredMixin, CreateView):
    model = Cafe
    form_class = CafeForm
    template_name = 'coplate/cafe_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user

        # 이미지 필드 목록
        image_fields = ['image1', 'image2', 'image3', 'image4', 'image5']

        for image_field in image_fields:
            image = self.request.FILES.get(image_field)
            if image:
                setattr(form.instance, image_field, image)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cafe-detail', kwargs={'pk': self.object.id})

class CafeDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Cafe
    template_name = 'coplate/cafe_confirm_delete.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('index')

    def test_func(self, user):
        cafe = self.get_object()
        return cafe.author == user

class CafeUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Cafe
    form_class = CafeForm
    template_name = 'coplate/cafe_form.html'
    pk_url_kwarg = 'pk'

    redirect_unauthenticated_users = False
    raise_exception = True

    def get_success_url(self):
        return reverse('cafe-detail', kwargs={'pk': self.object.id})

    def test_func(self, user):
        cafe = self.get_object()
        return cafe.author == user

class CommentCreateView(LoginAndverificationRequiredMixin, CreateView):
    http_method_names = ['post']
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.review = Cafe.objects.get(id=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('review-detail', kwargs={'pk': self.object.id})

class CommentUpdateView(LoginAndOwnershipRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'coplate/comment_update_form.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('review-detail', kwargs={'pk': self.object.review.id})

class CommentDeleteView(LoginAndOwnershipRequiredMixin, DeleteView):
    model = Comment
    template_name = 'coplate/comment_confirm_delete.html'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse('review-detail', kwargs={'pk': self.object.review.id})

class ProcessLikeView(LoginAndverificationRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        like, created = Like.objects.get_or_create(
            user=self.request.user,
            content_type_id=self.kwargs.get('content_type_id'),
            object_id=self.kwargs.get('object_id')
        )
        if not created:
            like.delete()
        
        return redirect(self.request.META['HTTP_REFERER'])

class ProfileView(DetailView):
    model = User
    template_name = 'coplate/profile.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile_user_id = self.kwargs.get('pk')

        if user.is_authenticated:
            # 사용자 팔로우 여부
            context['is_following'] = user.following.filter(id=profile_user_id).exists()

            # 사용자가 좋아요를 누른 카페
            cafe_content_type = ContentType.objects.get_for_model(Cafe)
            context['liked_cafes'] = Cafe.objects.filter(
                likes__user=user,
                likes__content_type=cafe_content_type
            ).distinct()

            # 사용자가 좋아요를 누른 드립샷
            dripshot_content_type = ContentType.objects.get_for_model(Dripshot)
            context['liked_dripshots'] = Dripshot.objects.filter(
                likes__user=user,
                likes__content_type=dripshot_content_type
            ).distinct()

        # 사용자의 리뷰 (작성한 리뷰)
        context['user_reviews'] = Cafe.objects.filter(author_id=profile_user_id)[:4]

        return context

class ProcessFollowView(LoginAndverificationRequiredMixin, View):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        user = self.request.user
        profile_user_id = self.kwargs.get('pk')
        if user.following.filter(id=profile_user_id).exists():
            user.following.remove(profile_user_id)
        else:
            user.following.add(profile_user_id)
        return redirect('profile', user_id=profile_user_id)

class UserReviewListView(ListView):
    model = Cafe
    template_name = 'coplate/user_cafe_list.html'
    context_object_name = 'user_cafe'
    paginate_by = 4

    def get_queryset(self):
        return Cafe.objects.filter(author__id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user'] = get_object_or_404(User, id=self.kwargs.get('pk'))
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
        return reverse('profile', kwargs={'pk': self.request.user.id})
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.id})

class FollowingListView(ListView):
    model = User
    template_name = 'coplate/following_list.html'
    context_object_name = 'following'
    paginate_by = 10

    def get_queryset(self):
        profile_user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return profile_user.following.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user_id'] = self.kwargs.get('pk')
        return context

class FollowerListView(ListView):
    model = User
    template_name = 'coplate/follower_list.html'
    context_object_name = 'followers'
    paginate_by = 10

    def get_queryset(self):
        profile_user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        return profile_user.followers.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_user_id'] = self.kwargs.get('pk')
        return context
