from django.db import connection

from utils.managers.base_manager import BasePRManager


class RegionManager(BasePRManager):

    def get_port_list_by_code(self, region_slug):
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