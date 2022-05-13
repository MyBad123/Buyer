from django.shortcuts import render
from django import forms

from request.tasks import send_marcup_csv_attach


class LinkEmailForm(forms.Form):
    link = forms.URLField(widget=forms.TextInput(attrs={
        'class': 'form-control input_login',
        'placeholder': 'Link'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control input_login',
        'placeholder': 'Email'
    }))


class MarkupDoc:

    @staticmethod
    def create_markup_doc(request):
        if request.method == 'POST':
            form = LinkEmailForm(request.POST)
            if form.is_valid():
                send_marcup_csv_attach.delay(form.data['email'], form.data['link'])
                return render(
                    request,
                    'markup/markup_create_doc.html',
                    {
                        'status': 'The application was successfully created. You will receive an email',
                        'form': form
                    }
                )
        else:
            form = LinkEmailForm()

        return render(request, 'markup/markup_create_doc.html', {'form': form})
