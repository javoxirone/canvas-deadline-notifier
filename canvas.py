import requests
import datetime as header_datetime
from datetime import datetime, timedelta
from typing import List, Dict, TypedDict


class AssignmentInfo(TypedDict):
    course_name: str
    assignment_name: str
    assignment_due_at: datetime

class CanvasAPI:
    
    def __init__(self, token):
        self.token: str = token
        self.api_root: str = "https://canvas.instructure.com/api/v1/"


    def request_endpoint(self, endpoint:str, params:dict|None=None) -> List[Dict]:
        """ 
        This method sends request to canvas API with authorization token and with optional paramateres, and then returns serialized response.

        :param endpoint: Route to certain endpoint.
        :param params: (optional) Additional parameters for GET request.
        :return: JSON encoded Response object (List of dictionaries).
        """
        response = requests.get(self.api_root + endpoint, headers={'Authorization': 'Bearer ' + self.token},
                            params=params)
        
        response.raise_for_status()

        json_response = response.json()

        return json_response
    

    def get_all_courses(self) -> List[Dict]:
        courses = self.request_endpoint("courses")
        return courses

    def get_all_assignments_of_single_course(self, course_id: int) -> List[Dict]:
        """
        This method returns list of all assignments of one course by getting course_id as an argument.

        :param course_id: Unique ID of the course.
        :return: List of dictionaries with all assignment information.
        """

        assignments = self.request_endpoint("courses/" + str(course_id) + "/assignments/", {'bucket': 'unsubmitted', 'enrollment_state': 'active'})

        return assignments

    def get_all_assignments(self) -> List[AssignmentInfo]:
        """ 
        This method retrieves all active assignments from all courses and returns a list of AssignmentInfo objects.
        
        :return: A list of assignments with required fields extracted from each active assignment.
        """
        assignment_list_with_required_fields = []
        
        course_list = self.get_all_courses()

        for course in course_list:

            assignment_list = self.get_all_assignments_of_single_course(course['id'])

            for assignment in assignment_list:

                if self.is_active_assignment(assignment):

                    assignment_list_with_required_fields.append(self.extract_required_fields_from_assignment(course['name'], assignment))

        return assignment_list_with_required_fields
    

    def format_deadline(self, datetime: str) -> datetime:
        """
        This method converts datetime to "%Y-%m-%dT%H:%M:%SZ" format.

        :param datetime: datetime in string format.
        :return: datetime object.
        """

        return header_datetime.datetime.strptime(datetime, "%Y-%m-%dT%H:%M:%SZ")
    

    def convert_timezone_to_utc5(self, datetime: datetime) -> datetime:
        """
        This method corrects timezone by 5 hours (UTC+5).

        :param datetime: datetime object.
        :return: +5 hours datetime object.
        """

        return datetime + timedelta(hours=5)
    
    def handle_assignment_deadline(self, datetime:str) -> datetime:
        """
        This method handles deadline field by converting it to datetime format and by changing timezone by 5 hours.

        :param datetime: datetime string.
        :return: datetime that is converted to object and added 5 hours.
        """
        final_datetime = self.convert_timezone_to_utc5(self.format_deadline(datetime))
        return final_datetime

    def extract_required_fields_from_assignment(self, course_name: str, assignment_data: Dict) -> AssignmentInfo:
        """
        This method gets only important fields from given data and returns it.

        :param course_name: The name of the course.
        :param assignment_data: Assignment dictionary with all fields.
        :return: Assignment dictionary with all important fields for user.
        """

        context = {
                "course_name": course_name,
                "assignment_name": assignment_data["name"],
                "assignment_due_at": self.handle_assignment_deadline(assignment_data["due_at"]),
        }

        return context
    
    def is_active_assignment(self, assignment:Dict) -> bool:
        """
        This method checks if assignment's deadline passed or not, and returns boolean condition based on that.

        :param assignment: Assignment dictionary with all fields.
        :return: Condition checked on appearance of deadline and is deadline ahead or passed.
        """

        is_active = assignment['due_at'] and self.format_deadline(assignment['due_at']) > datetime.now()

        return is_active
