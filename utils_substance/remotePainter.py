import bpy
import sys
import json
import base64
import subprocess
import time

# --- Error Classes (already moved to top from previous fix) ---
class PainterError(Exception):
    def __init__(self, message):
        super(PainterError, self).__init__(message)

class ExecuteScriptError(PainterError):
    def __init__(self, data):
        super(ExecuteScriptError, self).__init__('An error occured when executing script: {0}'.format(data))
# --- End Error Classes ---

if sys.version_info >= (3, 0):
    import http.client as http
else:
    import httplib as http

class RemotePainter() :
    def __init__(self, port=60041, host='localhost'):
        self._host = host
        self._port = port
        self._PAINTER_ROUTE = '/run.json'
        self._HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}

    def _jsonPostRequest( self, route, body, type ) :
        connection = http.HTTPConnection(self._host, self._port, timeout=3600)
        connection.request('POST', route, body, self._HEADERS)
        response = connection.getresponse()

        raw_data = response.read()
        connection.close()

        decoded_response_str = raw_data.decode('utf-8', errors='ignore').strip()

        parsed_json_data = None
        try:
            parsed_json_data = json.loads(decoded_response_str)
        except json.JSONDecodeError:
            pass # Not a JSON response

        if isinstance(parsed_json_data, dict) and 'error' in parsed_json_data:
            try:
                body_json = json.loads(body.decode('utf-8'))
                script_b64 = body_json.get("python", body_json.get("js", ""))
                decoded_script = base64.b64decode(script_b64).decode('utf-8', errors='ignore')
                print("\n--- Error from Painter's Script Execution ---")
                print("Original script sent:")
                print(decoded_script)
                print(f"Error message from Painter: {parsed_json_data['error']}\n")
            except Exception as e_debug:
                print(f"Failed to decode original script for error context: {e_debug}")
                print(f"Raw error from Painter: {parsed_json_data['error']}")
            
            raise ExecuteScriptError(parsed_json_data['error'])
        else :
            if type == "js":
                return parsed_json_data
            return decoded_response_str

    def checkConnection(self):
        connection = http.HTTPConnection(self._host, self._port)
        connection.connect()

    def execScript( self, script, type ) :
        encoded_script_base64_bytes = base64.b64encode( script.encode('utf-8') )
        encoded_script_base64_str = encoded_script_base64_bytes.decode('utf-8')

        payload_dict = {}
        if type == "js" :
            payload_dict["js"] = encoded_script_base64_str
        else :
            payload_dict["python"] = encoded_script_base64_str

        json_payload_str = json.dumps(payload_dict)
        final_request_body_bytes = json_payload_str.encode( "utf-8" )

        return self._jsonPostRequest( self._PAINTER_ROUTE, final_request_body_bytes, type )