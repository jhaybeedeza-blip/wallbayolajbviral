from django.db import models
import json

class UnsentMessage(models.Model):
    sender_name = models.CharField(max_length=100, blank=True, null=True, help_text="Optional: Leave blank for anonymous")
    receiver_name = models.CharField(max_length=100, help_text="Required: Who this message is for")
    message_content = models.TextField(help_text="Your unsent message")
    music_file = models.FileField(upload_to='messages_music/', blank=True, null=True, help_text="Optional: Attach a music file (MP3, WAV, etc.)")
    preset_music = models.CharField(max_length=255, blank=True, null=True, help_text="Optional: Select from preset music collection")
    music_start_time = models.FloatField(blank=True, null=True, default=0, help_text="Song snippet start time in seconds")
    music_end_time = models.FloatField(blank=True, null=True, help_text="Song snippet end time in seconds")
    voicemail = models.FileField(upload_to='voicemails/', blank=True, null=True, help_text="Optional: Voice message recording")
    image_file = models.FileField(upload_to='messages_media/images/', blank=True, null=True, help_text="Optional: Photo captured from camera")
    video_clip = models.FileField(upload_to='messages_media/videos/', blank=True, null=True, help_text="Optional: Short video clip (max ~15s)")
    ghost_draft = models.TextField(blank=True, null=True, help_text="Deleted/overwritten text from drafting")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        sender = self.sender_name if self.sender_name else "Anonymous"
        return f"{sender} → {self.receiver_name}"
    
    def get_music_snippet_data(self):
        """Return music snippet timing info as dict"""
        if self.music_start_time is not None or self.music_end_time is not None:
            return {
                'start': float(self.music_start_time or 0),
                'end': float(self.music_end_time or 0),
                'duration': float((self.music_end_time or 0) - (self.music_start_time or 0))
            }
        return None
