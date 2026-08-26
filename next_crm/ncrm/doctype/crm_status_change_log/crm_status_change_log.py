# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


from frappe import session
from frappe.model.document import Document
from frappe.utils import get_datetime

from next_crm.utils import get_duration


class CRMStatusChangeLog(Document):
    pass


def add_status_change_log(doc):
    if not doc.is_new():
        previous_doc = doc.get_doc_before_save()

        if not previous_doc.status_change_log:
            previous_status = previous_doc.status
            previous_time = previous_doc.modified
        else:
            previous_status = previous_doc.status_change_log[-1].to
            previous_time = previous_doc.status_change_log[-1].to_date

        doc.append(
            "status_change_log",
            {
                "from": previous_status,
                "to": doc.status,
                "from_date": previous_time,
                "to_date": get_datetime(),
                "log_owner": session.user,
                "duration": get_duration(previous_time, get_datetime()),
            },
        )
