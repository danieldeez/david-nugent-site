# QA v1.0 Checklist — David Nugent BL Site

## How to use
Work through each section in order after every deploy.
Mark each item ✅ PASS or ❌ FAIL with a note.

---

## 1. Smoke Tests (curl — run before anything else)

```bash
BASE=https://your-render-url.onrender.com   # replace with live URL

# Public pages — all should return 200
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

# Should return 404 (not 500)
curl -sI $BASE/owner/          | head -1   # redirects to login, not 500
curl -sI $BASE/calendar/badkey.ics | head -1  # should be 404

# Static assets
curl -sI $BASE/static/css/site.css | head -1  # should be 200
```

---

## 2. Public — Enquiry Flow (`/contact/` or `/intake/`)

- [ ] Page loads without error
- [ ] Form shows: Name (optional), Email (optional), Matter description (required), Consent checkbox
- [ ] Consent checkbox label includes **Privacy Policy link** (GDPR required)
- [ ] Submit **without** ticking consent → form rejects with inline error on checkbox
- [ ] Submit **without** filling Matter description → form rejects with inline error
- [ ] Submit a **valid** form → redirects to `/intake/thank-you/<uuid>/`
- [ ] Thank-you page shows submitted date, name/email if provided, reference UUID
- [ ] No legal advice text anywhere on page

### Triage branching (thank-you page)

| Scenario | Expected outcome |
|----------|-----------------|
| Barrister-appropriate matter (e.g., "I have a Circuit Court date next month for assault charge, have solicitor") | Green alert + **Book a Consultation** button shown |
| Solicitor-level matter (e.g., "I need to transfer my house to my daughter") | Amber alert, told to contact chambers, no booking button |
| LLM not configured / triage fails | Neutral text, "contact chambers" CTA, no booking button |

---

## 3. Public — Booking Flow (`/book/`)

- [ ] `/book/` loads, shows list of available dates (or empty-state if none)
- [ ] Click a date → `/book/date/YYYY-MM-DD/` loads with time slots
- [ ] Click a slot → `/book/slot/<pk>/` loads booking form
- [ ] Booking form shows: Name*, Email*, Phone (opt), Description*, Consent*
- [ ] Submit **without** Name → validation error shows inline (not as raw Django UL dump)
- [ ] Submit **without** consent → checkbox error shown
- [ ] Submit **valid** form → redirects to `/book/success/<id>/`
- [ ] Success page shows booking details (date, time, type, client name, email)
- [ ] Success page shows Revolut QR if `static/img/revolut-qr.png` exists; otherwise shows placeholder text
- [ ] Success page does **not** show "@davidnugent (placeholder)" text
- [ ] Success page shows correct email/phone from env vars (not hardcoded)
- [ ] Slot is marked unavailable after successful booking (won't appear again)

---

## 4. Owner CRM — Login

- [ ] `/site-access-dk2847/` shows login form
- [ ] Wrong credentials → error shown, no 500
- [ ] Correct staff credentials → redirects to `/owner/`
- [ ] Navbar shows "Owner" gear icon when logged in as staff

---

## 5. Owner CRM — Dashboard

- [ ] All 9 cards visible: Homepage, About, Practice Areas, Blog Posts, Case Studies, Site Pages, Availability Slots, Bookings, Enquiries
- [ ] Each card's button navigates to the correct section
- [ ] Admin panel link opens `/admin/` in new tab

---

## 6. Owner CRM — Enquiries (`/owner/intake/`)

- [ ] Table shows enquiries with: Received date, Contact, Matter (truncated), AI Status badge, Actions
- [ ] "Read full text" link opens modal with full text **(modals must open — they were broken before this fix)**
- [ ] Modal footer has "View Full Details" button
- [ ] "View Details" → `/owner/intake/<uuid>/` loads intake detail
- [ ] Detail page shows: submission info, triage status badge, triage result (if run)
- [ ] **Run Full AI Analysis** button → triggers POST to `/owner/intake/<uuid>/analyse/`
- [ ] After analysis: case_type, urgency, key_facts, risk_flags, suitability_hint display correctly
- [ ] Re-run button appears after first analysis

---

## 7. Owner CRM — Bookings (`/owner/bookings/`)

- [ ] List shows all bookings with Client, Date/Time, Type, Description, Payment status
- [ ] **View** button navigates to `/owner/bookings/<pk>/` **(was missing before this fix)**
- [ ] **Paid/Unpaid** toggle button changes payment status
- [ ] Booking detail page shows: client info, slot details, payment status, linked intake ref if applicable
- [ ] Linked enquiry card shows "View Enquiry Details" button

---

## 8. Owner CRM — Availability (`/owner/availability/`)

- [ ] List shows existing slots
- [ ] New slot form: date, start_time, end_time, type, notes
- [ ] End time before start time → validation error shown
- [ ] Created slot appears in public `/book/` if `is_available=True` and date is in future

---

## 9. Calendar Feed

- [ ] `/calendar/<wrong_key>.ics` returns 404
- [ ] `/calendar/<correct_secret>.ics` returns 200 with `text/calendar` content type
- [ ] ICS content begins with `BEGIN:VCALENDAR` and ends with `END:VCALENDAR`
- [ ] Only **paid** bookings appear in feed (unpaid bookings excluded)
- [ ] Only **future** bookings appear (past slots excluded)
- [ ] Each VEVENT has: SUMMARY, DTSTART, DTEND, DESCRIPTION, LOCATION, UID
- [ ] Outlook subscription: subscribe via File → Account Settings → Internet Calendars → New. Paste the full ICS URL. Note: Outlook refreshes every few hours, not instantly.

---

## 10. UI / Global Consistency

- [ ] Navbar brand, email, phone in topbar match env vars (not "01 XXX XXXX" placeholder)
- [ ] Navbar collapses correctly on mobile (hamburger menu works)
- [ ] Active nav link highlighted on each page
- [ ] Footer shows correct address, email, phone from env vars
- [ ] "Submit an Enquiry" and "Book Consultation" CTAs both visible on home hero
- [ ] Blog card images load correctly when a `hero_image` has been uploaded
- [ ] About page portrait loads from uploaded image or falls back to `static/img/headshot.jpg`

---

## 11. Safety / GDPR

- [ ] No page provides legal advice content
- [ ] Consent checkbox is on all 3 forms (contact/intake, booking, implicitly elsewhere)
- [ ] Privacy Policy is linked from consent checkbox label
- [ ] Privacy Policy page (`/privacy/`) is accessible and not a blank placeholder in production
- [ ] Calendar ICS description contains only Booking ID + Intake Ref — no PII (name, email, phone)
- [ ] Chat widget does NOT appear (ASSISTANT_ENABLED not set or set to 0)

---

## 12. Known Remaining Items (not fixed in this pass)

| Item | Notes |
|------|-------|
| `about.html` credentials section has hardcoded "LLB (Hons) Irish Law, 2021" | Managed content — update via Owner → About Page |
| No confirmation email to client after booking | Email backend not configured (would need SMTP + email view) |
| CKEditor 4 security warning | Pre-existing; consider upgrading when time allows |
| `revolut-qr.png` not in repo | Upload via admin or add to `static/img/` and commit |
| No pagination on intake list or booking list | Fine for low volume; add if list grows large |

---

## Render Deploy Verification

After `git push origin main` and Render auto-deploys:

1. Check Render build logs — no errors
2. Run smoke tests above against the live URL
3. Log in to owner area and verify enquiries modal + booking view button work
4. Check topbar shows correct phone (not "01 XXX XXXX")
5. Submit a test enquiry via `/contact/` and confirm thank-you page loads
