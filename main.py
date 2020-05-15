from __future__ import unicode_literals
import frappe
import frappe.defaults
from frappe.utils import nowdate, cstr, flt, cint, now ,getdate
from frappe import throw, _
from frappe.utils import formatdate, get_number_format_info
import requests
import json
import datetime

@frappe.whitelist()
def notify_delete_recover(doc,event):
	try:
		doc = doc.as_dict()
		if 'comment_type' in doc and 'Deleted' in doc.comment_type:
			name = doc.subject.split(" ")[-1]
			sql = "select * from `tabDeleted Document` where deleted_name = '{deleted_name}'".format(deleted_name = name)
			result = frappe.db.sql(sql, as_dict=True)
			doc = result[0]
			data = doc.data.strip()
			msg = """
<h2>Warning - Monitored document deleted</h2>
<h3 style="color:#999999">Automatic send</h3>
<p>The system detected a delete event in one of monitored documents, follow below the deleted document, to recover just click in the recover button at the end</p>
<h3>Information:</h3><br>
<strong>Deleted document:</strong> {deldoc}<br>
<strong>Document name:</strong> {deldocname}<br>
<br>
<strong>Deleted by:</strong> {user}<br>
<strong>Date:</strong> {now}<br>
<h3>Document info:</h3><br>
<pre>{allinfo}</pre>
<br>
<h3>Recover?</h3>
<form action=http://frappe_ip_address/recover method="get">
<input type="hidden" id="key" name="key" value={id}>
<input type="submit" role="button" class="btn btn-primary" id="sbtn" value="Recover">
<input type="button" role="button" class="btn btn-secondary" value="Help">
</form>
""".format(deldoc=doc.deleted_doctype, deldocname=doc.deleted_name, user=doc.owner, now=frappe.utils.get_datetime(doc.creation).strftime('%m/%d/%Y %H:%M:%S'), allinfo=data, id=doc.name)
			subject = "[Warning] Monitored document deleted"
			recipients = "team@company.com"
			frappe.sendmail(recipients=recipients, subject=subject, message=msg, now=True)
		else:
			pass
	except Exception as e:
		print(e)
		pass

@frappe.whitelist()
def restore(name):
	print(name)
	deleted = frappe.get_doc('Deleted Document', name)
	if deleted.restored == 1:
		frappe.msgprint(_("Documento restored"))
		raise Exception('Document already been restored')
	doc = frappe.get_doc(json.loads(deleted.data))
	try:
		doc.insert()
	except frappe.DocstatusTransitionError:
		frappe.msgprint(_("Deleted document saved as draft"))
		doc.docstatus = 0
		doc.insert()
	doc.add_comment('Edit', _('restored {0} as {1}').format(deleted.deleted_name, doc.name))
	deleted.new_name = doc.name
	deleted.restored = 1
	deleted.db_update()

	frappe.msgprint(_("Document restored"))