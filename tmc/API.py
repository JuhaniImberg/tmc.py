import requests
import tmc


class API:

    """Handles communication with TMC server."""

    def __init__(self):
        self.server_url = ""
        self.auth_header = ""
        self.configured = False
        self.api_version = 7

        self.db_configure()

    def db_configure(self):
        try:
            url = tmc.db.config_get("url")
            token = tmc.db.config_get("token")
            self.configure(url, token)
        except Exception as e:
            pass

    def configure(self, url, token):
        self.server_url = url
        self.auth_header = {
            "Authorization": "Basic {0}".format(token)}
        self.configured = True

        self.make_request("courses.json")

        tmc.db.config_set("url", url)
        tmc.db.config_set("token", token)

    def make_request(self, slug):
        if not self.configured:
            raise Exception("API needs to be configured before use!")
        req = requests.get("{0}{1}".format(self.server_url, slug),
                           headers=self.auth_header,
                           params={"api_version": self.api_version})
        if req is None:
            raise Exception("Request is none!")
        json = None
        try:
            json = req.json()
        except ValueError as e:
            if "500" in request.text:
                raise Exception("TMC Server encountered a internal error.")
            else:
                raise Exception("TMC Server did not send valid JSON.")
        if "error" in json:
            raise Exception(json["error"])
        return json

    def get_courses(self):
        return self.make_request("courses.json")["courses"]

    def get_exercises(self, id):
        return self.make_request("courses/{0}.json".format(id))["course"]["exercises"]

    def get_exercise(self, id):
        return self.make_request("exercises/{0}.json".format(id))

    def get_submission(self, id):
        return self.make_request("submissions/{0}.json".format(id))
