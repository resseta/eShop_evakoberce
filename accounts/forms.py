from django.contrib.auth.forms import UserCreationForm
from django.forms import DateField, NumberInput, CharField
from django.db.transaction import atomic

from accounts.models import Profile


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email', 'password1']

    date_of_birth = DateField(widget=NumberInput(attrs={'type': 'date'}), label="Datum narození:", required=False)
    phone = CharField(widget=NumberInput, label="Telefon:", required=False)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)
        date_of_birth = self.cleaned_data['date_of_birth']
        phone = self.cleaned_data['phone']
        profile = Profile(user=user,
                          date_of_birth=date_of_birth,
                          phone=phone)
        if commit:
            profile.save()
        return user
