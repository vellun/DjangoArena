import django.forms


class DuelCodeForm(django.forms.Form):
    code = django.forms.CharField(
        widget=django.forms.Textarea,
        initial="from django.views.generic import"
        " View\n\nclass SolutionView(View):\
            \n\t'''\n\tWrite your code here\n\t'''\n\tpass",
    )


__all__ = [DuelCodeForm]
