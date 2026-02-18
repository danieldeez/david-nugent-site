# Agent Review Prompt — David Nugent BL Website

Use this prompt when assigning an agent to QA the live site end-to-end.

---

## Context

This is the live Django website for barrister David Nugent BL. It has:

- Public marketing pages (home, about, practice areas, blog, cases)
- An enquiry/intake form with AI triage
- A custom booking system (browse dates → pick slot → fill form → success page)
- An owner CRM (dashboard, enquiries, bookings, availability management)
- A private calendar ICS feed

The base URL is stored in `BASE`. Replace with the actual Render URL before running.

---

## What to check and verify

### 1. Global — Every page

**MUST have:**
- Navbar: brand name "David Nugent BL" on left; nav links About, Practice Areas, Insights, Case Studies; two buttons "Submit an Enquiry" + "Book Consultation"
- Navbar fits in one row at 100% zoom on a 1366px-wide screen (no overflow)
- Topbar above navbar: barrister email + phone (NOT "01 XXX XXXX" placeholder, NOT "info@davidnugent.ie")
- Footer: navigation links, privacy/terms links, address (Law Library, Four Courts), email, phone
- Active nav link is highlighted for the current page
- No hardcoded `01 XXX XXXX`, `david.nugent@lawlibrary.ie`, or `(placeholder)` text anywhere
- No AI chat widget button or panel visible (ASSISTANT_ENABLED is off)
- No legal advice statements

**MUST NOT have:**
- Nested `<main>` elements (only `base.html` provides `<main>`)
- The Revolut username `@davidnugent (placeholder)` text
- Raw Django UL error dumps (form errors must render as inline `<div>` text, not `<ul><li>` list tags)

---

### 2. Home page (`/`)

**MUST have:**
- Hero section with heading and subheading (CMS-managed)
- Two CTA buttons in hero: "Submit an Enquiry" → `/contact/` and "Book Consultation" → `/book/`
- Practice areas preview cards (3 columns)
- Case studies teaser section
- Blog teaser section
- Blog card images load from media storage (not `/static/img/`)

---

### 3. About page (`/about/`)

**MUST have:**
- Light background (NOT dark navy gradient) — the hero section must have a light/white background
- Portrait image (uploaded or fallback to `static/img/headshot.jpg`)
- Sidebar card with: barrister name, "Junior Counsel: [year]", qualifications, circuits, direct access note
- Biography text (CMS body content or default text)
- Biography text is readable dark text on light background (NOT white text)
- Credentials section: Areas of practice, Qualifications, Circuits, Professional access
- Bottom CTA strip: "Submit enquiry" + "Book consultation" buttons

---

### 4. Practice Areas page (`/practice-areas/`)

**MUST have:** Intro, grid of practice area cards, each with name + short summary

---

### 5. Blog (`/blog/`) and Cases (`/cases/`)

**MUST have:** Grid of cards; blog cards show hero image if uploaded; cards link to detail pages

---

### 6. Enquiry / Intake flow

#### `/contact/` or `/intake/`

**MUST have:**
- Fields: Name (optional), Email (optional), Matter description (required), Consent checkbox
- Consent label includes a clickable Privacy Policy link
- Submitting without ticking consent → inline error on the checkbox (NOT a 500, NOT silent fail)
- Submitting without matter description → inline error on that field
- Valid submission → redirects to `/intake/thank-you/<uuid>/`

#### `/intake/thank-you/<uuid>/`

**MUST have:**
- Submission date, name/email if provided, reference UUID shown
- Submitted matter text shown in a box

**Triage result section — three branches:**

| Branch | Condition | What must appear |
|--------|-----------|-----------------|
| Suitable | `is_suitable == True` | Green success alert + "Book a Consultation" button → `/book/?intake=<uuid>` + "Email Chambers" button → `mailto:` link |
| Unsuitable | `is_suitable == False` | Amber/neutral alert, explanation text + "Email Chambers" mailto button + phone `tel:` button |
| Pending/no triage | `is_suitable == None` | Neutral text, "Email Chambers" mailto button + phone `tel:` button |

**MUST NOT have:**
- "Contact Chambers" button linking to `{% url 'contact' %}` (this is the same enquiry form — circular loop). All "contact chambers" CTAs must be direct `mailto:` or `tel:` links.

---

### 7. Booking flow

#### `/book/` (index)

**MUST have:** List of available dates (slots where `is_available=True` and date is in future). Empty state if none.

#### `/book/date/YYYY-MM-DD/`

**MUST have:**
- List of time slots for that date
- Each slot shows: time range (e.g. "10:00 AM - 11:00 AM") and duration in minutes
- **MUST NOT show consultation type label** (e.g. "Initial Consultation •") — type has been removed from user-facing views

#### `/book/slot/<pk>/`

**MUST have:**
- Selected slot info card: date, time range, duration in minutes
- **MUST NOT show slot type label** in the slot info card
- Booking form fields: Full Name*, Email Address*, Phone (optional), Matter description*, Consent checkbox*
- Consent label includes clickable Privacy Policy link
- Submit without Name → inline validation error (not a raw `<ul>` error dump)
- Submit without consent → inline checkbox error

#### `/book/success/<id>/`

**MUST have:**
- Booking summary: date, time, consultation type (shown in booking summary only if still present in template), client name, email
- Payment instructions section with Revolut QR (or placeholder if QR not uploaded)
- Email and phone from env vars (NOT hardcoded)
- "What Happens Next?" steps
- "Questions or Need to Reschedule?" section with correct email/phone
- **MUST NOT show** `@davidnugent (placeholder)` text anywhere

---

### 8. Owner CRM — Login

- URL: `/site-access-dk2847/`
- Wrong credentials → error message, no 500
- Correct staff credentials → redirects to `/owner/`
- Navbar shows Owner gear icon when logged in as staff

---

### 9. Owner CRM — Dashboard (`/owner/`)

**MUST have** 9 cards visible and clickable:
Homepage, About, Practice Areas, Blog Posts, Case Studies, Site Pages, Availability Slots, Bookings, Enquiries

---

### 10. Owner CRM — Enquiries (`/owner/intake/`)

**MUST have:**
- Table with: Received date, Contact, Matter (truncated), AI Status badge, Actions
- "Read full text" opens a Bootstrap modal with the full text (modals must open — they were broken previously due to invalid HTML placement inside `<tbody>`)
- Modal footer has "View Full Details" link
- "View Details" navigates to `/owner/intake/<uuid>/`
- Detail page: submission info, triage status badge, triage result if run
- "Run Full AI Analysis" button triggers POST to `/owner/intake/<uuid>/analyse/`
- After analysis: case_type, urgency, key_facts, risk_flags, suitability_hint display correctly
- Re-run button appears after first analysis

---

### 11. Owner CRM — Bookings (`/owner/bookings/`)

**MUST have:**
- Table with: Client, Date/Time, Type, Description, Payment, Booked date, Actions
- **"View" button present on every row** — navigates to `/owner/bookings/<pk>/` (was missing before)
- "Paid/Unpaid" toggle button changes payment status inline
- Booking detail page: client info, slot details, payment status, linked intake ref if applicable

---

### 12. Owner CRM — Availability (`/owner/availability/`)

**MUST have:**
- Table: Date, Time, Duration, Status, Actions (NO "Type" column — slot type removed)
- Add New Slot form: Date, Start Time, End Time in a single 3-column row (col-md-4 each)
- **MUST NOT show a "Consultation Type" / slot type dropdown** in the owner slot form
- End time before start time → validation error shown
- New slot defaults to `slot_type='initial'` automatically (not selectable by owner)
- Created slot appears in public `/book/` when `is_available=True` and date is future

---

### 13. Calendar Feed

- `/calendar/<wrong_key>.ics` → 404
- `/calendar/<correct_secret>.ics` → 200, content-type `text/calendar`
- ICS starts with `BEGIN:VCALENDAR`, ends with `END:VCALENDAR`
- Only **paid** bookings in feed
- Only **future** bookings in feed
- Each VEVENT has: SUMMARY, DTSTART, DTEND, DESCRIPTION, LOCATION, UID
- DESCRIPTION contains Booking ID and Intake Ref only — **NO PII** (no name, email, phone)

---

### 14. Safety / GDPR

- No page provides legal advice content
- Consent checkbox + Privacy Policy link appears on: intake/contact form, booking form
- `/privacy/` accessible, not a blank placeholder
- Chat widget (AI assistant button/panel) does NOT appear on any page
- Calendar ICS description contains only booking ID + intake ref — no PII

---

## Smoke test commands (curl)

```bash
BASE=https://your-render-url.onrender.com

# All should return HTTP/2 200
curl -sI $BASE/                | head -1
curl -sI $BASE/about/          | head -1
curl -sI $BASE/practice-areas/ | head -1
curl -sI $BASE/blog/           | head -1
curl -sI $BASE/cases/          | head -1
curl -sI $BASE/contact/        | head -1
curl -sI $BASE/intake/         | head -1
curl -sI $BASE/book/           | head -1
curl -sI $BASE/privacy/        | head -1
curl -sI $BASE/terms/          | head -1

# Should NOT return 500
curl -sI $BASE/owner/                 | head -1   # redirects to login
curl -sI $BASE/calendar/badkey.ics    | head -1   # should be 404

# Static asset
curl -sI $BASE/static/css/site.css   | head -1   # should be 200
```

---

## Common failure modes to look for

| Symptom | Likely cause |
|---------|-------------|
| "Contact Chambers" button goes to the enquiry form | `{% url 'contact' %}` not replaced with `mailto:` |
| Intake list modals don't open | Modal divs inside `<tbody>` — move them after `</table>` |
| About page dark background | `.about-hero` still has navy gradient in site.css |
| Form errors show as raw bullet list | Template uses `{{ form.errors }}` instead of per-field `{{ form.field.errors }}` |
| Slot type picker shown in owner availability form | `slot_type` not removed from `AvailabilitySlotForm.Meta.fields` |
| Slot type label shown in booking flow | `{{ slot.get_slot_type_display }}` still in `booking_date.html` or `booking_slot.html` |
| Topbar shows "01 XXX XXXX" | `BARRISTER_PHONE` env var not set or settings default wrong |
| Blog card images broken | Template still uses `/static/img/{{ post.hero_image }}` instead of `{{ post.hero_image.url }}` |
| AI chat widget visible | `ASSISTANT_ENABLED` env var set to `1` or truthy in production |
