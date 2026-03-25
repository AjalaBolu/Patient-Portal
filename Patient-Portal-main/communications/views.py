from django.shortcuts import render, redirect
from .models import Message
from .forms import MessageForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages as django_messages


def is_staff(user):
    return user.is_staff

@login_required
def send_message(request):
    # Get all patients (non-staff users)
    patients = User.objects.filter(is_staff=False).order_by('first_name', 'last_name')
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)  # Don't save yet
            message.sender = request.user      # Set the sender
            message.save()
            django_messages.success(request, f'Message sent to {message.recipient.get_full_name()}')
            return redirect('communications:inbox')
    else:
        form = MessageForm()

    context = {
        'form': form,
        'patients': patients
    }
    return render(request, 'communications/send_message.html', context)

@login_required
def inbox(request):
    """
    Display messages received by the logged-in user.
    """
    messages_received = Message.objects.filter(recipient=request.user).order_by('timestamp')
    context = {
        'messages': messages_received
    }
    return render(request, 'communications/inbox.html', context)