from django import forms

from ministry.models import Report
from dal import autocomplete


class NameForm(forms.Form):
    your_name = forms.CharField(label="Your name", max_length=100)


class ReportForm(forms.ModelForm):
    remarks = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 4}))
    hours = forms.IntegerField(required=False, initial="")
    return_visits = forms.IntegerField(required=False, initial="")
    bible_studies = forms.IntegerField(required=False, initial="")
    placements = forms.IntegerField(required=False, initial="")
    videos = forms.IntegerField(required=False, initial="")

    class Meta:
        model = Report
        fields = [
            "publisher",
            "hours",
            "return_visits",
            "bible_studies",
            "placements",
            "videos",
            "remarks",
        ]
        labels = {
            "publisher": "Publisher",
        }
        widgets = {
            "publisher": autocomplete.ModelSelect2(
                url="publisher-autocomplete",
                forward=("cong",),
                attrs={
                    # Set some placeholder
                    "data-placeholder": "Search Publisher...",
                },
            )
        }

    def clean(self):
        self.cleaned_data = super(ReportForm, self).clean()
        if not self.cleaned_data["hours"]:
            self.cleaned_data["hours"] = 0
        if not self.cleaned_data["videos"]:
            self.cleaned_data["videos"] = 0
        if not self.cleaned_data["return_visits"]:
            self.cleaned_data["return_visits"] = 0
        if not self.cleaned_data["bible_studies"]:
            self.cleaned_data["bible_studies"] = 0
        if not self.cleaned_data["placements"]:
            self.cleaned_data["placements"] = 0
        return self.cleaned_data
