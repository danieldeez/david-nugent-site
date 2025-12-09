"""
Script to populate sample content for the barrister site.
Run with: python manage.py shell < populate_sample_content.py
"""

from pages.models import SitePage, PracticeArea, BlogPost, CaseStudy, HomepageSettings
from django.utils import timezone
from datetime import timedelta

print("Starting content population...")

# 1. Update Privacy Policy
print("Creating Privacy Policy...")
privacy, created = SitePage.objects.get_or_create(slug="privacy")
privacy.title = "Privacy Policy"
privacy.body = """<h3>1. Introduction</h3>
<p>David Nugent ("we", "our", "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, and safeguard your personal information when you use our website or engage our legal services.</p>

<h3>2. Information We Collect</h3>
<p>We may collect the following types of information:</p>
<ul>
  <li>Contact details (name, email address, phone number)</li>
  <li>Details about your legal matter provided through contact forms or consultations</li>
  <li>Website usage data through cookies and analytics</li>
</ul>

<h3>3. How We Use Your Information</h3>
<p>We use your personal information to:</p>
<ul>
  <li>Provide legal services and respond to your inquiries</li>
  <li>Schedule consultations and communicate about your matters</li>
  <li>Improve our website and services</li>
  <li>Comply with legal and professional obligations</li>
</ul>

<h3>4. Data Security</h3>
<p>We implement appropriate technical and organisational measures to protect your personal information against unauthorised access, alteration, disclosure, or destruction.</p>

<h3>5. Your Rights</h3>
<p>Under GDPR and Irish data protection law, you have rights including access to your data, correction, deletion, and objection to processing. To exercise these rights, please contact us.</p>

<h3>6. Contact</h3>
<p>For questions about this Privacy Policy, please contact chambers at the details provided on our contact page.</p>

<p class="small text-muted mt-4">Last updated: December 2025</p>
"""
privacy.save()
print(f"  {'Created' if created else 'Updated'} Privacy Policy")

# 2. Update Terms of Use
print("Creating Terms of Use...")
terms, created = SitePage.objects.get_or_create(slug="terms")
terms.title = "Terms of Use"
terms.body = """<h3>1. Acceptance of Terms</h3>
<p>By accessing and using this website, you accept and agree to be bound by these Terms of Use. If you do not agree, please do not use this website.</p>

<h3>2. Nature of Information</h3>
<p>The information on this website is for general informational purposes only and does not constitute legal advice. No solicitor-client relationship is created by your use of this website or by contacting us through the website.</p>

<h3>3. Professional Services</h3>
<p>David Nugent is a barrister practising in Ireland. Legal services are provided in accordance with the Code of Conduct of the Bar of Ireland and applicable professional regulations.</p>

<h3>4. Limitation of Liability</h3>
<p>While we strive to keep information accurate and up-to-date, we make no representations or warranties about the completeness, accuracy, or reliability of information on this website.</p>

<h3>5. Intellectual Property</h3>
<p>All content on this website, including text, graphics, logos, and images, is the property of David Nugent or used with permission and is protected by copyright law.</p>

<h3>6. External Links</h3>
<p>This website may contain links to external websites. We are not responsible for the content or privacy practices of third-party sites.</p>

<h3>7. Changes to Terms</h3>
<p>We reserve the right to modify these Terms of Use at any time. Continued use of the website after changes constitutes acceptance of the modified terms.</p>

<h3>8. Governing Law</h3>
<p>These Terms of Use are governed by the laws of Ireland. Any disputes shall be subject to the exclusive jurisdiction of the Irish courts.</p>

<p class="small text-muted mt-4">Last updated: December 2025</p>
"""
terms.save()
print(f"  {'Created' if created else 'Updated'} Terms of Use")

# 3. Update About Page
print("Creating About page...")
about, created = SitePage.objects.get_or_create(slug="about")
about.title = "About"
about.body = """<p class="lead">David Nugent is a barrister specialising in commercial and employment law, with a practice spanning Ireland and the UK.</p>

<h3 class="mt-4">Called to the Bar</h3>
<p>David was called to the Bar of Ireland in 2015 and has since developed a busy practice advising individuals, businesses, and institutions on complex commercial and employment matters.</p>

<h3 class="mt-4">Practice Focus</h3>
<p>David's practice focuses on three main areas:</p>
<ul>
  <li><strong>Employment Law:</strong> Advising on unfair dismissal claims, discrimination, redundancy, employment contracts, and workplace investigations</li>
  <li><strong>Commercial Litigation:</strong> Contract disputes, shareholder matters, injunctive relief, and debt recovery proceedings</li>
  <li><strong>Regulatory:</strong> Professional discipline proceedings, compliance matters, and statutory appeals</li>
</ul>

<h3 class="mt-4">Qualifications & Memberships</h3>
<ul>
  <li>Barrister-at-Law, King's Inns (2015)</li>
  <li>BCL (Law and Business), University College Dublin</li>
  <li>Member, Bar of Ireland</li>
  <li>Member, Employment Law Association of Ireland</li>
</ul>

<h3 class="mt-4">Approach</h3>
<p>David is known for providing clear, practical advice focused on commercial outcomes. He works closely with solicitors and clients to develop effective strategies, whether through negotiation, mediation, or litigation.</p>

<p>David accepts instructions from solicitors and, where appropriate under the Bar of Ireland's direct access scheme, from members of the public.</p>
"""
about.save()
print(f"  {'Created' if created else 'Updated'} About page")

# 4. Create Practice Areas
print("Creating Practice Areas...")
employment, created = PracticeArea.objects.get_or_create(
    slug="employment-law",
    defaults={
        "name": "Employment Law",
        "description": "Comprehensive advice on all aspects of employment law for both employers and employees.",
        "detail": """<p class="lead">David provides expert advice and representation in all areas of employment law, acting for both employers and employees.</p>

<h3>Areas of Expertise</h3>
<ul>
  <li>Unfair dismissal claims before the Workplace Relations Commission and Labour Court</li>
  <li>Discrimination and equality claims</li>
  <li>Redundancy and restructuring</li>
  <li>Employment contract drafting and review</li>
  <li>Restrictive covenants and confidentiality</li>
  <li>Workplace investigations and disciplinary procedures</li>
  <li>TUPE transfers and outsourcing</li>
  <li>Executive terminations and settlement agreements</li>
</ul>

<h3>Recent Matters</h3>
<p>David has recently advised on:</p>
<ul>
  <li>High-value constructive dismissal claims in the technology sector</li>
  <li>Complex discrimination claims involving whistleblowing elements</li>
  <li>Employment aspects of corporate restructuring and redundancy programmes</li>
  <li>Enforcement of restrictive covenants in senior executive contracts</li>
</ul>

<p class="mt-4"><a href="/contact/" class="btn btn-cta">Discuss your employment matter</a></p>
""",
        "order": 1
    }
)
print(f"  {'Created' if created else 'Updated'} Employment Law")

commercial, created = PracticeArea.objects.get_or_create(
    slug="commercial-litigation",
    defaults={
        "name": "Commercial Litigation",
        "description": "Resolving business disputes through negotiation, mediation, and court proceedings.",
        "detail": """<p class="lead">David acts for businesses and individuals in a wide range of commercial disputes in the Irish courts and through alternative dispute resolution.</p>

<h3>Areas of Expertise</h3>
<ul>
  <li>Contract disputes and breach of contract claims</li>
  <li>Shareholder disputes and company law matters</li>
  <li>Injunctive relief and urgent applications</li>
  <li>Debt recovery and enforcement</li>
  <li>Commercial property disputes</li>
  <li>Partnership disputes</li>
  <li>Professional negligence claims</li>
  <li>Commercial mediation and arbitration</li>
</ul>

<h3>Court Experience</h3>
<p>David regularly appears in:</p>
<ul>
  <li>High Court (Commercial Court and Chancery Division)</li>
  <li>Circuit Court</li>
  <li>Court of Appeal</li>
</ul>

<h3>Approach</h3>
<p>David focuses on achieving commercial outcomes for clients, whether through negotiated settlements, mediation, or litigation. He provides clear advice on the strengths and risks of each case and works with solicitors to develop cost-effective strategies.</p>

<p class="mt-4"><a href="/contact/" class="btn btn-cta">Discuss your commercial dispute</a></p>
""",
        "order": 2
    }
)
print(f"  {'Created' if created else 'Updated'} Commercial Litigation")

regulatory, created = PracticeArea.objects.get_or_create(
    slug="regulatory-law",
    defaults={
        "name": "Regulatory & Professional Discipline",
        "description": "Defending professionals in regulatory investigations and discipline proceedings.",
        "detail": """<p class="lead">David represents professionals facing regulatory investigations and disciplinary proceedings before professional bodies and tribunals.</p>

<h3>Areas of Expertise</h3>
<ul>
  <li>Professional discipline proceedings (medical, legal, financial services, and other sectors)</li>
  <li>Regulatory investigations and compliance</li>
  <li>Fitness to practise hearings</li>
  <li>Statutory appeals and judicial review</li>
  <li>Licensing and regulatory applications</li>
  <li>Health and safety prosecutions</li>
  <li>Data protection and GDPR compliance</li>
</ul>

<h3>Professional Bodies</h3>
<p>David has appeared before:</p>
<ul>
  <li>Medical Council of Ireland</li>
  <li>Solicitors Disciplinary Tribunal</li>
  <li>Financial Services and Pensions Ombudsman</li>
  <li>Various professional regulatory bodies</li>
</ul>

<h3>Sensitive Matters</h3>
<p>David understands the serious personal and professional consequences of regulatory proceedings. He provides discreet, strategic advice aimed at protecting clients' reputations and livelihoods.</p>

<p class="mt-4"><a href="/contact/" class="btn btn-cta">Discuss your regulatory matter</a></p>
""",
        "order": 3
    }
)
print(f"  {'Created' if created else 'Updated'} Regulatory Law")

# 5. Create Blog Posts
print("Creating Blog Posts...")
blog1, created = BlogPost.objects.get_or_create(
    slug="remote-working-employment-contracts",
    defaults={
        "title": "Remote Working and Employment Contracts: Key Legal Issues",
        "summary": "With remote work now commonplace, employers and employees need to understand the legal implications for employment contracts and workplace rights.",
        "body": """<p class="lead">The shift to remote and hybrid working has transformed the workplace, but many employment contracts haven't caught up. This creates legal uncertainties for both employers and employees.</p>

<h3>Contractual Terms</h3>
<p>Traditional employment contracts typically specify a fixed workplace. When employees work remotely, questions arise:</p>
<ul>
  <li>Is the employee entitled to work remotely, or is it at the employer's discretion?</li>
  <li>Can the employer require a return to the office?</li>
  <li>What happens if the employee moves to a different jurisdiction?</li>
</ul>

<h3>The Right to Request Remote Working</h3>
<p>Under Irish law, employees with at least 26 weeks' service have the right to <em>request</em> remote working. However, employers can refuse on reasonable grounds related to the business.</p>

<h3>Health and Safety</h3>
<p>Employers retain health and safety obligations even when employees work from home. This includes:</p>
<ul>
  <li>Risk assessments of home working environments</li>
  <li>Provision of suitable equipment</li>
  <li>Policies on working hours and breaks</li>
</ul>

<h3>Cross-Border Issues</h3>
<p>Remote working across borders raises complex questions about:</p>
<ul>
  <li>Which country's employment law applies</li>
  <li>Tax residency and PAYE obligations</li>
  <li>Social security contributions</li>
</ul>

<h3>Practical Steps</h3>
<p>Employers should:</p>
<ol>
  <li>Review and update employment contracts to address remote working</li>
  <li>Implement clear remote working policies</li>
  <li>Ensure equipment and expense policies are fair</li>
  <li>Consider tax and legal implications of cross-border remote work</li>
</ol>

<p>Employees should ensure they understand their contractual position and any company policies before assuming a right to permanent remote working.</p>

<p class="alert alert-info mt-4"><i class="bi bi-info-circle me-2"></i><strong>Need advice?</strong> If you're facing issues with remote working arrangements, <a href="/contact/">contact chambers</a> to discuss your situation.</p>
""",
        "published": True,
        "published_at": timezone.now() - timedelta(days=15)
    }
)
print(f"  {'Created' if created else 'Updated'} Blog: Remote Working")

blog2, created = BlogPost.objects.get_or_create(
    slug="restrictive-covenants-enforceability",
    defaults={
        "title": "Restrictive Covenants: When Are They Enforceable?",
        "summary": "Irish courts take a strict approach to restrictive covenants. Understanding the legal test is crucial for both employers and employees.",
        "body": """<p class="lead">Restrictive covenants in employment contracts—clauses preventing employees from competing, soliciting clients, or poaching staff—are common. But enforceability is far from guaranteed.</p>

<h3>The Legal Test</h3>
<p>Irish law starts from the position that restrictive covenants are <strong>void as restraints of trade</strong> unless the employer can show they are:</p>
<ol>
  <li>Necessary to protect a legitimate business interest</li>
  <li>Reasonable in scope (time, geography, and activities restricted)</li>
  <li>Not contrary to public policy</li>
</ol>

<h3>Legitimate Business Interests</h3>
<p>Courts will only enforce covenants protecting genuine business interests such as:</p>
<ul>
  <li>Trade secrets and confidential information</li>
  <li>Customer connections and goodwill</li>
  <li>Stability of the workforce</li>
</ul>

<p>A covenant cannot simply prevent competition or protect against the loss of a skilled employee.</p>

<h3>Reasonableness</h3>
<p>Even where there's a legitimate interest, the covenant must be no wider than necessary:</p>
<ul>
  <li><strong>Duration:</strong> 6-12 months is typical; longer periods face scrutiny</li>
  <li><strong>Geography:</strong> Must relate to where the employee actually worked</li>
  <li><strong>Scope:</strong> Must be limited to genuinely competing activities</li>
</ul>

<h3>Common Mistakes</h3>
<p>Employers often make covenants unenforceable by:</p>
<ul>
  <li>Using standard "template" clauses without tailoring to the role</li>
  <li>Making covenants too broad in scope or duration</li>
  <li>Failing to provide consideration (e.g., in contracts with existing employees)</li>
  <li>Including multiple restrictions that compound to be unreasonable</li>
</ul>

<h3>Garden Leave</h3>
<p>An alternative or complement to restrictive covenants is a garden leave clause, allowing the employer to require the employee to stay away from work during their notice period while still employed.</p>

<h3>For Employees</h3>
<p>If you're subject to a restrictive covenant:</p>
<ul>
  <li>Check whether it's actually enforceable under the legal test</li>
  <li>Take legal advice before starting a new role that might breach it</li>
  <li>Consider whether your former employer is likely to enforce it</li>
  <li>Be aware that breaches can result in injunctions and damages claims</li>
</ul>

<p class="alert alert-info mt-4"><i class="bi bi-info-circle me-2"></i>Restrictive covenants require careful drafting and individual assessment. For advice on drafting or challenging a covenant, <a href="/contact/">get in touch</a>.</p>
""",
        "published": True,
        "published_at": timezone.now() - timedelta(days=45)
    }
)
print(f"  {'Created' if created else 'Updated'} Blog: Restrictive Covenants")

blog3, created = BlogPost.objects.get_or_create(
    slug="commercial-court-procedure",
    defaults={
        "title": "Navigating the Commercial Court: A Practical Guide",
        "summary": "The Commercial Court offers fast-track resolution of business disputes. Here's what you need to know about procedure and requirements.",
        "body": """<p class="lead">Ireland's Commercial Court, established in 2004, provides an efficient forum for resolving high-value commercial disputes. Understanding its procedures is essential for businesses considering litigation.</p>

<h3>What Cases Qualify?</h3>
<p>The Commercial Court hears disputes:</p>
<ul>
  <li>Valued at €1 million or more</li>
  <li>Arising from commercial transactions or relationships</li>
  <li>Where speed and commercial expertise would be beneficial</li>
</ul>

<p>Common case types include contract disputes, shareholder disputes, banking litigation, and intellectual property matters.</p>

<h3>Key Advantages</h3>
<p>The Commercial Court offers:</p>
<ul>
  <li><strong>Speed:</strong> Cases typically reach trial within 12 months</li>
  <li><strong>Judicial expertise:</strong> Judges with commercial law backgrounds</li>
  <li><strong>Active case management:</strong> Tight control of procedure and costs</li>
  <li><strong>Limited discovery:</strong> Focus on essential documents only</li>
</ul>

<h3>Procedure</h3>
<p>Key procedural features include:</p>

<h4>1. Entry to the List</h4>
<p>Parties must apply for entry to the Commercial List, demonstrating the case meets the criteria. Both plaintiff and defendant must agree (or the Court must order) entry.</p>

<h4>2. Case Management</h4>
<p>The Court maintains tight control through regular case management conferences. Judges expect parties to be ready to progress matters efficiently.</p>

<h4>3. Pleadings</h4>
<p>Pleadings must be clear and concise. The Court discourages lengthy, technical pleadings and focuses on the real commercial issues.</p>

<h4>4. Discovery</h4>
<p>Discovery is limited to essential documents. The Court expects parties to cooperate and avoid disproportionate discovery applications.</p>

<h4>5. Hearings</h4>
<p>Trials are typically shorter than in the general High Court list. The Court appreciates concise written submissions and focused oral argument.</p>

<h3>Costs Considerations</h3>
<p>While the Commercial Court is faster, it's not necessarily cheaper:</p>
<ul>
  <li>The condensed timetable requires intensive preparation</li>
  <li>Expert senior counsel is typically required</li>
  <li>Multiple interlocutory hearings add to costs</li>
</ul>

<p>However, the certainty of a rapid resolution often makes it the most cost-effective option for high-value disputes.</p>

<h3>Alternative Dispute Resolution</h3>
<p>The Commercial Court actively encourages mediation and other forms of ADR. Many cases settle after entry to the list as parties focus on the real issues and trial date approaches.</p>

<h3>Practical Tips</h3>
<ul>
  <li>Engage experienced commercial litigation counsel early</li>
  <li>Ensure your case genuinely meets the €1m threshold</li>
  <li>Be prepared for an aggressive timetable once listed</li>
  <li>Consider ADR seriously before incurring full trial costs</li>
  <li>Maintain realistic settlement discussions throughout</li>
</ul>

<p class="alert alert-info mt-4"><i class="bi bi-info-circle me-2"></i>If you're considering Commercial Court proceedings, <a href="/contact/">contact chambers</a> to discuss your case strategy.</p>
""",
        "published": True,
        "published_at": timezone.now() - timedelta(days=72)
    }
)
print(f"  {'Created' if created else 'Updated'} Blog: Commercial Court")

# 6. Create Case Studies
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
        "date": timezone.now() - timedelta(days=180),
        "practice_area": employment,
        "published": True,
        "published_at": timezone.now() - timedelta(days=90)
    }
)
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
        "date": timezone.now() - timedelta(days=240),
        "practice_area": commercial,
        "published": True,
        "published_at": timezone.now() - timedelta(days=120)
    }
)
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
        "date": timezone.now() - timedelta(days=300),
        "practice_area": regulatory,
        "published": True,
        "published_at": timezone.now() - timedelta(days=150)
    }
)
print(f"  {'Created' if created else 'Updated'} Case: Medical Council")

print("\n✓ Content population complete!")
print("\nSummary:")
print("- Privacy Policy: Updated")
print("- Terms of Use: Updated")
print("- About Page: Updated")
print("- Practice Areas: 3 created (Employment, Commercial, Regulatory)")
print("- Blog Posts: 3 created")
print("- Case Studies: 3 created")
