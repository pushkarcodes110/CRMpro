from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Lead
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm

class SignupView(generic.CreateView):
    template_name ="registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

@login_required
def logoutUser(request):
    logout(request)
    return redirect('/')

class LandingPageView(generic.TemplateView):
    template_name="landing.html"

def landing_page(request):
    return render(request, "landing.html")


class LeadListView(generic.ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name ='leads'

def lead_lists(request):
    leads = Lead.objects.all()
    context ={
        'leads': leads,
    }
    return render(request, "leads/lead_list.html", context)


class LeadDetailView(generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name ='lead'

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context ={
        'lead': lead,
    }

    return render(request, "leads/lead_detail.html", context)

class LeadCreateView(generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class= LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        # TODO send email
        send_mail(
            subject="A New Lead is Created",
            message="Check out!",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )

        return super(LeadCreateView, self).form_valid(form)

def lead_create(request):

    form = LeadModelForm
    if request.method=="POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/leads")

    context = {
        'form': form
    }
    return render(request, "leads/lead_create.html",context)


class LeadUpdateView(generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class= LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method=="POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
        return redirect("/leads")

    context={
        "form": form,
        "lead": lead,
    }

    return render(request, "leads/lead_update.html", context)


class LeadDeleteView(generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")