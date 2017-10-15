class HSPConnector:

    base_url = "http://sms.hspsms.com/"
    key_username = 'username'
    key_api = 'apikey'
    key_numbers = 'numbers'
    key_smstype = 'smstype'
    key_sendername = 'sendername'
    key_message = 'message'
    key_scheduled = 'scheduled'
    key_group = 'gname'
    key_from = 'from'
    key_to = 'to'
    key_query = '?'
    key_query_separater = '&'
    key_msgid = 'msgid'

    def __init__(self, username: str, apikey: str, sender: str, smstype: str):
        self.username = username
        self.api_key = apikey
        self.sender = sender
        self.sms_type = smstype

    def send_request(self, url:str):
        import requests

        self.response = requests.get(url)

    def send_sms(self, recipient: list, message: str, sendername: str = None, smstype: str = None,
                 scheduled: str = None):
        from urllib import parse

        url = 'sendSMS'

        params = {self.key_username: self.username, self.key_api: self.api_key, self.key_message: message,
                  self.key_sendername: sendername or self.sender, self.key_smstype: smstype or self.sms_type}

        if scheduled:
            params[self.key_scheduled] = scheduled

        self.send_request(self.base_url + url + self.key_query + parse.urlencode(params) + self.key_numbers + '='
                          + ','.join(recipient))

        return self.parse_response()

    def delivery_report(self, msgid: str):
        from urllib import parse

        url = 'getDLR'

        params = {self.key_username: self.username, self.key_api: self.api_key, self.key_msgid: msgid}

        self.send_request(self.base_url + url + self.key_query + parse.urlencode(params))

        return self.parse_response()

    def parse_response(self):
        if 200 <= self.response.status_code < 300:
            return self.response.json()
