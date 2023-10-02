from django import forms      
from .models import Ad, Reply 


class AdCreateForm(forms.ModelForm):
    
        class Meta:
            model = Ad
            fields = ('title', 'category_ad', 'text_ad', 'pictures', 'video', 'status')

        def __init__(self, *args, **kwargs):
            
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    'autocomplete': 'off'
                })
            
class AdUpdateForm(AdCreateForm):
    
    class Meta:
        model = Ad
        fields = ('title', 'category_ad', 'text_ad', 'pictures', 'video', 'status')

    def __init__(self, *args, **kwargs):
      
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })
            
class ReplyCreateForm(forms.ModelForm):
    
    class Meta:
        model = Reply
        fields = ['text']

    def __init__(self, *args, **kwargs):
       
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'off'
        })