import logging

from datetime import datetime

from rest_framework.exceptions import ValidationError


logger = logging.getLogger(__name__)


def parse_date(provided_date):
    try:
        return datetime.strptime(provided_date, "%Y-%m-%d")
    except Exception as E:
        logger.error(str(E), exc_info=True)
        raise ValidationError("Date not in valid format")
