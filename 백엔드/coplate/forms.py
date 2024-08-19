from django import forms

from .models import * 

class DripshotForm(forms.ModelForm):
    cafe = forms.ModelChoiceField(
        queryset=Cafe.objects.all(),
        label='Cafe',
        widget=forms.TextInput(attrs={'id': 'cafe-autocomplete'}),
    )

    class Meta:
        model = Dripshot
        fields = [
            'title',
            'image1',
            'image2',
            'image3',
            'image4',
            'image5',
            'content',
            'cafe',
        ]
        widgets = {
            'style_keywords': forms.CheckboxSelectMultiple(),
        }

    

class CafeForm(forms.ModelForm): # 카페 추가 창 만들때 사용하는거
    class Meta:
        model = Cafe
        fields = [
            'name',
            'address',
            'address_url',
            'sns_link',
            'image1',
            'image2',
            'image3',
            'image4',
            'image5',
            'style_keywords',
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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 첫 3개의 스타일 키워드만 선택 가능하도록 제한
    #     self.fields['style_keywords'].queryset = StyleKeyword.objects.all()[:12]

       
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea,
        }