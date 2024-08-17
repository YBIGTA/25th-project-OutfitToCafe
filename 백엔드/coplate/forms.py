from django import forms

from .models import * 


class DripshotForm(forms.ModelForm):
    class Meta:
        model = Dripshot
        fields = [
            'title',
            'image1',
            'image2',
            'image3',
            'image4',
            'image5',
            'style_keywords',
            'content',
            'caffe',
        ]
        widgets = {
            'style_keywords': forms.CheckboxSelectMultiple(),  # 체크박스 위젯으로 설정
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 첫 3개의 스타일 키워드만 선택 가능하도록 제한
        self.fields['style_keywords'].queryset = StyleKeyword.objects.all()[:3]

class CaffeForm(forms.ModelForm): # 카페 추가 창 만들때 사용하는거
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
            'image4',
            'image5',
            'style_keyword',
            'content',
        ]
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'name',
            'gender',
            'birth_date',
            'recommend_location',
            'profile_pic',
            'style_keywords',
        ]
        widgets = {
            'style_keywords': forms.CheckboxSelectMultiple(),  # 체크박스 위젯으로 설정
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 첫 3개의 스타일 키워드만 선택 가능하도록 제한
        self.fields['style_keywords'].queryset = StyleKeyword.objects.all()[:3]

       
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea,
        }