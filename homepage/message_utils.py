"""
Custom utilities for message processing in The Flora Project.
Provides intelligent message summarization and metadata extraction.
"""

import re
from typing import Dict, Tuple


def extract_message_sentiment_keywords(content: str) -> Dict[str, list]:
    """
    Extract sentiment-based keywords from message content.
    Identifies emotional tone and key themes in unsent messages.
    
    Args:
        content (str): The message content to analyze
        
    Returns:
        Dict with 'positive', 'negative', and 'neutral' keyword lists
    """
    
    positive_words = {
        'love', 'happy', 'joy', 'grateful', 'appreciate', 'beautiful',
        'wonderful', 'amazing', 'proud', 'smile', 'laugh', 'hug', 'kiss',
        'treasure', 'cherish', 'blessed', 'hope', 'believe', 'forever'
    }
    
    negative_words = {
        'sorry', 'regret', 'miss', 'sad', 'angry', 'hurt', 'pain',
        'disappointed', 'broken', 'tears', 'lonely', 'fear', 'lost',
        'struggle', 'difficult', 'hard', 'wish', 'should have'
    }
    
    neutral_words = {
        'remember', 'time', 'think', 'tell', 'know', 'always', 'never',
        'want', 'need', 'understand', 'believe', 'feel', 'say'
    }
    
    content_lower = content.lower()
    
    found_positive = [word for word in positive_words if word in content_lower]
    found_negative = [word for word in negative_words if word in content_lower]
    found_neutral = [word for word in neutral_words if word in content_lower]
    
    return {
        'positive': found_positive,
        'negative': found_negative,
        'neutral': found_neutral
    }


def generate_message_preview(content: str, max_length: int = 150) -> str:
    """
    Generate an intelligent preview of a message.
    Truncates at word boundary and preserves readability.
    
    Args:
        content (str): Full message content
        max_length (int): Maximum preview length
        
    Returns:
        str: Preview text with ellipsis if truncated
    """
    
    # Remove extra whitespace
    content = ' '.join(content.split())
    
    if len(content) <= max_length:
        return content
    
    # Truncate at word boundary
    preview = content[:max_length]
    last_space = preview.rfind(' ')
    
    if last_space > max_length * 0.7:  # Only if reasonable word boundary
        return preview[:last_space] + '...'
    
    return preview + '...'


def calculate_message_engagement_score(message_obj) -> float:
    """
    Calculate an engagement score based on message attributes.
    Scores messages with multimedia content higher.
    
    Args:
        message_obj: UnsentMessage model instance
        
    Returns:
        float: Engagement score between 0.0 and 10.0
    """
    
    score = 5.0  # Base score
    
    # Content length bonus
    content_length = len(message_obj.message_content)
    if content_length > 500:
        score += 2.0
    elif content_length > 200:
        score += 1.0
    
    # Multimedia bonus
    if message_obj.music_file or message_obj.preset_music:
        score += 1.5
    if message_obj.voicemail:
        score += 1.5
    if message_obj.image_file or message_obj.video_clip:
        score += 1.0
    
    # Named sender bonus (more personal)
    if message_obj.sender_name:
        score += 0.5
    
    # Cap at 10.0
    return min(10.0, score)
