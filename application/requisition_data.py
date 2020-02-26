import json
import datetime


class RequisitionData(object):
    def __init__(self, user_id, uri, access_time, request_method, user_agent):
        self.user_id = user_id
        self._uri = uri
        self._access_time = access_time
        self._request_method = request_method
        self._user_agent = user_agent

    @property
    def uri(self):
        return self._uri

    @uri.setter
    def uri(self, uri):
        self._uri = uri

    @property
    def access_time(self):
        return self._access_time

    @access_time.setter
    def access_time(self, access_time):
        self._access_time = access_time

    @property
    def request_method(self):
        return self._request_method

    @request_method.setter
    def request_method(self, request_method):
        self._request_method = request_method

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self, user_agent):
        self._user_agent = user_agent


class RequisitionDataEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, RequisitionData):
            return {
                'user_id': o.user_id,
                'uri': o.uri,
                'access_time': o.access_time,
                'request_method': o.request_method,
                'user_agent': o.user_agent
            }
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        else:
            return json.JSONEncoder.default(self, o)

