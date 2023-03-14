import logging
from django.db import connection, DatabaseError
from rest_framework.exceptions import ValidationError

from api.models import Port, Region

logger = logging.getLogger(__name__)


class PortManager:

    def validate_provided_code(self, provided_code):
        port_filter_params = Port.objects.filter(code=provided_code)
        region_filter_params = Region.objects.filter(slug=provided_code)
        if port_filter_params.exists():
            return 'port'
        if region_filter_params.exists():
            return 'region'

        raise ValidationError("Provided code doesn't exists")

    def get_port_list(self, provided_code, code_type):
        if code_type == 'port':
            return list(Port.objects.values_list('code').get(code=provided_code))

        if code_type == 'region':
            return self.get_port_from_region(provided_code)

    def get_port_from_region(self, region_slug):
        region_recursive_query = """
            SELECT code from ports where parent_slug in (
                WITH RECURSIVE rate_table_cte AS
                (
                    SELECT slug, parent_slug
                    FROM regions
                    WHERE slug=%s
                    UNION
                    SELECT r.slug, r.parent_slug
                    from regions as r
                    INNER JOIN rate_table_cte as rtc on r.parent_slug = rtc.slug
                ) 
                SELECT slug FROM rate_table_cte
            )
            """
        with connection.cursor() as cursor:
            cursor.execute(region_recursive_query, [region_slug])
            return [current_code[0] for current_code in cursor.fetchall()]

