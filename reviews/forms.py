from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    RATING_CHOICES = (
        (5, '★★★★★ (5/5) - Outstanding Care'),
        (4, '★★★★☆ (4/5) - Very Good'),
        (3, '★★★☆☆ (3/5) - Satisfactory'),
        (2, '★★☆☆☆ (2/5) - Needs Improvement'),
        (1, '★☆☆☆☆ (1/5) - Unsatisfactory'),
    )
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe how the caretaker handled your pet, communication quality, punctuality...'
            })
        }
