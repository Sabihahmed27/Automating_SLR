from django.core.exceptions import ValidationError


def validate_file(value):
    value= str(value)
    if value.endswith(".pdf") != True:
        print("Cheetos")
        raise ValidationError("Only PDF and Word Documents can be uploaded")
    else:
        print("correct!!")
        return value
