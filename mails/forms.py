from django import forms
from froala_editor.widgets import FroalaEditor

class EmailForm(forms.Form):
   sender = forms.EmailField()
   receiver = forms.EmailField(widget=forms.Textarea(attrs={'class': 'textarea', 'placeholder': 'janedoe@mail.com\njohndoe@mail.com'}))
   subject = forms.CharField(max_length=75, widget=forms.TextInput(attrs={'class':'input'}))
   content = forms.CharField(widget=FroalaEditor(options={
       'useClasses': False,
       }))

   attachments = forms.FileField(
           required= False, 
           widget=forms.ClearableFileInput(attrs={'multiple': True})
           )


