from django import forms
from .models import Badge, Contest, ContestSubmission


class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['name', 'description', 'icon', 'badge_type', 'requirement_value', 'xp_reward', 'rarity', 'is_active']


class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['title', 'description', 'theme', 'start_date', 'end_date', 'judging_end_date', 'first_prize_xp', 'second_prize_xp', 'third_prize_xp', 'participation_xp', 'status', 'max_participants']


class ContestSubmissionForm(forms.ModelForm):
    class Meta:
        model = ContestSubmission
        fields = ['contest', 'artwork']
