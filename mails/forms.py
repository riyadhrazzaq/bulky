from django import forms
from froala_editor.widgets import FroalaEditor

class EmailForm(forms.Form):
   sender = forms.EmailField()
   receiver = forms.EmailField()
   subject = forms.CharField(max_length=75)
   content = forms.CharField(widget=FroalaEditor(options={
       'useClasses': False,
       }))
