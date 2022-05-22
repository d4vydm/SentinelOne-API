import requests
import json



# Suppress SSL warning
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)




##################################################
## APIError
class ApiError(Exception):
    """An API Error Exception"""
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "ApiError: status={}".format(self.status)





##################################################
## SentinelOne API CLIENT
class S1Client:
    def __init__(self, configfile):
        self.base_url = configfile['uri']
        self.api_token = configfile['api_token']
        self.api = configfile['api']

    def get_general_http_request(self, function):
        #Create API call URI
        fulluri = self.base_url \
            + self.api \
            + function

        #Call API
        resp = requests.get(
            url=fulluri,
            verify=False,
            headers={
                "Content-Type": "application/json",
                "Authorization": "ApiToken " + self.api_token
            }
        )

        if resp.status_code != 200:
            raise ApiError(f'CALL {function} '.format(resp.status_code))
        else:
            return resp

    def post_general_http_request(self, function, data):
        #Create API call URI
        fulluri = self.base_url \
            + self.api \
            + function

        #Call API
        resp = requests.post(
            url=fulluri, 
            data=data, 
            verify=False, 
            headers={\
                "Content-Type": "application/json", \
                "Authorization": "ApiToken " + self.api_token \
            }
        )

        if resp.status_code != 200:
            raise ApiError(f'CALL {function} '.format(resp.status_code) + json.dumps(resp.json()))
        else:
            return resp

    def get_filter_http_request(self, function, filter):
        """
        Takes the filter in json string format, like:
        {
            "groupIds": "...",
            "computerName": "..."
        }
        """

        #Create the filter in string
        filter_str=""
        if (filter != ""):
            filter_str="?"
            filter_dict=json.loads(filter)
            for f,v in filter_dict.items():
                filter_str+=f+"="+v+"&"
            filter_str=filter_str[:-1]

        #Create API call URI
        fulluri = self.base_url \
            + self.api \
            + function \
            + filter_str

        #Call API
        resp = requests.get(
            url=fulluri,
            verify=False,
            headers={
                "Content-Type": "application/json",
                "Authorization": "ApiToken " + self.api_token
            }
        )

        if resp.status_code != 200:
            raise ApiError(f'CALL {function} '.format(resp.status_code) + json.dumps(resp.json()))
        else:
            return resp

    def disconnect_from_network_http_request(self, data):
        """
        # Disconnect from Network
        """

        function = "agents/actions/disconnect"
        return self.post_general_http_request(function, data)

    def get_agents_http_request(self):
        """
        # Get Agents
        """

        function = "agents"
        return self.get_general_http_request(function)

    def get_agents_filter_http_request(self, filter):
        """
        # Get Agents by filter
        """

        function = "agents"
        return self.get_filter_http_request(function, filter)

    def get_threats_filter_http_request(self, filter):
        """
        # Get Threats by filter
        """

        function = "threats"
        return self.get_filter_http_request(function, filter)

    def update_threat_http_request(self, data):
        """
        # Update threat with given data
        """

        function = "threats/incident"
        return self.post_general_http_request(function, data)




def disconnect_from_network(s1client, data):
    """
    # Disconnect host from Network
    """

    resp = s1client.disconnect_from_network_http_request(data)

    name = 'SentinelOne disconnect host from network'
    output = json.dumps({"APICall": name, "Data": data, "Response": resp.json()}, indent=4)

    return output

def get_agents(s1client):
    """
    # Get setinelone agents
    """

    resp = s1client.get_agents_http_request()

    name = 'SentinelOne get Agents'
    output = json.dumps({"APICall": name, "Response": resp.json()}, indent=4)

    return output

def get_agents_filter(s1client, filter):
    """
    # Get setinelone agents by filter
    """

    resp = s1client.get_agents_filter_http_request(filter)

    name = 'SentinelOne get Agentsby filter'
    output = json.dumps({"APICall": name, "Filter": filter, "Response": resp.json()}, indent=4)

    return output


def get_threats_filter(s1client, filter):
    """
    # Get setinelone threats by filter
    """

    resp = s1client.get_threats_filter_http_request(filter)

    name = 'SentinelOne get Threats by filter'
    output = json.dumps({"APICall": name, "Filter": filter, "Response": resp.json()}, indent=4)

    return output


def update_threat(s1client, update):
    """
    # Update SentinelOne threat
    """

    resp = s1client.update_threat_http_request(update)

    name = 'SentinelOne threats updated'
    output = json.dumps({"APICall": name, "Update": update, "Response": resp.json()}, indent=4)

    return output