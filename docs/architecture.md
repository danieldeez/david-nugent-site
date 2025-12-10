# Project Architecture: David Nugent Barrister Website

## Overview
Production-bound website supporting:
• Public legal pages (Premium Legal UI)
• Owner CMS (pages, practice areas, blogs, case studies)
• AI Assistant (DeepSeek chat widget)
• Emerging custom booking system (slot-based)
• Secure deployment on Render

## Tech Stack
- Django 5
- Python 3
- HTML / CSS / JS (Bootstrap 5 + custom legal styling)
- DeepSeek API for AI assistant
- SQLite locally, Render PostgreSQL recommended for production
- WhiteNoise for static files
- S3/R2 recommended for media persistence

## Directory Skeleton
- core/ — settings, URLs, WSGI
- pages/ — models, views, CMS logic
- templates/ — all site templates including CRM
- static/ — CSS/JS/images
- ai/prompts/ — system prompts for AI components
- docs/ — architecture + operational manuals

## Core Functional Areas

### 1. Public Website
- Homepage (Premium Legal UI hero, practice areas preview, trust elements)
- Practice Areas (description blocks + CMS editable content)
- About Page (portrait, biography, legal credentials)
- Blog Posts (CMS-managed)
- Case Studies (CMS-managed)
- Contact page (form + consent)
- Booking page (to be replaced with custom booking)

### 2. Owner CMS
- CRUD for Pages, Practice Areas, Blogs, Case Studies
- Dashboard-only access via custom /owner/login
- Non-technical UX with legal-friendly forms

### 3. AI Assistant
- Floating widget
- DeepSeek-powered answers with disclaimers
- Endpoint: /api/assist/
- Prompts controlled via /ai/prompts

### 4. Booking System (In Progress)
- Owner-defined availability slots
- User submission with details and Revolut payment confirmation
- Email notification (optional)
- NO on-site payments at this stage

### 5. Deployment
- Render.com with:
   - Procfile
   - build.sh
   - environment variables
   - security middleware
   - static collection
