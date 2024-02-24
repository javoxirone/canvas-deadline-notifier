from datetime import datetime

import requests


class CanvasAPI:
    def __init__(self, token):
        self.token = token
        self.api_root = "https://canvas.instructure.com/api/v1/"

    def request_endpoint(self, endpoint):
        return requests.get(self.api_root + endpoint, headers={'Authorization': 'Bearer ' + self.token}).json()

    def get_all_courses(self):
        return self.request_endpoint("courses")

    def get_all_assignments(self):
        assignments_data = []
        courses = self.get_all_courses()
        for course in courses:
            for assignment in self.request_endpoint("courses/" + str(course["id"]) + "/assignments/"):
                if assignment['due_at'] and datetime.strptime(assignment['due_at'],
                                                              "%Y-%m-%dT%H:%M:%SZ") > datetime.now():
                    assignments_data.append(
                        {
                            "course_name": course["name"],
                            "assignment_name": assignment["name"],
                            "assignment_due_at": datetime.strptime(assignment['due_at'], "%Y-%m-%dT%H:%M:%SZ"),
                        }
                    )
        return assignments_data

