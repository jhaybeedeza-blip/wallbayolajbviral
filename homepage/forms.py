from django import forms
from .models import UnsentMessage
import os
import json
from django.conf import settings

def get_preset_music_choices():
    """
    Get list of available music files from static/music directory.
    
    AUTO-DISCOVERS all audio files in the folder.
    Optionally categorizes them using categories.json if available.
    
    EASY TO ADD MUSIC: Just drop audio files in static/music/
    - They will appear immediately in the dropdown
    - Optional: Edit categories.json to organize by mood/category
    """
    music_dir = os.path.join(settings.BASE_DIR, 'static', 'music')
    default_choice = ('', '--- No Music Selected ---')

    # Try to read categories mapping from static/music/categories.json
    # This is OPTIONAL - if you don't have it, all files still appear
    categories_path = os.path.join(music_dir, 'categories.json')
    mapping = {}
    if os.path.exists(categories_path):
        try:
            with open(categories_path, 'r', encoding='utf-8') as f:
                mapping = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load categories.json: {e}")
            mapping = {}

    choices = [default_choice]

    if os.path.exists(music_dir):
        # AUTO-DISCOVER: Find all audio files (no manual listing needed)
        music_files = sorted([
            f for f in os.listdir(music_dir)
            if f.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac'))
        ])

        if not music_files:
            # No files found
            return choices

        # Group by category
        grouped = {}  # For categorized music
        uncategorized = []  # For music without category

        for music_file in music_files:
            cat = mapping.get(music_file)  # Check if file has a category
            if cat:
                grouped.setdefault(cat, []).append((music_file, music_file))
            else:
                uncategorized.append((music_file, music_file))

        # Add uncategorized files first (as individual items)
        for item in uncategorized:
            choices.append(item)

        # Then add grouped/categorized items as optgroups
        for cat, items in grouped.items():
            choices.append((cat, items))

        # If categories.json references files that are not present on disk,
        # include them in a "Missing files" optgroup with a special prefix
        missing_files = [fname for fname in mapping.keys() if fname not in music_files]
        if missing_files:
            missing_items = [(f'MISSING__{fname}', f'{fname} (missing - add to static/music)') for fname in missing_files]
            choices.append(('Missing files (add to static/music)', missing_items))

    return choices

class UnsentMessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically load choices each time the form is instantiated
        self.fields['preset_music'].choices = get_preset_music_choices()
    
    preset_music = forms.ChoiceField(
        choices=[],  # Empty initially, will be populated in __init__
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'presetMusicSelect'
        }),
        label='🎵 Select Preset Music'
    )
    
    music_start_time = forms.FloatField(
        required=False,
        initial=0,
        widget=forms.HiddenInput(attrs={
            'id': 'musicStartTime'
        }),
        label='Music Start Time'
    )
    
    music_end_time = forms.FloatField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'id': 'musicEndTime'
        }),
        label='Music End Time'
    )
    
    class Meta:
        model = UnsentMessage
        fields = ['sender_name', 'receiver_name', 'message_content', 'preset_music', 'music_file', 'music_start_time', 'music_end_time', 'voicemail', 'image_file', 'video_clip', 'ghost_draft']
        widgets = {
            'sender_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional)',
                'maxlength': '100'
            }),
            'receiver_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Recipient name (required)',
                'maxlength': '100'
            }),
            'message_content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your unsent message here...',
                'rows': 8
            }),
            'music_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'audio/*',
            }),
            'voicemail': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'audio/*',
                'style': 'display:none;'
            })
            ,
            'image_file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'style': 'display:none;'
            }),
            'video_clip': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*',
                'style': 'display:none;'
            }),
            'ghost_draft': forms.Textarea(attrs={
                'style': 'display:none;',
                'readonly': 'readonly'
            })
        }

class MessageSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by sender or receiver name (case-insensitive)...',
            'autocomplete': 'off'
        })
    )
