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
    tickets = models.Ticket.objects.filter(user=current_user).all()
    reviews = models.Review.objects.filter(user=current_user).all()
    list_user_Followed = models.UserFollows.objects.filter(user=current_user)

    for relation in list_user_Followed:
        tickets |= models.Ticket.objects.filter(user=relation.followed_user)
        reviews |= models.Review.objects.filter(user=relation.followed_user)

    # Remove from flux tickets that already have a review
    for ticket in tickets:
        for review in reviews:
            if ticket == review.ticket:
                tickets = tickets.exclude(id=ticket.id)

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
    review_form = forms.ReviewTicketForm()
    if request.method == 'POST':
        print(request.POST)
        review_form = forms.ReviewTicketForm(request.POST, request.FILES)
        if review_form.is_valid():
            ticket = models.Ticket(
                title=request.POST.get("title"),
                description=request.POST.get("description"),
                image=request.FILES.get("image", ""),
                user=request.user,
            )
            ticket.save()
            review = models.Review(
                ticket=ticket,
                rating=request.POST.get("rating"),
                headline=request.POST.get("headline"),
                body=request.POST.get("body"),
                user=request.user
            )
            review.save()
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
            # Subscribe
            follow_form = forms.FollowForm(request.POST)
            if follow_form.is_valid():
                user_to_follow = request.POST.get("Username", "")
                if user_to_follow != "":
                    # Check if an user with the given username exist
                    user_to_follow = get_object_or_404(UserClass, username=user_to_follow)
                    if user_to_follow != current_user:
                        # Check if the user is already following the given user
                        models.UserFollows.objects.get_or_create(
                            user=current_user, followed_user=user_to_follow)
        else:
            # Unsubscribe
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


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, pk=ticket_id)
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect('my_posts')
        else:
            print("Form is not valid")
            print(ticket_form.errors)
    else:
        ticket_form = forms.TicketForm(instance=ticket)
    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'review/edit_ticket.html', context=context)


@login_required
def delete_ticket(request, ticket_id):
    if request.method == 'POST':
        ticket = get_object_or_404(models.Ticket, pk=ticket_id)
        ticket.delete()
        return redirect(home)
    context = {
        'ticket_id': ticket_id,
    }
    return render(request, 'review/delete_ticket.html', context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, pk=review_id)
    if request.method == 'POST':
        review_form = forms.ReviewOnlyForm(request.POST, instance=review)
        if review_form.is_valid():
            review.rating = request.POST.get('rating')
            review_form.save()
            return redirect('my_posts')
        else:
            print("Form is not valid")
            print(review_form.errors)
    else:
        review_form = forms.ReviewOnlyForm(instance=review)
    context = {
        'review_form': review_form,
    }
    return render(request, 'review/edit_review.html', context=context)


@login_required
def delete_review(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(models.Review, pk=review_id)
        review.delete()
        return redirect(home)
    context = {
        'review_id': review_id,
    }
    return render(request, 'review/delete_review.html', context)


@login_required
def my_posts(request):
    current_user = request.user
    tickets = models.Ticket.objects.filter(user=current_user).all()
    reviews = models.Review.objects.filter(user=current_user).all()

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
    return render(request, 'review/my_posts.html', context=context)

@login_required
def create_review_for_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewOnlyForm(request.POST)
    if request.method == 'POST':
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('home')
        else:
            print("Form is not valid")
            print(review_form.errors)
    context = {
        'review_form': review_form,
    }
    return render(request, 'review/create_review_for_ticket.html', context=context)