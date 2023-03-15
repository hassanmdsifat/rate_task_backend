from rest_framework.exceptions import ValidationError

from api.models import Port, Region
from utils.helpers.date_time_helpers import parse_date


class ValidatorManager:

    def validate_date_params(self, date_from, date_to):
        if not date_from:
            raise ValidationError("Date from parameter is not provided")
        if not date_to:
            raise ValidationError("Date to parameter is not provided")

        parsed_date_from = parse_date(date_from)
        parsed_date_to = parse_date(date_to)

        if parsed_date_from > parsed_date_to:
            raise ValidationError("Date from can not be bigger then Date to")

        return parsed_date_from, parsed_date_to

    def validate_provided_code(self, provided_code):
        port_filter_params = Port.objects.filter(code=provided_code)
        region_filter_params = Region.objects.filter(slug=provided_code)
        if port_filter_params.exists():
            return 'port'
        if region_filter_params.exists():
            return 'region'

        raise ValidationError("Provided code doesn't exists")