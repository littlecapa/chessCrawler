from django import forms

class AppInfoForm(forms.Form):
    app_id = forms.CharField(help_text= "Enter App-ID", required=True)
    app_secret = forms.CharField(help_text= "Enter App-Secret", required=True)

    def checkInfos(self):
        if self.app_id != "" and self.app_secret != "":
            return True
        else:
            return False