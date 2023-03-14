import logging

from datetime import datetime

from rest_framework.exceptions import ValidationError


logger = logging.getLogger(__name__)


def validate_date_params(date_from, date_to):
    if not date_from:
        raise ValidationError("Date from parameter is not provided")
    if not date_to:
        raise ValidationError("Date to parameter is not provided")

    parsed_date_from = parse_date(date_from)
    parsed_date_to = parse_date(date_to)

    if parsed_date_from > parsed_date_to:
        raise ValidationError("Date from can not be bigger then Date to")

    return parsed_date_from, parsed_date_to

def parse_date(provided_date):
    try:
        return datetime.strptime(provided_date, "%Y-%m-%d")
    except Exception as E:
        logger.error(str(E), exc_info=True)
        raise ValidationError("Date not in valid format")
