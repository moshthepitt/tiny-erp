# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestEmails::test_requisition_filed_email 1'] = '''Bob Ndoe sent this purchase requisition:

Date Placed: Jan. 1, 2019
Date Required: Feb. 2, 2019
Business: X Inc
Department: Science
Location: Voi
Staff Member: Bob Ndoe

Please log in to process the above: http://example.com/reviews/1

Thank you,


example.com
------
http://example.com'''

snapshots['TestEmails::test_requisition_filed_email 2'] = 'Bob Ndoe sent this purchase requisition:<br /><br />Date Placed: Jan. 1, 2019<br />Date Required: Feb. 2, 2019<br />Business: X Inc<br />Department: Science<br />Location: Voi<br />Staff Member: Bob Ndoe<br />Please log in to process the above: http://example.com/reviews/1<br /><br />Thank you,<br />example.com<br />------<br />http://example.com'
