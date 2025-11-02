from django import forms
from .models import Report, UserViolation


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'maxlength': 500}),
        }

    def clean_description(self):
        data = self.cleaned_data.get('description', '')
        if len(data) > 500:
            raise forms.ValidationError('Description must be 500 characters or fewer.')
        return data


class UserViolationForm(forms.ModelForm):
    class Meta:
        model = UserViolation
        fields = ['user', 'violation_type', 'description', 'report', 'action_taken', 'action_expires_at', 'actioned_by']
