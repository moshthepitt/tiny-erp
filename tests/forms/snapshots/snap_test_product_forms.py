# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestProductForms::test_supplier_form 1'] = '''<p><label for="id_name">Name:</label> <input type="text" name="name" maxlength="2000" required id="id_name"></p>
<p><label for="id_contact_person">Contact Person:</label> <input type="text" name="contact_person" maxlength="2000" required id="id_contact_person"></p>
<p><label for="id_emails">Email Address(es):</label> <textarea name="emails" cols="40" rows="2" id="id_emails">
</textarea> <span class="helptext">Enter a comma-separated list of email addresses</span></p>
<p><label for="id_phones">Phone Number(s):</label> <textarea name="phones" cols="40" rows="2" id="id_phones">
</textarea> <span class="helptext">Enter a comma-separated list of phone numbers</span></p>'''

snapshots['TestProductForms::test_supplier_form 2'] = '''<p><label for="id_name">Name:</label> <input type="text" name="name" value="Umbrella Inc" maxlength="2000" required id="id_name"></p>
<p><label for="id_contact_person">Contact Person:</label> <input type="text" name="contact_person" value="Alice" maxlength="2000" required id="id_contact_person"></p>
<p><label for="id_emails">Email Address(es):</label> <textarea name="emails" cols="40" rows="2" id="id_emails">
b@example.com</textarea> <span class="helptext">Enter a comma-separated list of email addresses</span></p>
<p><label for="id_phones">Phone Number(s):</label> <textarea name="phones" cols="40" rows="2" id="id_phones">
+254711000000, +254722000000</textarea> <span class="helptext">Enter a comma-separated list of phone numbers</span></p>'''
