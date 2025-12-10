#!/usr/bin/env python
"""
Migrate blog post images from media to static references.
Updates the database to store just filenames, which templates will load from static.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from pages.models import BlogPost

print("Updating blog post image references to use static files...\n")

for post in BlogPost.objects.all():
    if post.hero_image:
        old_path = str(post.hero_image)

        # Extract just the filename
        if 'posts/' in old_path:
            filename = old_path.split('posts/')[-1]
        else:
            filename = os.path.basename(old_path)

        # Store just the filename - templates will prepend static/img/blog/
        post.hero_image = f"blog/{filename}"
        post.save()

        print(f"Updated: {post.title}")
        print(f"  Old: {old_path}")
        print(f"  New: blog/{filename}\n")

print("Done! Blog post images now reference static files.")
print("Images are available at: static/img/blog/")
