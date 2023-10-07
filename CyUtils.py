import hashlib
import json
import urllib.error
import urllib.request

import requests

USER_AGENT = "Cyberno-API-Sample-Python"


class CyUtils:
    server_address = ''

    def __init__(self, server_address):
        self.server_address = server_address

    @staticmethod
    def get_sha256(file_path):
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    @staticmethod
    def get_error(return_value):
        error = 'Error!\n'
        if "error_code" in return_value:
            error += ("Error code: %d\n" % return_value["error_code"])
        if "error_desc" in return_value:
            error += ("Error description: %s\n" % return_value["error_desc"])
        return error

    def call_with_json_input(self, api, json_input):
        try:
            if self.server_address.endswith('/') is False:
                self.server_address += "/"
            req = urllib.request.Request(self.server_address + api)
            req.add_header("Content-type", "application/json")
            req.add_header("User-Agent", USER_AGENT)
            json_data_as_bytes = json.dumps(json_input).encode('utf-8')
            req.add_header('Content-Length', len(json_data_as_bytes))
            response = urllib.request.urlopen(req, json_data_as_bytes)
            data = response.read()
            values = json.loads(data)
            return values
        except urllib.error.HTTPError as e:
            try:
                data = e.read()
                values = json.loads(data)
                return values
            except:
                return {"success": False, "error_code": 900}
        except:
            return {"success": False, "error_code": 900}

    def call_with_form_input(self, api, data_input, file_param_name, file_path):
        try:
            with open(file_path, 'rb') as file_handle:
                files = [(file_param_name, ("file_to_upload", file_handle, "application/octet-stream"))]
                response = requests.post(self.server_address + "/" + api,
                                         files=files,
                                         data=data_input)
                values = response.json()
                return values
        except:
            return {"success": False, "error_code": 900}
