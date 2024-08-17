from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .validators import validate_no_special_characters, validate_restaurant_link


def caffe_pic_upload_to(instance, filename):
    return f'caffe/{filename}'

def dripshot_pic_upload_to(instance, filename):
    return f'user_pic/{filename}'

def person_pic_upload_to(instance, filename):
    return f'person/{filename}'

class StyleKeyword(models.Model):
    keyword = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.keyword

class CaffeKeyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    
class User(AbstractUser):
    name = models.CharField(max_length=15, null=False, error_messages={"null": "이름을 입력해주세요."})
    profile_pic = models.FileField(upload_to=person_pic_upload_to, blank=True, null=True, default='user_pics/default_profile_pic.jpg')
    profile_pic_url = models.URLField(blank=True, default='https://yonfen.s3.amazonaws.com/default_profile_pic.jpg')
    GENDER_CHOICES = [
        (1, "남자"),
        (2, "여자")
    ]
    age = models.IntegerField(null=False, error_messages={"null": "나이를 입력해주세요."})
    gender = models.IntegerField(choices=GENDER_CHOICES, default=None)
    style_keywords = models.ManyToManyField('StyleKeyword', related_name='users')
    location = models.CharField(max_length=100, null=False, error_messages={"null": "추천장소를 입력해주세요."})
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')

    def __str__(self):
        return self.email

class Caffe(models.Model):
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100, null=False)
    location_url = models.URLField()
    instagram_url = models.URLField(null=True)
    image1 = models.FileField(upload_to=caffe_pic_upload_to, blank=False)
    image1_url = models.URLField(blank=False)
    image2 = models.FileField(upload_to=caffe_pic_upload_to, blank=True)
    image2_url = models.URLField(blank=True)
    image3 = models.FileField(upload_to=caffe_pic_upload_to, blank=True)
    image3_url = models.URLField(blank=True)
    image4 = models.FileField(upload_to=caffe_pic_upload_to, blank=True)
    image4_url = models.URLField(blank=True)
    image5 = models.FileField(upload_to=caffe_pic_upload_to, blank=True)
    image5_url = models.URLField(blank=True)
    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES,blank=False,null=False)
    content = models.TextField(max_length=500, blank=False)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    caffe_keywords = models.ManyToManyField(CaffeKeyword, related_name='caffes', blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caffes')
    likes = GenericRelation('Like', related_query_name='caffes')
    style_keywords = models.ManyToManyField('StyleKeyword', related_name='caffes')

class Dripshot(models.Model):
    title = models.CharField(max_length=50, null=False)
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
    style_keywords = models.ManyToManyField('StyleKeyword', related_name='dripshots')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dripshot')
    likes = GenericRelation('Like', related_query_name='dripshot')

class Like(models.Model):
    dt_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    liked_object = GenericForeignKey()

    def __str__(self):
        return f"({self.user}, {self.liked_object})"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'content_type', 'object_id'], name='unique_like')
        ]

# 댓글(Comment) 모델
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