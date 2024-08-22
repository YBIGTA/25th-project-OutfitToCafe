from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import os

def cafe_pic_upload_to(instance, filename):
    new_filename = filename.replace(" ", "_")
    return f'cafe_images/{instance.id}_{instance.name}_images/{new_filename}'

def dripshot_pic_upload_to(instance, filename):
    return f'user_pic/{filename}'

def person_pic_upload_to(instance, filename):
    return f'person/{filename}'

def cafe_image_upload_to(instance, filename):
    # 카페 이름을 포함한 폴더에 이미지를 저장
    folder_name = f"{instance.id}_{instance.name}_images"
    return os.path.join('cafe_images', folder_name, filename)

class StyleKeyword(models.Model):
    keyword = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.keyword

# class CafeKeyword(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.name
def person_pic_upload_to(instance, filename):
    # 파일이 저장될 경로를 정의
    return f'user_pics/{filename}'


class User(AbstractUser):
    name = models.CharField(max_length=15, null=False, default='Unknown', error_messages={"null": "이름을 입력해주세요."})
    profile_pic = models.FileField(upload_to='profile_pics', default='default_profile_pic.jpg')
    GENDER_CHOICES = [
        (1, "남자"),
        (2, "여자")
    ]
    birth_date = models.DateField(null=True, blank=True, error_messages={"null": "생년월일을 입력해주세요."})
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    recommend_location = models.CharField(max_length=100, error_messages={"null": "존재하지 않는 역입니다."})
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')
    style_keywords = models.ManyToManyField(StyleKeyword, related_name='users', blank=True)
    uploaded_image = models.ImageField(upload_to='uploaded_images/', null=True, blank=True)
    classification_result = models.JSONField(null=True, blank=True)  # 분류 결과를 JSON 형식으로 저장
    def __str__(self):
        return self.email

class Cafe(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address_url = models.URLField(null=True)
    total_review = models.IntegerField(null=True)
    sns_link = models.URLField(null=True)
    image1 = models.ImageField(upload_to=cafe_image_upload_to, blank=True)
    image2 = models.ImageField(upload_to=cafe_image_upload_to, blank=True)
    image3 = models.ImageField(upload_to=cafe_image_upload_to, blank=True)
    image4 = models.ImageField(upload_to=cafe_image_upload_to, blank=True)
    image5 = models.ImageField(upload_to=cafe_image_upload_to, blank=True)
    rating = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    short_description = models.CharField(max_length=500)
    content = models.TextField(max_length=500, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cafes')
    likes = GenericRelation('Like', related_query_name='dripshot')
    style_keywords = models.ManyToManyField(StyleKeyword, blank=True, related_name='cafes')  # Added this line
    comments = GenericRelation('Comment', related_query_name='cafes')

    def __str__(self):
        return self.name


class Dripshot(models.Model):
    title = models.CharField(max_length=50)
    image1 = models.FileField(upload_to=dripshot_pic_upload_to, blank=False)
    image1_url = models.URLField(blank=False)
    image2 = models.FileField(upload_to=dripshot_pic_upload_to, blank=True)
    image2_url = models.URLField(blank=True)
    image3 = models.FileField(upload_to=dripshot_pic_upload_to, blank=True)
    image3_url = models.URLField(blank=True)
    image4 = models.FileField(upload_to=dripshot_pic_upload_to, blank=True)
    image4_url = models.URLField(blank=True)
    image5 = models.FileField(upload_to=dripshot_pic_upload_to, blank=True)
    image5_url = models.URLField(blank=True)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=500, blank=False)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='dripshots', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dripshot')
    likes = GenericRelation('Like', related_query_name='dripshot')
    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=None, null=True, blank=True)
    comments = GenericRelation('Comment', related_query_name='cafes')

    def __str__(self):
        return self.title 

class Like(models.Model):
    dt_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    liked_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"({self.user}, {self.liked_object})"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'content_type', 'object_id'], name='unique_like')
        ]

class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    likes = GenericRelation('Like', related_query_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.content[:30]

    class Meta:
        ordering = ['-dt_created']
