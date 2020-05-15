# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "recover_deleted"
app_title = "Recover Deleted Docs"
app_publisher = "Marcos Vinicius Fernandes Machado"
app_description = "Recover deleted documents"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = ""
app_license = "MIT"

doc_events = {
	"*": {
		"after_insert": "recover.main.notify_deleted"
	}
}
