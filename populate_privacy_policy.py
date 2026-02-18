"""
Populate Privacy Policy page with GDPR-compliant content.
Run with: python manage.py shell < populate_privacy_policy.py
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from pages.models import SitePage

privacy_content = """
<h2>Privacy Policy</h2>

<p><strong>Last Updated:</strong> [Date]</p>

<p>This privacy policy explains how [Barrister Name] ("we", "us", "our") collects, uses, and protects your personal data when you use this website.</p>

<h3>1. Data Controller</h3>
<p>The data controller responsible for your personal data is:</p>
<ul>
    <li><strong>Name:</strong> [Barrister Name] BL</li>
    <li><strong>Address:</strong> [Chambers Address]</li>
    <li><strong>Email:</strong> [Contact Email]</li>
    <li><strong>Phone:</strong> [Contact Phone]</li>
</ul>

<h3>2. What Data We Collect</h3>
<p>We collect the following types of personal data when you use our services:</p>

<h4>2.1 Contact Form Enquiries</h4>
<ul>
    <li>Name</li>
    <li>Email address</li>
    <li>Phone number (optional)</li>
    <li>Message content</li>
    <li>Date and time of submission</li>
</ul>

<h4>2.2 Consultation Bookings</h4>
<ul>
    <li>Full name</li>
    <li>Email address</li>
    <li>Phone number (optional)</li>
    <li>Brief description of your legal matter</li>
    <li>Preferred consultation date and time</li>
</ul>

<h4>2.3 Technical Data</h4>
<ul>
    <li>IP address (for rate limiting and security)</li>
    <li>Browser type and version</li>
    <li>Pages visited and time spent on site</li>
</ul>

<h3>3. How We Use Your Data</h3>
<p>We process your personal data for the following purposes:</p>
<ul>
    <li><strong>Enquiry Response:</strong> To respond to your contact form submissions and assess whether we can assist</li>
    <li><strong>Booking Management:</strong> To schedule and manage consultation appointments</li>
    <li><strong>Communication:</strong> To provide updates about your consultation or respond to queries</li>
    <li><strong>Legal Compliance:</strong> To comply with our professional obligations and legal requirements</li>
</ul>

<h3>4. Legal Basis for Processing</h3>
<p>We process your data under the following legal bases:</p>
<ul>
    <li><strong>Consent:</strong> You provide explicit consent when submitting forms</li>
    <li><strong>Legitimate Interests:</strong> Processing is necessary for providing legal services</li>
    <li><strong>Legal Obligation:</strong> Processing is necessary to comply with professional and legal obligations</li>
</ul>

<h3>5. Third-Party Data Processors</h3>
<p>We may share your data with the following third-party service providers:</p>

<h4>5.1 Hosting Provider</h4>
<p>This website is hosted on Render.com. Your data is stored on secure servers in [Region]. Please see Render's privacy policy for more information.</p>

<h4>5.2 AI Assistant (Optional)</h4>
<p>If you use our AI chat assistant, your messages may be processed by an external AI service provider (such as DeepSeek or similar) to provide responses. This processing:</p>
<ul>
    <li>Is limited to the text of your question</li>
    <li>Does not include your name, email, or other identifying information</li>
    <li>Is used solely for generating responses</li>
    <li>Is not stored by the third-party provider</li>
</ul>

<h3>6. Data Retention</h3>
<p>We retain your personal data for the following periods:</p>
<ul>
    <li><strong>Contact Form Enquiries:</strong> [6 months] from submission, unless converted to an active matter</li>
    <li><strong>Consultation Bookings:</strong> [12 months] from consultation date</li>
    <li><strong>Active Matters:</strong> In accordance with our professional retention obligations (typically 7 years)</li>
</ul>
<p>After these periods, data will be securely deleted or anonymized unless we have a legal obligation to retain it longer.</p>

<h3>7. Your Rights Under GDPR</h3>
<p>You have the following rights regarding your personal data:</p>
<ul>
    <li><strong>Right to Access:</strong> Request a copy of the personal data we hold about you</li>
    <li><strong>Right to Rectification:</strong> Request correction of inaccurate or incomplete data</li>
    <li><strong>Right to Erasure:</strong> Request deletion of your personal data (subject to legal obligations)</li>
    <li><strong>Right to Restrict Processing:</strong> Request limitation on how we use your data</li>
    <li><strong>Right to Data Portability:</strong> Request a copy of your data in a machine-readable format</li>
    <li><strong>Right to Object:</strong> Object to processing based on legitimate interests</li>
    <li><strong>Right to Withdraw Consent:</strong> Withdraw consent at any time (does not affect prior processing)</li>
</ul>

<p>To exercise any of these rights, please contact us at [Contact Email].</p>

<h3>8. Data Security</h3>
<p>We implement appropriate technical and organizational measures to protect your personal data, including:</p>
<ul>
    <li>HTTPS encryption for all data transmission</li>
    <li>Secure server infrastructure with regular security updates</li>
    <li>Access controls limiting who can view your data</li>
    <li>Regular backups with encryption</li>
    <li>Staff training on data protection</li>
</ul>

<h3>9. Cookies and Tracking</h3>
<p>This website uses the following cookies:</p>
<ul>
    <li><strong>Session Cookies:</strong> Essential for the booking system functionality (expires when you close your browser)</li>
    <li><strong>CSRF Protection:</strong> Security cookie to prevent cross-site request forgery</li>
</ul>
<p>We do not use tracking cookies, analytics cookies, or third-party advertising cookies.</p>

<h3>10. International Data Transfers</h3>
<p>Your data is stored within the European Economic Area (EEA). If we transfer data outside the EEA, we ensure appropriate safeguards are in place (such as Standard Contractual Clauses).</p>

<h3>11. Children's Privacy</h3>
<p>This website is not intended for children under 18. We do not knowingly collect personal data from children.</p>

<h3>12. Changes to This Policy</h3>
<p>We may update this privacy policy from time to time. The "Last Updated" date at the top of this page indicates when the policy was last revised. We encourage you to review this policy periodically.</p>

<h3>13. Complaints</h3>
<p>If you have concerns about how we handle your personal data, you have the right to lodge a complaint with the Data Protection Commission (Ireland):</p>
<ul>
    <li><strong>Website:</strong> <a href="https://www.dataprotection.ie" target="_blank">www.dataprotection.ie</a></li>
    <li><strong>Phone:</strong> +353 (0)761 104 800</li>
    <li><strong>Email:</strong> info@dataprotection.ie</li>
</ul>

<h3>14. Contact Us</h3>
<p>If you have questions about this privacy policy or how we handle your data, please contact us:</p>
<ul>
    <li><strong>Email:</strong> [Contact Email]</li>
    <li><strong>Phone:</strong> [Contact Phone]</li>
    <li><strong>Post:</strong> [Chambers Address]</li>
</ul>

<hr>

<p><small><strong>Important Notice:</strong> Submitting an enquiry through this website does not create a solicitor-client or barrister-client relationship. No legal advice is provided through this website or the contact process.</small></p>
"""

# Create or update privacy policy
page, created = SitePage.objects.get_or_create(
    slug='privacy',
    defaults={
        'title': 'Privacy Policy',
        'body': privacy_content
    }
)

if not created:
    page.body = privacy_content
    page.save()
    print("Privacy policy UPDATED")
else:
    print("Privacy policy CREATED")
