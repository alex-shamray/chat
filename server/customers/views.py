from django.views.generic.edit import CreateView

from .forms import CustomerSignupForm


class CustomerSignupView(CreateView):
    template_name = 'customers/signup_form.html'
    form_class = CustomerSignupForm
    success_url = '/'
