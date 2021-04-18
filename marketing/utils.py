"""
pip install requests
https://mailchimp.com/developer/reference/lists/#%20
https://mailchimp.com/developer/reference/lists/list-members/
"""
import hashlib
import json
import re
import requests
from django.conf import settings

MAILCHIMP_API_KEY = getattr(settings, "MAILCHIMP_API_KEY", None)
if MAILCHIMP_API_KEY is None:
    raise NotImplementedError("MAILCHIMP_API_KEY must be set in the settings")

MAILCHIMP_DATA_CENTER = getattr(settings, "MAILCHIMP_DATA_CENTER", None)
if MAILCHIMP_DATA_CENTER is None:
    raise NotImplementedError(
        "MAILCHIMP_DATA_CENTER must be set in the settings, e.g. us17"
    )

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)
if MAILCHIMP_EMAIL_LIST_ID is None:
    raise NotImplementedError(
        "MAILCHIMP_EMAIL_LIST_ID must be set in the settings, like us19"
    )


def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError("Please enter a valid email address")
    return


def get_subscriber_hash(member_email):
    """
    This makes a email hash which is required by the Mailchimp API
    """
    check_email(member_email)
    member_email = member_email.lower().encode()
    _m = hashlib.md5(member_email)
    return _m.hexdigest()


class Mailchimp(object):
    def __init__(self):
        super(Mailchimp, self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = "https://{dc}.api.mailchimp.com/3.0".format(
            dc=MAILCHIMP_DATA_CENTER
        )
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = "{api_url}/lists/{list_id}".format(
            api_url=self.api_url, list_id=self.list_id
        )

    def get_members_endpoint(self):

        endpoint = "{list_endpoint}/members".format(list_endpoint=self.list_endpoint)
        return endpoint

    def add_email(self, email):
        """
        Redundancy
        """
        check_email(email)
        endpoint = self.get_members_endpoint()
        data = {"email_address": email, "status": "subscribed"}
        _r = requests.post(
            endpoint, auth=("", MAILCHIMP_API_KEY), data=json.dumps(data)
        )
        return (
            _r.status_code,
            _r.json(),
        )  # self.change_subscription_status(email, status='subscribed')

    def check_valid_status(self, status):
        """"""
        choices = ["subscribed", "unsubscribed", "cleaned", "pending"]
        if status not in choices:
            raise ValueError("Not a valid choice")
        return status

    def change_subscription_status(self, email, status):
        """
        status='unsubscribed', check_status=False
        """
        subscriber_hash = get_subscriber_hash(email)
        members_endpoint = self.get_members_endpoint()
        endpoint = "{members_endpoint}/{sub_hash}".format(
            members_endpoint=members_endpoint, sub_hash=subscriber_hash
        )
        data = {"status": self.check_valid_status(status)}
        # if check_status:
        #     return requests.get(endpoint, auth=('', self.key)).json()
        _r = requests.put(endpoint, auth=("", MAILCHIMP_API_KEY), data=json.dumps(data))
        return _r.status_code, _r.json()

    def check_subscription_status(self, email):
        """"""
        subscriber_hash = get_subscriber_hash(email)
        members_endpoint = self.get_members_endpoint()
        endpoint = "{members_endpoint}/{sub_hash}".format(
            members_endpoint=members_endpoint, sub_hash=subscriber_hash
        )
        _r = requests.get(endpoint, auth=("", MAILCHIMP_API_KEY))
        return _r.status_code, _r.json()

    def unsubscribe(self, email):
        """Shortcuts"""
        return self.change_subscription_status(email, status="unsubscribed")

    def subscribe(self, email):
        return self.change_subscription_status(email, status="subscribed")

    def pending(self, email):
        return self.change_subscription_status(email, status="pending")
