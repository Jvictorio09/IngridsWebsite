import os
from django.conf import settings
from django.template import Library

register = Library()

@register.simple_tag
def webp_image(image_path):
    """
    Returns the WebP version of an image if it exists, otherwise returns the original path.
    """
    # Full path to the static directory
    static_dir = os.path.join(settings.BASE_DIR, 'myApp', 'static')

    # Construct the WebP file path
    webp_path = os.path.splitext(image_path)[0] + '.webp'
    webp_full_path = os.path.join(static_dir, webp_path)

    # Debugging output to confirm paths
    print(f"Original Path: {image_path}")
    print(f"WebP Path: {webp_path}")
    print(f"Full WebP Path: {webp_full_path}")
    print(f"WebP File Exists: {os.path.exists(webp_full_path)}")

    # Check if the WebP file exists
    if os.path.exists(webp_full_path):
        # Return the WebP path for use in the <img> tag
        return f"{settings.STATIC_URL}{webp_path}"
    else:
        # Fallback to the original image
        return f"{settings.STATIC_URL}{image_path}"
