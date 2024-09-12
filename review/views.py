from itertools import chain

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models
from litrevu import settings

@login_required
def home(request):
    tickets = models.Ticket.objects.filter()
    reviews = models.Review.objects.filter()
    ticket_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda post: post.time_created,
        reverse=True
    )

    paginator = Paginator(ticket_and_reviews, 6)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'review/home.html', context=context)

@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_create')
        else:
            print("Form is not valid")
            print(ticket_form.errors)
    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'review/create_ticket.html', context=context)

@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'review/view_ticket.html', {'ticket': ticket})

@login_required
def create_review(request):
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            ticket = review_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    context = {
        'review_form': review_form,
    }
    return render(request, 'review/create_review.html', context=context)

@login_required
def follow(request):
    follow_form = forms.FollowForm()
    if request.method == 'POST':
        follow_form = forms.FollowForm(request.POST)
        if follow_form.is_valid():
            pass
            #A continuer

    context = {
        'follow_form': follow_form,
    }
    return render(request, 'review/follow.html', context=context)