"""
Script to populate remaining sample content (Practice Areas and Case Studies).
Run with: python manage.py shell < populate_remaining_content.py
"""

from pages.models import PracticeArea, CaseStudy
from django.utils import timezone
from datetime import timedelta

print("Creating remaining content...")

# Create Practice Areas (without 'detail' field - just name, slug, description, order)
print("Creating Practice Areas...")
employment, created = PracticeArea.objects.get_or_create(
    slug="employment-law",
    defaults={
        "name": "Employment Law",
        "description": "Comprehensive advice on unfair dismissal, discrimination, redundancy, employment contracts, and workplace investigations for both employers and employees.",
        "order": 1
    }
)
print(f"  {'Created' if created else 'Updated'} Employment Law")

commercial, created = PracticeArea.objects.get_or_create(
    slug="commercial-litigation",
    defaults={
        "name": "Commercial Litigation",
        "description": "Resolving business disputes through negotiation, mediation, and court proceedings. Contract disputes, shareholder matters, injunctions, and debt recovery.",
        "order": 2
    }
)
print(f"  {'Created' if created else 'Updated'} Commercial Litigation")

regulatory, created = PracticeArea.objects.get_or_create(
    slug="regulatory-law",
    defaults={
        "name": "Regulatory & Professional Discipline",
        "description": "Defending professionals in regulatory investigations and discipline proceedings before professional bodies and tribunals.",
        "order": 3
    }
)
print(f"  {'Created' if created else 'Updated'} Regulatory Law")

# Create Case Studies
print("Creating Case Studies...")
case1, created = CaseStudy.objects.get_or_create(
    slug="unfair-dismissal-whistleblowing",
    defaults={
        "title": "Unfair Dismissal with Whistleblowing Elements",
        "summary": "Successfully represented senior executive in high-value constructive dismissal claim involving alleged whistleblowing retaliation.",
        "body": """<h3>Background</h3>
<p>Our client was a senior finance manager at a technology company. After raising concerns internally about accounting irregularities, she experienced a significant deterioration in her working relationship with senior management.</p>

<p>Within months, her responsibilities were reduced, she was excluded from key meetings, and subjected to an aggressive performance improvement process. She ultimately resigned and claimed constructive dismissal.</p>

<h3>Legal Issues</h3>
<p>The case raised complex questions:</p>
<ul>
  <li>Whether the client's concerns constituted "protected disclosures" under whistleblowing legislation</li>
  <li>Whether the employer's conduct amounted to a fundamental breach of contract</li>
  <li>The appropriate level of compensation given the client's seniority and difficulty finding equivalent employment</li>
</ul>

<h3>Strategy</h3>
<p>We advised on:</p>
<ul>
  <li>Careful documentation of the whistleblowing concerns and subsequent treatment</li>
  <li>Exhausting internal grievance procedures before resignation</li>
  <li>Preserving evidence of exclusion and changes to responsibilities</li>
  <li>Framing the claim to maximize protection under whistleblowing legislation</li>
</ul>

<h3>Outcome</h3>
<p>The case proceeded to a full hearing at the Workplace Relations Commission. Following detailed evidence and legal submissions, the Adjudication Officer found:</p>
<ul>
  <li>The client's concerns constituted protected disclosures</li>
  <li>The employer's treatment was in retaliation for those disclosures</li>
  <li>The conduct amounted to a fundamental breach of the employment contract</li>
</ul>

<p>The client was awarded substantial compensation reflecting her seniority, length of service, and the whistleblowing retaliation finding. The award was in the top tier for WRC constructive dismissal cases.</p>

<h3>Key Takeaways</h3>
<ul>
  <li>Document protected disclosures carefully and follow proper procedures</li>
  <li>Keep detailed records of any subsequent detrimental treatment</li>
  <li>Don't resign hastily—exhaust internal procedures where possible</li>
  <li>Whistleblowing claims can significantly increase compensation awards</li>
</ul>
""",
        "outcome": "Substantial compensation awarded at WRC hearing",
        "date_of_case": (timezone.now() - timedelta(days=180)).date(),
        "published": True,
        "published_at": timezone.now() - timedelta(days=90)
    }
)
if created:
    case1.practice_areas.add(employment)
print(f"  {'Created' if created else 'Updated'} Case: Unfair Dismissal")

case2, created = CaseStudy.objects.get_or_create(
    slug="shareholder-dispute-injunction",
    defaults={
        "title": "Shareholder Dispute and Emergency Injunction",
        "summary": "Obtained urgent injunction preventing improper removal of director and protecting client's shareholding in family business.",
        "body": """<h3>Background</h3>
<p>Our client held a 30% shareholding in a successful family manufacturing business. Following a disagreement with the majority shareholder (his brother), our client was suddenly removed as a director at an improperly-convened board meeting.</p>

<p>The majority shareholder then attempted to force through a share buyback at a significant undervalue, threatening to exclude our client from management and dividends.</p>

<h3>Urgent Action Required</h3>
<p>With a crucial shareholders' meeting scheduled within days, immediate court intervention was necessary to preserve our client's position.</p>

<h3>Legal Strategy</h3>
<p>We advised on and obtained:</p>
<ul>
  <li>An urgent <em>ex parte</em> injunction restraining the proposed shareholders' meeting</li>
  <li>An order requiring production of company books and records</li>
  <li>Interlocutory relief preventing any changes to share capital or board composition</li>
</ul>

<p>The application relied on:</p>
<ul>
  <li>Breaches of the company's articles of association</li>
  <li>Failure to give proper notice of board and shareholder meetings</li>
  <li>Unfairly prejudicial conduct by the majority shareholder</li>
  <li>Undervaluation of the client's shareholding</li>
</ul>

<h3>High Court Proceedings</h3>
<p>At the initial <em>ex parte</em> hearing, we secured an immediate interim injunction. At the interlocutory hearing (on notice to the respondents), we successfully argued:</p>
<ul>
  <li>There was a serious issue to be tried regarding breaches of company law</li>
  <li>Damages would not be an adequate remedy</li>
  <li>The balance of convenience favored preserving the <em>status quo</em></li>
</ul>

<p>The Court granted injunctions preventing:</p>
<ul>
  <li>Removal of our client as director</li>
  <li>Any dilution or forced buyback of his shares</li>
  <li>Exclusion from company information</li>
</ul>

<h3>Resolution</h3>
<p>With the court's protection in place, negotiations proceeded from a position of strength. The case ultimately settled with:</p>
<ul>
  <li>Our client's reinstatement as a director</li>
  <li>An agreement on fair dividend distributions</li>
  <li>A shareholders' agreement protecting minority shareholder rights</li>
  <li>An option for either party to purchase the other's shares at a fair valuation</li>
</ul>

<h3>Key Lessons</h3>
<ul>
  <li>Act quickly when minority shareholder rights are threatened</li>
  <li>Maintain detailed records of all board and shareholder decisions</li>
  <li>Shareholders' agreements are crucial in family businesses</li>
  <li>Injunctive relief can reset negotiations and protect your position</li>
</ul>
""",
        "outcome": "Emergency injunction granted; matter settled protecting client's interests",
        "date_of_case": (timezone.now() - timedelta(days=240)).date(),
        "published": True,
        "published_at": timezone.now() - timedelta(days=120)
    }
)
if created:
    case2.practice_areas.add(commercial)
print(f"  {'Created' if created else 'Updated'} Case: Shareholder Dispute")

case3, created = CaseStudy.objects.get_or_create(
    slug="professional-discipline-medical",
    defaults={
        "title": "Medical Council Fitness to Practise Proceedings",
        "summary": "Successfully defended surgeon in serious professional discipline proceedings before the Medical Council, preserving client's career.",
        "body": """<h3>Background</h3>
<p>Our client, a highly experienced surgeon, faced a formal complaint to the Medical Council alleging poor professional performance relating to a complex surgical procedure.</p>

<p>The complaint, if upheld, could have resulted in conditions on practice, suspension, or even erasure from the medical register—effectively ending a distinguished 20-year career.</p>

<h3>The Challenge</h3>
<p>The case involved:</p>
<ul>
  <li>Complex medical evidence requiring expert testimony</li>
  <li>Questions of surgical judgment in difficult clinical circumstances</li>
  <li>The balance between honest clinical error and professional misconduct</li>
  <li>Significant media interest in the proceedings</li>
</ul>

<h3>Our Approach</h3>
<p>We worked closely with the client and medical experts to:</p>
<ul>
  <li>Analyze the clinical records and surgical decisions in detail</li>
  <li>Obtain supportive expert opinions from leading surgeons</li>
  <li>Prepare the client for giving evidence under cross-examination</li>
  <li>Develop a clear narrative explaining the clinical reasoning</li>
  <li>Address each allegation comprehensively in written submissions</li>
</ul>

<h3>The Hearing</h3>
<p>The Fitness to Practise hearing spanned multiple days and included:</p>
<ul>
  <li>Detailed expert medical evidence on both sides</li>
  <li>Cross-examination of the complainant and witnesses</li>
  <li>Our client's direct evidence and cross-examination</li>
  <li>Legal submissions on the appropriate standard of care</li>
</ul>

<p>Key to our defense was demonstrating:</p>
<ul>
  <li>The surgical judgment was within the range of reasonable responses</li>
  <li>Appropriate protocols and procedures were followed</li>
  <li>The outcome, while unfortunate, did not indicate poor professional performance</li>
  <li>Our client's otherwise exemplary career and ongoing commitment to professional development</li>
</ul>

<h3>Outcome</h3>
<p>After careful deliberation, the Fitness to Practise Committee found:</p>
<ul>
  <li>The complaint was not well-founded</li>
  <li>The surgical care provided was appropriate in the circumstances</li>
  <li>No further action was required</li>
</ul>

<p>The decision fully vindicated our client, allowing continuation of practice without restriction.</p>

<h3>Significance</h3>
<p>This case highlights:</p>
<ul>
  <li>The importance of early expert review in professional discipline cases</li>
  <li>The need for careful preparation and clear presentation of complex evidence</li>
  <li>How regulatory bodies distinguish between poor outcomes and poor performance</li>
  <li>The value of experienced advocacy in high-stakes professional proceedings</li>
</ul>

<p class="alert alert-warning mt-4"><i class="bi bi-exclamation-triangle me-2"></i>If you're facing professional discipline proceedings, early legal advice is crucial. <a href="/contact/">Contact us</a> to discuss your case in confidence.</p>
""",
        "outcome": "Complaint not well-founded; no sanction imposed",
        "date_of_case": (timezone.now() - timedelta(days=300)).date(),
        "published": True,
        "published_at": timezone.now() - timedelta(days=150)
    }
)
if created:
    case3.practice_areas.add(regulatory)
print(f"  {'Created' if created else 'Updated'} Case: Medical Council")

print("\n✓ All remaining content created!")
print("\nFinal Summary:")
print("- Practice Areas: 3 created")
print("- Case Studies: 3 created")
