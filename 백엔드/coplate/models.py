from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from .validators import validate_no_special_characters, validate_restaurant_link


def caffe_pic_upload_to(instance, filename):
    return f'caffe/{filename}'

def dripshot_pic_upload_to(instance, filename):
    return f'user_pic/{filename}'

def person_pic_upload_to(instance, filename):
    return f'person/{filename}'


class User(AbstractUser):
    nickname = models.CharField(
        max_length=15, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters],
        error_messages={'unique': '이미 사용중인 닉네임입니다.'},
    )
    profile_pic = models.FileField(upload_to=person_pic_upload_to, blank=True, null=True, default='user_pics/default_profile_pic.jpg')
    profile_pic_url = models.URLField(
        blank=True, 
        default='https://yonfen.s3.amazonaws.com/default_profile_pic.jpg'
    )

    profile_pic = models.ImageField(default='default_profile_pic.jpg', upload_to='profile_pics')

    intro = models.CharField(max_length=60, blank=True)

    following = models.ManyToManyField('self',symmetrical=False, blank=True, related_name='followers')


    def __str__(self):
        return self.email # 이거 아마 이메일로 매칭이 되는것일껄?


class Review(models.Model):
    title = models.CharField(max_length=30)

    restaurant_name = models.CharField(max_length=20)

    restaurant_link = models.URLField(validators=[validate_restaurant_link])

    RATING_CHOICES = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES, default=None)

    # image1 = models.ImageField(upload_to='review_pics')
    image1 = models.FileField(upload_to=caffe_pic_upload_to,blank=True) # 용량 확장 공사 진행해야 되고 , 프론트에서 필드를 추가할때 +누르면 이미지 필드 나올 수 있게 하면 되지 않을까
    image1_url = models.URLField(blank=True)

    image2 = models.FileField(upload_to=caffe_pic_upload_to,blank=True) # > 이미지 , 동영상 > 외부 스토리지에 저장하고 mongodb에 url 저장해야됨 
    image2_url = models.URLField(blank=True)

    image3 = models.FileField(upload_to=caffe_pic_upload_to,blank=True)
    image3_url = models.URLField(blank=True)

    image4 = models.FileField(upload_to=caffe_pic_upload_to,blank=True)
    image4_url = models.URLField(blank=True)
  #  image1 = models.ImageField(upload_to='review_pics')

   # image2 = models.ImageField(upload_to='review_pics', blank=True)
 
  #   image3 = models.ImageField(upload_to='review_pics', blank=True)

    content = models.TextField()

    dt_created = models.DateTimeField(auto_now_add=True)

    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='reviews')

    likes = GenericRelation('Like', related_query_name='review')


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-dt_created']
    
class Comment(models.Model):
    content = models.TextField(max_length=500, blank=False)

    dt_created = models.DateTimeField(auto_now_add = True)

    dt_updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')

    review = models.ForeignKey(Review, on_delete=models.CASCADE,related_name='comments')

    likes = GenericRelation('Like', related_query_name='comment')

    def __str__(self):
        return self.content[:30]
    class Meta:
        ordering = ['-dt_created']
    
class Like(models.Model):
    dt_created = models.DateTimeField(auto_now_add = True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.PositiveIntegerField()

    liked_object = GenericForeignKey()

    def __str__(self):
        return f"({self.user}, {self.liked_object})"
    class Meta:
        unique_together = ['user', 'content_type', 'object_id']