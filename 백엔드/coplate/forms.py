from django import forms

from .models import * 


class ReviewForm(forms.ModelForm): # 카페 추가 창 만들때 사용하는거
    class Meta:
        model = Caffe
        fields = [
            'name',
            'location',
            'location_url',
            'instagram_url',
            'image1',
            'image2',
            'image3',
            'content',
        ]
        widgets = {
            'rating': forms.RadioSelect,
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'user_name',
            'gender',
            'age',
            'location',
            'profile_pic',
        ]
       
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea,
        }