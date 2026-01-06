
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from admin_panel.models import Consultation, Feedback
from ml_model import predict_sentiment
from django.db.models import Count

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


def home(request):
    consultations = Consultation.objects.all().order_by('-date')
    return render(request, 'home.html', {
        'consultations': consultations
    })


def consultation_detail(request, reference_no):
    consultation = get_object_or_404(
        Consultation,
        reference_no=reference_no
    )
    if request.method == "POST":
        name = request.POST.get("name")
        organization = request.POST.get("organization")
        comment = request.POST.get("comment")
        sentiment = predict_sentiment(comment)
        Feedback.objects.create(
            consultation=consultation,
            name=name,
            organization=organization,
            comment=comment,
            sentiment=sentiment
        )
        messages.success(request, " Your feedback has been submitted successfully.")
        return redirect("consultation_detail", reference_no=reference_no)
    return render(
        request,
        "consultation_detail.html",
        {"consultation": consultation}
    )
