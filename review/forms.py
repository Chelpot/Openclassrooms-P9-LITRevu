from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field

from . import models

User = get_user_model()

class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'description', 'image']
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    title = forms.CharField(
        label="Titre",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'larger_input_text'}),
    )

    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={'class': 'larger_input_text'}),
    )

    image = forms.ImageField(
        label="Télécharger fichier",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Publier', css_class='button'))

class ReviewTicketForm(forms.Form):
    title = forms.CharField(
        label="Titre de l'ouvrage",
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={'class': 'larger_input_text'}),
    )

    description = forms.CharField(
        label = "Description",
        max_length= 2048,
        required = False,
        widget=forms.Textarea(attrs={'class': 'larger_input_text'}),

    )

    image = forms.ImageField(
        label = "Télécharger fichier",
        required = False,
    )

    #Review part
    headline = forms.CharField(
        label="Titre de la critique",
        max_length=128,
        required=True,
        widget=forms.TextInput(attrs={'class': 'larger_input_text'}),
    )

    rating = forms.TypedChoiceField(
        label="Note",
        choices=((0, "0"),
                 (1, "1"),
                 (2, "2"),
                 (3, "3"),
                 (4, "4"),
                 (5, "5"),
                 ),
        coerce=lambda x: bool(int(x)),
        initial='0',
        required=True,
        widget=forms.RadioSelect(),
    )

    body = forms.CharField(
        label="Commentaire ",
        max_length=8192,
        required=False,
        widget=forms.Textarea(attrs={'class': 'larger_input_text'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Valider'))

class ReviewOnlyForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['headline', 'rating', 'body']

    headline = forms.CharField(
        label="Titre de la critique",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'larger_input_text'}),
    )

    rating = forms.TypedChoiceField(
        label="Note",
        choices=((0, "0"),
                 (1, "1"),
                 (2, "2"),
                 (3, "3"),
                 (4, "4"),
                 (5, "5"),
                 ),
        coerce=lambda x: bool(int(x)),
        initial='0',
        required=True,
        widget=forms.RadioSelect(),
    )

    body = forms.CharField(
        label="Commentaire ",
        required=False,
        widget=forms.Textarea(attrs={'class': 'larger_input_text'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Valider'))


class FollowForm(forms.Form):
    Username = forms.CharField(
        max_length=100,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={'placeholder': "Entrez le nom d'un utilisateur à suivre",
                                      'name': 'subscribe'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('Username', css_class='large-input align-center-horizontal'),
        )
        self.helper.add_input(Submit('subscribe', 'Envoyer'))