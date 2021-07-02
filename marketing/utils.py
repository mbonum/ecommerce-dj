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
from django.utils.translation import gettext_lazy as _


MAILCHIMP_API_KEY = getattr(settings, "MAILCHIMP_API_KEY", None)
if MAILCHIMP_API_KEY is None:
    raise NotImplementedError("MAILCHIMP_API_KEY must be set in the settings")

MAILCHIMP_DATA_CENTER = getattr(settings, "MAILCHIMP_DATA_CENTER", None)
if MAILCHIMP_DATA_CENTER is None:
    raise NotImplementedError(
        "MAILCHIMP_DATA_CENTER must be set in the settings, e.g. us6"
    )

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)
if MAILCHIMP_EMAIL_LIST_ID is None:
    raise NotImplementedError("MAILCHIMP_EMAIL_LIST_ID must be set.")


def check_email(email):
    if not re.match(r".+@.+\..+", email):
        raise ValueError(_("Please enter a valid email address"))
    return


def get_subscriber_hash(member_email):
    """
    This makes an email hash which is required by the Mailchimp API
    """
    check_email(member_email)
    member_email = member_email.lower().encode()
    _m = hashlib.md5(member_email)
    return _m.hexdigest()


class Mailchimp(object):
    def __init__(self):
        super(Mailchimp, self).__init__()
        self.key = MAILCHIMP_API_KEY
        self.api_url = f"https://{MAILCHIMP_DATA_CENTER}.api.mailchimp.com/3.0"
        self.list_id = MAILCHIMP_EMAIL_LIST_ID
        self.list_endpoint = f"{self.api_url}/lists/{self.list_id}"

    def get_members_endpoint(self):
        # endpoint = f"{self.list_endpoint}/members"
        return self.list_endpoint + "/members"  # endpoint

    def change_subscription_status(self, email, status="unsubscribed"):
        """
        , check_status=False
        """
        hashed_email = get_subscriber_hash(email)
        # members_endpoint = self.get_members_endpoint()
        endpoint = (
            self.get_members_endpoint() + "/" + hashed_email
        )  # f"{members_endpoint}/{hashed_email}"
        data = {"status": self.check_valid_status(status)}
        # if check_status:
        #     return requests.get(endpoint, auth=('', self.key)).json()
        # auth=("", MAILCHIMP_API_KEY)
        r = requests.put(endpoint, auth=("", self.key), data=json.dumps(data))
        return r.status_code, r.json()

    def check_subscription_status(self, email):
        hashed_email = get_subscriber_hash(email)
        endpoint = self.get_members_endpoint() + "/" + hashed_email
        # endpoint = "{members_endpoint}/{sub_hash}".format(
        #     members_endpoint=members_endpoint, sub_hash=subscriber_hash
        # )
        r = requests.get(endpoint, auth=("", self.key))  # "", MAILCHIMP_API_KEY))
        return r.status_code, r.json()

    def check_valid_status(self, status):
        choices = ["subscribed", "unsubscribed", "cleaned", "pending"]
        if status not in choices:
            raise ValueError(_("Not a valid email status"))
        return status

    # def add_email(self, email):
    #     check_email(email)
    #     endpoint = self.get_members_endpoint()
    #     data = {"email_address": email, "status": "subscribed"}
    #     _r = requests.post(
    #         endpoint, auth=("", MAILCHIMP_API_KEY), data=json.dumps(data)
    #     )
    #     return (
    #         _r.status_code,
    #         _r.json(),
    #     )  # self.change_subscription_status(email, status='subscribed')
    def add_email(self, email):
        # status = "subscribed"
        # self.check_valid_status(status)
        # data = {
        #     "email_address": email,
        #     "status": status
        # }
        # endpoint = self.get_members_endpoint()
        # r = requests.post(endpoint, auth=("", self.key), data=json.dumps(data))
        return self.change_subscription_status(email, status="subscribed")

    def unsubscribe(self, email):
        return self.change_subscription_status(email, status="unsubscribed")

    def subscribe(self, email):
        return self.change_subscription_status(email, status="subscribed")

    def pending(self, email):
        return self.change_subscription_status(email, status="pending")
