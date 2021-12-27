"""Logic that handles the comunication with the DB
"""
from fastapi.templating import Jinja2Templates
from app.models import engine, TABLE_NAME

templates = Jinja2Templates(directory="templates")

class Sql_conn:
    def _parse(self, query_dict: dict[str]):
        """Parse the elements and renders the query

        Args:
            query_dict (dict): dictionary with the elements

        Returns:
            str: Rendered query
        """
        query_dict['table'] = TABLE_NAME
        render = templates.TemplateResponse(
            "query_template.j2", {'request':None, 'data': query_dict}
        )
        return render.body.decode('ascii')

    def _query(self, q):
        print(q)
        with engine.connect() as con:
            rs = con.execute(q)
        return rs.fetchall()

    def request_query(self, query_dict: dict[str]):
        q = self._parse(query_dict)
        data = self._query(q)
        return data
