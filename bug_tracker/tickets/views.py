import json
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
from django.views.generic import ListView, CreateView, View, UpdateView, DetailView
from auditlog.models import LogEntry

from projects.models import Project
from .forms import TicketForm, CommentForm

from .models import Ticket
from users.models import User

from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from .forms import CommentForm

# Create your views here.


class TicketListView(ListView):
    template_name = "tickets/index.html"
    model = Ticket
    context_object_name = "tickets"

    def get_queryset(self):
        if self.request.user.role != "admin":
            self.queryset = Ticket.objects.filter(developer=self.request.user)
        return super().get_queryset()

    def get_paginate_by(self, queryset):
        if self.request.GET.get("page_number"):
            self.request.session["page_number"] = self.request.GET.get("page_number")
        self.paginate_by = self.request.session.get("page_number", 5)
        return self.paginate_by


class CreateTicketView(View):
    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(pk=project_id)
        form = TicketForm(project_id=project_id)

        return render(
            request, "tickets/create_ticket.html", {"form": form, "project": project}
        )

    def post(self, request, project_id, *args, **kwargs):
        form = TicketForm(request.POST)
        project = Project.objects.get(pk=project_id)

        if form.is_valid():
            ticket = form.save(commit=False)

            ticket.project = project
            ticket.submitter = request.user
            ticket.save()
            return redirect("detail_project", project_id)
        else:
            return render(
                request,
                "tickets/create_ticket.html",
                {"form": form, "project": project},
            )


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
        actions = {0: "create", 1: "update", 2: "delete", 3: "Access"}

        histories = LogEntry.objects.filter(object_id=kwargs["object"].id)
        context["form"] = CommentForm()
        history_list = []

        for history in histories:
            changes = json.loads(history.changes)
            data = {}
            data["user"] = history.actor
            data["action"] = actions[history.action]
            data["field"] = list(changes.keys())[0]
            data["old_value"] = list(changes.values())[0][0]
            data["new_value"] = list(changes.values())[0][1]
            data["date"] = history.timestamp
            history_list.append(data)

        context["histories"] = history_list
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
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.commenter = self.request.user
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
