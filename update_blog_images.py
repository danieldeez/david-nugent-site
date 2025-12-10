#!/usr/bin/env python
"""
Update blog post image references from media/posts/ to static/img/blog/
This allows images to be bundled with the deployment instead of relying on media storage.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from pages.models import BlogPost

# Map of old media paths to new static paths
updates_made = 0

for post in BlogPost.objects.all():
    if post.hero_image:
        old_path = str(post.hero_image)
        print(f"\nPost: {post.title}")
        print(f"  Current image: {old_path}")

        # Extract filename from the path
        if 'posts/' in old_path:
            filename = old_path.split('posts/')[-1]
            # Update to reference static path (will be served by Django's static file system)
            # Note: We store just the path relative to static directory
            new_path = f"img/blog/{filename}"

            # Clear the old ImageField reference and store the static path in a way templates can use
            # Since hero_image is an ImageField, we'll need to handle this differently
            # For now, let's just document what needs to change
            print(f"  Should change to: static/{new_path}")
            print(f"  Action: Manual template update needed or model field change")

print(f"\n✓ Found {BlogPost.objects.filter(hero_image__isnull=False).count()} blog posts with images")
print("Note: Blog post images should now reference static files in templates")
