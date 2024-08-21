from django import forms

from .models import *


class DripshotForm(forms.ModelForm):
    cafe = forms.ModelChoiceField(
        queryset=Cafe.objects.all(),
        label='카페를 선택하세요',
        widget=forms.Select(attrs={'class': 'select2'})  # select2 클래스를 추가하여 Select2를 적용
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
            'rating',
        ]
        widgets = {
            'rating': forms.Select(),  # Select 위젯을 사용하여 드롭다운으로 선택 가능
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
        
            'content',
        ]
#class ProfileForm(forms.ModelForm):
 #   class Meta:
  #      model = User
   #     fields = [
    #        'name',
     #       'gender',
      #      'birth_date',
       #     'recommend_location',
        #    'profile_pic',
         #   'style_keywords',
      #  ]
       # widgets = {
        #    'style_keywords': forms.CheckboxSelectMultiple(),  # 체크박스 위젯으로 설정
         #   'birth_date': forms.DateInput(attrs={'type': 'date'}),
       # }
class ProfileForm(forms.ModelForm):
    style_keywords = forms.ModelMultipleChoiceField(
        queryset=StyleKeyword.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = User
        fields = ['name', 'profile_pic','birth_date','recommend_location', 'style_keywords']
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 첫 3개의 스타일 키워드만 선택 가능하도록 제한
    #     self.fields['style_keywords'].queryset = StyleKeyword.objects.all()[:12]

class CafeEssentialForm(forms.ModelForm):
    class Meta:
        model = Cafe
        fields = ['name', 'short_description', 'content', 'author']     
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content',
        ]
        widgets = {
            'content': forms.Textarea,
        }