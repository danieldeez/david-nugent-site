<project>
  <name>Barrister Django Website</name>
  <purpose>
    This project is a professional Django-based website for barrister David Nugent.
    It includes static pages, CMS-managed pages, blog/cases, a contact form, 
    Calendly booking integration, and a lightweight AI assistant endpoint.
  </purpose>

  <rules>
    - Make minimal diffs; never rewrite whole files unless required.
    - Follow existing Django architecture (pages app, Templates/SitePages/, static/css/).
    - Do not change models or database schema unless explicitly asked.
    - Keep HTML using our Bootstrap 5 + navy theme patterns.
    - Never generate legal advice in content or examples.
    - When editing templates, preserve block structure and base.html inheritance.
    - When editing Python, keep imports organized and avoid unnecessary abstractions.
    - When adding new features, modify only the files you list in the plan.
  </rules>

  <cost_controls>
    - ALWAYS begin your response with:
      1) a short plan,
      2) list of files you will modify,
      3) then provide unified diffs.
    - Use minimal context; never restate entire files if a diff is enough.
    - Avoid generating unused or speculative code.
  </cost_controls>

  <file_structure>
    - core/: Django project settings + root URLs
    - pages/: main app (views, urls, admin, models, forms)
    - Templates/SitePages/: HTML templates
    - Templates/base.html: global layout
    - static/css/site.css: global styling
    - static/img/: images
  </file_structure>

  <styles>
    - Use Bootstrap 5 utilities and our existing navy color palette.
    - For cards/sections, follow existing patterns in home.html and practice_areas.html.
    - Keep copy concise and professional.
  </styles>

  <ai_assistant_constraints>
    - Never provide legal advice; only general information.
    - Avoid adding new LLM logic unless instructed.
    - The assistant backend is already implemented; front-end widget lives in base.html.
  </ai_assistant_constraints>

  <output_format>
    - Use <plan> and <diff> sections.
    - Example format:

      <plan>
      - Modify pages/views.py to add X
      - Modify Templates/SitePages/home.html to render Y
      </plan>

      <diff file="pages/views.py">
      @@ ... @@
      </diff>

    - Ask ONE clarifying question if something is ambiguous, otherwise proceed.
  </output_format>
</project>

{
  "site": {
    "global": {
      "layout": {
        "body_class": "bg-body",
        "container_default": "container",
        "section_vertical_spacing": "py-5",
        "hero_vertical_spacing": "py-6"
      },
      "typography": {
        "hero_heading": "display-5 fw-semibold",
        "section_heading": "h3 fw-semibold",
        "card_title": "h5",
        "body_text": "fs-6",
        "muted_text": "text-muted"
      },
      "colors": {
        "hero_bg": "#0b1a2a",
        "nav_bg": "bg-body-tertiary",
        "light_section_bg": "#f5f7fa",
        "card_bg": "#ffffff",
        "primary": "#2e8fff"
      },
      "navbar": {
        "class": "navbar navbar-expand-lg navbar-dark bg-body-tertiary shadow-sm sticky-top",
        "items": [
          { "label": "About", "href": "/about/" },
          { "label": "Practice Areas", "href": "/practice-areas/" },
          { "label": "Case Studies", "href": "/cases/" },
          { "label": "Blog", "href": "/blog/" },
          { "label": "Contact", "href": "/contact/" },
          {
            "label": "Book",
            "href": "/book/",
            "class": "btn btn-primary btn-sm px-3 ms-lg-3",
            "icon": "bi bi-calendar-check"
          }
        ]
      },
      "footer": {
        "background": "#0b1a2a",
        "columns": [
          { "type": "about_snippet" },
          {
            "type": "links",
            "items": [
              { "label": "About", "href": "/about/" },
              { "label": "Practice Areas", "href": "/practice-areas/" },
              { "label": "Case Studies", "href": "/cases/" },
              { "label": "Blog", "href": "/blog/" },
              { "label": "Book a Consultation", "href": "/book/" },
              { "label": "Contact", "href": "/contact/" }
            ]
          },
          {
            "type": "legal",
            "items": [
              { "label": "Privacy Policy", "href": "/privacy/" },
              { "label": "Terms of Use", "href": "/terms/" }
            ],
            "disclaimer": "This website provides general information only and does not constitute legal advice."
          }
        ]
      }
    },
    "pages": {
      "home": {
        "template": "Templates/SitePages/home.html",
        "sections": [
          { "type": "hero", "layout": "row gx-5 gy-4", "cols": ["col-lg-7", "col-lg-5"] },
          { "type": "practice_areas_preview", "grid": "row g-4", "col": "col-12 col-md-4" },
          { "type": "case_studies_teaser", "grid": "row g-4", "col": "col-12 col-md-6 col-lg-4" },
          { "type": "blog_teaser", "grid": "row g-4", "col": "col-12 col-md-6 col-lg-4" },
          { "type": "cta_strip" }
        ]
      },
      "practice_areas": {
        "template": "Templates/SitePages/practice_areas.html",
        "layout": {
          "intro": true,
          "grid": "row g-4",
          "card_col": "col-12 col-md-6 col-lg-4"
        }
      },
      "cases_index": {
        "template": "Templates/SitePages/case_list.html",
        "layout": {
          "grid": "row g-4",
          "card_col": "col-12 col-md-6 col-lg-4"
        },
        "card": {
          "classes": "card h-100 border-0 shadow-sm",
          "uses_practice_area_badge": true,
          "shows_year": true,
          "shows_outcome": true,
          "shows_summary": true
        }
      },
      "blog_index": {
        "template": "Templates/SitePages/blog_list.html",
        "layout": {
          "grid": "row g-4",
          "card_col": "col-12 col-md-6 col-lg-4"
        },
        "card": {
          "classes": "card h-100 border-0 shadow-sm",
          "image_ratio": "ratio ratio-16x9",
          "fallback_image_bg": "bg-dark-subtle",
          "shows_date": true,
          "shows_summary": true
        }
      },
      "about": {
        "template": "Templates/SitePages/about.html",
        "layout": {
          "row": "row g-5",
          "cols": ["col-lg-4", "col-lg-8"]
        }
      },
      "contact": {
        "template": "Templates/SitePages/contact.html",
        "layout": {
          "row": "row g-4",
          "cols": ["col-lg-5", "col-lg-7"],
          "form_card": "card shadow-sm border-0"
        }
      },
      "book": {
        "template": "Templates/SitePages/book.html",
        "layout": {
          "content_col": "col-lg-6",
          "embed_col": "col-lg-6"
        }
      }
    },
    "assistant": {
      "button_position": { "bottom": 20, "right": 20 },
      "panel_max_height_vh": 72,
      "z_index": 1100
    }
  }
}
