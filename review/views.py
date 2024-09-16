from itertools import chain

from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models
from litrevu import settings
from .models import UserFollows


@login_required
def home(request):
    current_user = request.user
    tickets = models.Ticket.objects.filter(user=current_user)
    reviews = models.Review.objects.filter(user=current_user)
    list_user_Followed = models.UserFollows.objects.filter(user=current_user)

    for relation in list_user_Followed:
        tickets |= models.Ticket.objects.filter(user=relation.followed_user)
        reviews |= models.Review.objects.filter(user=relation.followed_user)

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
    current_user = request.user
    follow_form = forms.FollowForm()
    follow_list = models.UserFollows.objects.filter(user=current_user)
    UserClass = get_user_model()
    if request.method == 'POST':
        if 'subscribe' in request.POST:
            #Subscribe
            follow_form = forms.FollowForm(request.POST)
            if follow_form.is_valid():
                user_to_follow = request.POST.get("Username", "")
                if user_to_follow != "":
                    #Check if an user with the given username exist
                    user_to_follow = get_object_or_404(UserClass, username=user_to_follow)
                    if user_to_follow != current_user:
                        #Check if the user is already following the given user
                        models.UserFollows.objects.get_or_create(
                            user=current_user, followed_user=user_to_follow)
        else:
            #Unsubscribe
            user_to_unfollow = request.POST.get("followed_user", "")
            followed_user = get_object_or_404(UserClass, username=user_to_unfollow)
            relation = models.UserFollows.objects.filter(user=current_user, followed_user=followed_user)
            relation.delete()

            pass
    context = {
        'follow_form': follow_form,
        'follow_list': follow_list,
    }
    return render(request, 'review/follow.html', context=context)