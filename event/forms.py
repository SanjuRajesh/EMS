from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm



class addeventForm(forms.ModelForm):
    #dept_club = forms.CharField(max_length=50, required=True)
    class Meta:
        model = Event
        fields = '__all__'  
    def __init__(self, *args, **kwargs):
        super(addeventForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs and 'dept_club' in kwargs['initial']:
            self.fields['dept_club'].queryset = self.fields['dept_club'].queryset.filter(id=kwargs['initial']['dept_club'])

    def __init__(self, *args, **kwargs):
        super(addeventForm, self).__init__(*args, **kwargs)
        # Make dept_club field read-only
        self.fields['dept_club'].widget.attrs['disabled'] = 'disabled'


def __init__(self, *args, **kwargs):
        super(addeventForm, self).__init__(*args, **kwargs)
        self.fields['brochure'].required = True



class UserCreationFormExtended(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)



class EventReportForm(forms.ModelForm):
    class Meta:
        model = Event_Report
        fields = '__all__'

class DutyAllocForm(forms.ModelForm):
     class Meta:
          model = Duty_Alloc
          fields = '__all__'


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['name', 'email', 'phone', 'designation',  'user', 'dept_club']  