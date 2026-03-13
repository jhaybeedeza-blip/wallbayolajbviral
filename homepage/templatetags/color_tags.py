from django import template

register = template.Library()

@register.filter
def is_pink(color):
    """
    Check if a color is in the pink/rose spectrum.
    Checks if the color hex code is predominantly pink/red with high red component.
    """
    if not color or not isinstance(color, str):
        return False
    
    # Remove # if present
    color = color.lstrip('#')
    
    # Ensure it's a valid hex color
    if len(color) != 6:
        return False
    
    try:
        # Parse hex color
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        
        # Pink detection: high red component, moderate green, moderate-high blue
        # Pink variations include colors where red is dominant
        # Examples: #FF6B6B, #FFA07A, #F1948A, #F5B7B1
        
        # Check if it's a pink-ish color
        # Pink: R > 200, G < R, B < R (for lighter pinks)
        # Or: R is highest, and it's not too yellow (G not too close to R)
        if r >= 200 and r > g and r > b:
            # It's a red-ish color, check if it's pink (not pure red)
            if g >= 100 or b >= 100:  # Has some other component
                return True
        
        # Alternative pink detection: HSL-like approach for softer pinks
        # If red is significantly higher than green and blue, it's pink
        if r > g and r > b and (r - g) > 50:
            return True
            
    except (ValueError, IndexError):
        return False
    
    return False
