from django.db import connection

from utils.managers.base_manager import BasePRManager


class RegionManager(BasePRManager):

    def __get_port_from_region_query(self):

        return """
            SELECT code FROM ports 
            WHERE parent_slug IN
             (
                WITH RECURSIVE temporary_rate_table AS
                (
                    SELECT slug, parent_slug
                    FROM regions
                    WHERE slug=%(slug)s
                    UNION
                    SELECT r.slug, r.parent_slug
                    FROM regions AS r
                    INNER JOIN temporary_rate_table AS rtc ON r.parent_slug = rtc.slug
                ) 
                SELECT slug FROM temporary_rate_table
            )
            """

    def get_port_list_by_code(self, region_slug):
        region_recursive_query = self.__get_port_from_region_query()
        with connection.cursor() as cursor:
            cursor.execute(region_recursive_query, {
                'slug': region_slug
            })
            return [current_code[0] for current_code in cursor.fetchall()]