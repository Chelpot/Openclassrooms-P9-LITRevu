from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path

import authentication.views
import review.views
from litrevu import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('signup/', authentication.views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('home/', review.views.home, name='home'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('follow/', review.views.follow, name='follow'),
    path('ticket/create/', review.views.create_ticket, name='ticket_create'),
    path('ticket/<int:ticket_id>', review.views.view_ticket, name='view_ticket'),
    path('ticket/delete/<int:ticket_id>', review.views.delete_ticket, name='ticket_delete'),
    path('ticket/edit/<int:ticket_id>', review.views.edit_ticket, name='ticket_edit'),
    path('review/create/', review.views.create_review, name='review_create'),
    path('review/delete/<int:review_id>', review.views.delete_review, name='review_delete'),
    path('review/edit/<int:review_id>', review.views.edit_review, name='review_edit'),
    path('my_posts/', review.views.my_posts, name='my_posts'),

              ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


