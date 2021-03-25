from rest_framework.exceptions import APIException


class AnswerRecordNotValid(APIException):
    status_code = 400
    default_detail = (
        "Post request does not contain 'question_id' or 'answer_id' or 'user_id' parts"
    )
    default_code = "answer_record_not_valid"


class UserNotValid(APIException):
    status_code = 400
    default_detail = "User sent was not a valid user"
    default_code = "user_not_valid"
