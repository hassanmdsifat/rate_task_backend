import logging

from datetime import datetime

from rest_framework.exceptions import ValidationError


logger = logging.getLogger(__name__)


def parse_date_from_string(provided_date):
    try:
        return datetime.strptime(provided_date, "%Y-%m-%d")
    except Exception as E:
        logger.error(str(E), exc_info=True)
        raise ValidationError("Date not in valid format")


def parse_date_from_datetime(provided_date):
    try:
        return datetime.strftime(provided_date, "%Y-%m-%d")
    except Exception as E:
        logger.error(str(E), exc_info=True)
        return provided_date


