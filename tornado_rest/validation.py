import errors
import schematics.exceptions


def validate(data, validate_class):
    validate_data = validate_class(data)
    try:
        validate_data.validate()
    except schematics.exceptions.ValidationError as e:
        raise errors.ValidationError(400, error_messages=e.messages)

    return validate_data
