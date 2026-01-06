
from .models import Consultation

from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from .models import Consultation, Feedback
from ml_model import predict_sentiment
from django.db.models import Count

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect("manage_consultations")  
            else:
                messages.error(request, "Access denied. Superuser only.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login") 


def dashboard(request, reference_no):
    consultation = get_object_or_404(
        Consultation,
        reference_no=reference_no
    )
    
    # Fetch all feedback related to this consultation
    all_feedback = Feedback.objects.filter(consultation=consultation).order_by('-id')

    feedback_counts = (
        all_feedback
        .values('sentiment')
        .annotate(count=Count('id'))
    )

    positive = neutral = negative = 0
    for item in feedback_counts:
        # Added .lower() here to make sure it matches even if DB has "Positive" or "POSITIVE"
        sentiment_val = str(item['sentiment']).lower() 
        
        if sentiment_val == 'positive':
            positive = item['count']
        elif sentiment_val == 'neutral':
            neutral = item['count']
        elif sentiment_val == 'negative':
            negative = item['count']

    context = {
        'consultation': consultation,
        'positive_count': positive,
        'neutral_count': neutral,
        'negative_count': negative,
        'all_feedback': all_feedback,
    }
    return render(request, 'dashboard.html', context)

def manage_consultations(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        reference_no = request.POST.get('reference_no')
        if title and description and reference_no:
            Consultation.objects.create(
                title=title,
                description=description,
                reference_no=reference_no
            )
            return redirect('manage_consultations')
    consultations = Consultation.objects.all().order_by('-date')
    return render(request, 'manage_consultations.html', {
        'consultations': consultations
    })




def sentiment_analysis(request, reference_no):
    consultation = get_object_or_404(
        Consultation,
        reference_no=reference_no
    )
    feedback_counts = (
        Feedback.objects
        .filter(consultation=consultation)
        .values('sentiment')
        .annotate(count=Count('id'))
    )
    positive = neutral = negative = 0
    for item in feedback_counts:
        if item['sentiment'] == 'positive':
            positive = item['count']
        elif item['sentiment'] == 'neutral':
            neutral = item['count']
        elif item['sentiment'] == 'negative':
            negative = item['count']
    positive_feedbacks = Feedback.objects.filter(
        consultation=consultation,
        sentiment='positive'
    ).order_by('-submitted_at')

    context = {
        'consultation': consultation,
        'positive_count': positive,
        'neutral_count': neutral,
        'negative_count': negative,
        'positive_feedbacks': positive_feedbacks,
    }
    return render(request, 'sentiment_analysis.html', context)

def word_cloud(request, reference_no):
    consultation = get_object_or_404(Consultation, reference_no=reference_no)

    feedbacks = Feedback.objects.filter(consultation=consultation)

    return render(request, 'word_cloud.html', {
        'consultation': consultation,
        'feedbacks': feedbacks,
    })

def summaries(request, reference_no):
    consultation = get_object_or_404(Consultation, reference_no=reference_no)
    feedbacks = Feedback.objects.filter(consultation=consultation)
    total_count = feedbacks.count()
    summary_text = (
        "The public comments reflect mixed responses from stakeholders. "
        "Many respondents appreciate the improved transparency and governance measures, "
        "while concerns remain regarding compliance burden, timelines, and clarity of language."
    )
    return render(request, 'summary.html', {
        'consultation': consultation,
        'total_count': total_count,
        'summary_text': summary_text,
    })

def analysis(request, reference_no):
    consultation = get_object_or_404(Consultation, reference_no=reference_no)
    result = None
    if request.method == "POST":
        if request.FILES.get('csv_file'):
            result = "CSV file uploaded successfully and ready for analysis."
        elif request.POST.get('text_block'):
            text = request.POST.get('text_block')
            result = f"Analyzed {len(text.splitlines())} text entries."
    return render(request, 'analysis.html', {
        'consultation': consultation,
        'result': result,
    })
