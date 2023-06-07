from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views.generic import ListView, CreateView, View, UpdateView, DetailView

from projects.models import Project
from .forms import TicketForm, CommentForm

from .models import Ticket

from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from .forms import CommentForm

# Create your views here.


class TicketListView(ListView):
    template_name = "tickets/index.html"
    model = Ticket
    context_object_name = "tickets"


class TicketUpdateView(UpdateView):
    template_name = "tickets/update_ticket.html"
    form_class = TicketForm
    model = Ticket
    context_object_name = "ticket"
    success_url = "/tickets"


class TicketDisplay(DetailView):
    model = Ticket
    template_name = "tickets/detail_ticket.html"
    context_object_name = "ticket"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class PostComment(SingleObjectMixin, FormView):
    model = Ticket
    form_class = CommentForm
    template_name = "post_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostComment, self).get_form_kwargs()
        kwargs["request"] = self.request
        print(kwargs["request"])
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.ticket = self.get_object()
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        ticket = self.get_object()
        return reverse("ticket_detail", kwargs={"pk": ticket.pk})


class TicketDetailView(View):
    def get(self, request, *args, **kwargs):
        view = TicketDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)


# class TicketDetailView(DetailView):
#     template_name = "tickets/detail_ticket.html"
#     model = Ticket
#     context_object_name = "ticket"

# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context["tickets"] = Ticket.objects.filter(project=context["project"])
#     return context


# class CreateTicketView(CreateView):
#     template_name = "tickets/create_ticket.html"
#     form_class = TicketForm
#     model = Ticket
#     success_url = "/tickets"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print(self.request)
#         return context


class CreateTicketView(View):
    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        form = TicketForm()
        return render(
            request, "tickets/create_ticket.html", {"form": form, "project": project}
        )

    def post(self, request, project_id, *args, **kwargs):
        form = TicketForm(request.POST)
        project = Project.objects.get(pk=project_id)

        if form.is_valid():
            ticket = form.save(commit=False)

            ticket.project = project
            ticket.save()
            return redirect("detail_project", project_id)
        else:
            return render(
                request,
                "tickets/create_ticket.html",
                {"form": form, "project": project},
            )