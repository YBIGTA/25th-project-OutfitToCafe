from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType


def cafe_pic_upload_to(instance, filename):
    return f'cafe/{filename}'

def dripshot_pic_upload_to(instance, filename):
    return f'user_pic/{filename}'

def person_pic_upload_to(instance, filename):
    return f'person/{filename}'

class StyleKeyword(models.Model):
    keyword = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.keyword

class CafeKeyword(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    
class User(AbstractUser):
    name = models.CharField(max_length=15, null=False, default='Unknown',error_messages={"null": "이름을 입력해주세요."})
    profile_pic = models.FileField(upload_to=person_pic_upload_to, blank=True, null=True, default='user_pics/default_profile_pic.jpg')
    profile_pic_url = models.URLField(blank=True, default='https://yonfen.s3.amazonaws.com/default_profile_pic.jpg')
    GENDER_CHOICES = [
        (1, "남자"),
        (2, "여자")
    ]
    birth_date = models.DateField(null=True, blank=True, error_messages={"null": "생년월일을 입력해주세요."})
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    style_keywords = models.ManyToManyField('StyleKeyword', related_name='users')
    recommend_location = models.CharField(max_length=100, error_messages={"null": "존재하지 않는 역입니다."})
    following = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followers')

    def __str__(self):
        return self.email

class Cafe(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    address_url = models.URLField(null=True)
    total_review = models.IntegerField(null=True)
    sns_link = models.URLField(null=True)
    image1 = models.FileField(upload_to=cafe_pic_upload_to, blank=False)
    image1_url = models.URLField(blank=False)
    image2 = models.FileField(upload_to=cafe_pic_upload_to, blank=True)
    image2_url = models.URLField(blank=True)
    image3 = models.FileField(upload_to=cafe_pic_upload_to, blank=True)
    image3_url = models.URLField(blank=True)
    image4 = models.FileField(upload_to=cafe_pic_upload_to, blank=True)
    image4_url = models.URLField(blank=True)
    image5 = models.FileField(upload_to=cafe_pic_upload_to, blank=True)
    image5_url = models.URLField(blank=True)
    # RATING_CHOICES = [
    #     (1, '★'),
    #     (2, '★★'),
    #     (3, '★★★'),
    #     (4, '★★★★'),
    #     (5, '★★★★★'),
    # ]
    # rating = models.IntegerField(choices=RATING_CHOICES,blank=False,null=False)
    rating = models.DecimalField(max_digits=4, decimal_places=1,null=True,blank=True)
    short_description =models.CharField(max_length=500)

    content = models.TextField(max_length=500, blank=False) # info에 달린 설명이 될 듯 
    # dt_created = models.DateTimeField(auto_now_add=True)
    # dt_updated = models.DateTimeField(auto_now=True)
    cafe_keywords = models.ManyToManyField(CafeKeyword, related_name='cafes', blank=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cafes')
    likes = GenericRelation('Like', related_query_name='cafes')
    style_keywords = models.ManyToManyField('StyleKeyword', related_name='cafes')

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

    style_keywords = models.ManyToManyField('StyleKeyword', related_name='dripshots')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dripshot')
    likes = GenericRelation('Like', related_query_name='dripshot')

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

# 댓글(Comment) 모델
class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    likes = GenericRelation('Like', related_query_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, default=1)
    object_id = models.PositiveIntegerField(default=1)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.content[:30]

    class Meta:
        ordering = ['-dt_created']