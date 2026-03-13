from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils import timezone
from .models import UnsentMessage
from .forms import UnsentMessageForm, MessageSearchForm
from .message_utils import extract_message_sentiment_keywords, generate_message_preview, calculate_message_engagement_score
import random
import math
import hashlib

def get_random_colors():
    """Generate a random color for message cards"""
    colors = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
        '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#A9DFBF',
        '#F1948A', '#AED6F1', '#F9E79F', '#D7BDE2', '#A3E4D7',
        '#F5B7B1', '#AEB6BF', '#F9E2AF', '#D2B4DE', '#81C784',
        '#64B5F6', '#FFB74D', '#E57373', '#81C784', '#64B5F6'
    ]
    return random.choice(colors)

def home(request):
    """Homepage with message submission form and recent messages"""
    if request.method == 'POST':
        form = UnsentMessageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UnsentMessageForm()
    
    # Get recent messages
    recent_messages = UnsentMessage.objects.all()[:10]

    # Assign random colors to messages and compute aging
    messages_with_colors = []
    now = timezone.now()
    for msg in recent_messages:
        age_days = (now - msg.created_at).days
        age_months = age_days // 30
        # compute intervals after 6 months: each 6 months increases stain level
        intervals = 0
        if age_months > 6:
            intervals = math.floor((age_months - 6) / 6) + 1
        age_opacity = min(0.6, intervals * 0.12)
        text_opacity = max(0.45, 1 - intervals * 0.12)

        messages_with_colors.append({
            'message': msg,
            'color': get_random_colors(),
            'age_months': age_months,
            'age_opacity': age_opacity,
            'text_opacity': text_opacity,
            'preview': generate_message_preview(msg.message_content),
            'sentiment': extract_message_sentiment_keywords(msg.message_content),
            'engagement_score': calculate_message_engagement_score(msg),
        })

    context = {
        'form': form,
        'messages_with_colors': messages_with_colors,
    }
    return render(request, 'homepage/home.html', context)

def search_messages(request):
    """Search messages by sender or receiver name (case-insensitive)"""
    form = MessageSearchForm(request.GET)
    search_results = []

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query', '').strip()

        if search_query:
            # Case-insensitive search on both sender and receiver names
            qs = UnsentMessage.objects.filter(
                Q(sender_name__icontains=search_query) |
                Q(receiver_name__icontains=search_query)
            )

            # Assign random colors and aging info
            now = timezone.now()
            for msg in qs:
                age_days = (now - msg.created_at).days
                age_months = age_days // 30
                intervals = 0
                if age_months > 6:
                    intervals = math.floor((age_months - 6) / 6) + 1
                age_opacity = min(0.6, intervals * 0.12)
                text_opacity = max(0.45, 1 - intervals * 0.12)

                search_results.append({
                    'message': msg,
                    'color': get_random_colors(),
                    'age_months': age_months,
                    'age_opacity': age_opacity,
                    'text_opacity': text_opacity,
                    'preview': generate_message_preview(msg.message_content),
                    'sentiment': extract_message_sentiment_keywords(msg.message_content),
                    'engagement_score': calculate_message_engagement_score(msg),
                })
    
    context = {
        'form': form,
        'search_results': search_results,
        'query': form.cleaned_data.get('search_query', '') if form.is_valid() else '',
    }
    return render(request, 'homepage/search.html', context)

def message_detail(request, pk):
    """Display a single message with random color"""
    message = get_object_or_404(UnsentMessage, pk=pk)
    color = get_random_colors()

    # compute reaction count deterministically based on music identifier
    reaction_count = 0
    key = message.preset_music or (message.music_file.name if message.music_file else '')
    if key:
        try:
            hv = hashlib.md5(key.encode('utf-8')).hexdigest()
            reaction_count = (int(hv, 16) % 12) + 1
        except Exception:
            reaction_count = random.randint(1, 8)

    # aging info
    now = timezone.now()
    age_days = (now - message.created_at).days
    age_months = age_days // 30
    intervals = 0
    if age_months > 6:
        intervals = math.floor((age_months - 6) / 6) + 1
    age_opacity = min(0.6, intervals * 0.12)
    text_opacity = max(0.45, 1 - intervals * 0.12)

    context = {
        'message': message,
        'color': color,
        'reaction_count': reaction_count,
        'age_months': age_months,
        'age_opacity': age_opacity,
        'text_opacity': text_opacity,
    }
    return render(request, 'homepage/message_detail.html', context)


def messages_by_song(request):
    """Show messages that share the same preset music or uploaded music file name."""
    song = request.GET.get('song', '').strip()
    results = []
    if song:
        qs = UnsentMessage.objects.filter(
            Q(preset_music=song) | Q(music_file__icontains=song)
        )
        now = timezone.now()
        for msg in qs:
            age_days = (now - msg.created_at).days
            age_months = age_days // 30
            intervals = 0
            if age_months > 6:
                intervals = math.floor((age_months - 6) / 6) + 1
            age_opacity = min(0.6, intervals * 0.12)
            text_opacity = max(0.45, 1 - intervals * 0.12)

            results.append({
                'message': msg,
                'color': get_random_colors(),
                'age_months': age_months,
                'age_opacity': age_opacity,
                'text_opacity': text_opacity,
            })

    context = {
        'song': song,
        'results': results,
        'count': len(results),
    }
    return render(request, 'homepage/messages_by_song.html', context)

