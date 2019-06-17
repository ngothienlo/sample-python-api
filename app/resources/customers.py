import falcon
from webargs import fields
from webargs.falconparser import use_args

from app.config import PAGE_SIZE

# Done
# Create
#   * collection
#       * only updates 1
#       * also has bulk endpoints
# Read
#   * collection: 200;
#       * Pagination should be set up via page and implemented with index and
#         offset behind the scenes
#   * customer: 200 or 404
# Update
#   * collection: PUT and PATCH not allowed
#   * customer: PUT allowed, PATCH not allowed. what if customer
# Delete
#   * collection: DELETE not allowed
#   * customer: delete customer, return something in response body or 404

create_customer_args = {
    'name': fields.String(location='json', required=True),
    'dob': fields.Date(location='json', required=True),
}

bulk_create_customer_args = {
    'data': fields.List(fields.Nested(create_customer_args), required=True)
}

pagination_args = {
    'last_id': fields.Int(location='query')
}

# queries
DELETE_CUSTOMER_QUERY = """
    DELETE FROM     customers
    WHERE           id=%(id)s"""

GET_COLLECTION_QUERY = """
    SELECT  *
    FROM    customers
    LIMIT   %(page_size)s;"""

GET_COLLECTION_PAGINATION_QUERY = """
    SELECT  *
    FROM    customers
    WHERE   id > %(last_id)s
    LIMIT   %(page_size)s;"""

GET_CUSTOMER_QUERY = """
    SELECT  *
    FROM    customers
    WHERE   id=%(id)s;"""

INSERT_CUSTOMER_QUERY = """
    INSERT INTO     customers(name, dob)
    VALUE           (%(name)s, %(dob)s)"""

UPDATE_CUSTOMER_QUERY = """
    UPDATE  customers
    SET     name=%(name)s,
            dob=%(dob)s
    WHERE   id=%(id)s;"""


def get_only_result(cursor, query, params):
    """
    Given cursor, query, and params, return customer
    """
    cursor.execute(query, params)
    return cursor.fetchone()


class CustomersResource:
    """
    Single resource
    """

    def on_get(self, req, resp, id_):
        customers = get_only_result(
            req.cursor, GET_CUSTOMER_QUERY, {'id': id_})

        if not customers:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK

        results = {
            'data': customers,
            'error': '',
        }
        resp.media = results

    @use_args(create_customer_args)
    def on_put(self, req, resp, args, id_):
        # check to see if exists
        customers = get_only_result(
            req.cursor, GET_CUSTOMER_QUERY, {'id': id_})

        if not customers:
            raise falcon.HTTPNotFound()

        data = {
            'id': id_,
            'name': args['name'],
            'dob': args['dob'],
        }

        req.cursor.execute(UPDATE_CUSTOMER_QUERY, data)
        resp.status = falcon.HTTP_OK

    def on_delete(self, req, resp, id_):
        # check to see if exists
        customers = get_only_result(
            req.cursor, GET_CUSTOMER_QUERY, {'id': id_})

        if not customers:
            raise falcon.HTTPNotFound()

        req.cursor.execute(DELETE_CUSTOMER_QUERY, {'id': id_})
        resp.status = falcon.HTTP_NO_CONTENT


class CustomersCollectionResource:
    """
    Customer collection
    """

    @use_args(pagination_args)
    def on_get(self, req, resp, args):
        data = {}
        data['page_size'] = PAGE_SIZE

        if 'last_id' in args:
            data['last_id'] = args['last_id']
            sql_query = GET_COLLECTION_PAGINATION_QUERY
        else:
            sql_query = GET_COLLECTION_QUERY

        req.cursor.execute(sql_query, data)
        customers = req.cursor.fetchall()

        if not customers:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK

        results = {
            'data': customers,
            'last_id': customers[-1]['id'],
            'error': '',
        }

        resp.media = results

    @use_args(create_customer_args)
    def on_post(self, req, resp, args):
        data = {
            'name': args['name'],
            'dob': args['dob'],
        }

        req.cursor.execute(INSERT_CUSTOMER_QUERY, data)

        customers_id = req.cursor.lastrowid
        resp.location = '/customers/' + str(customers_id)
        resp.status = falcon.HTTP_CREATED


class CustomersBulkAddResource:
    """
    Customers Bulk Add Resource
    """

    @use_args(bulk_create_customer_args)
    def on_post(self, req, resp, args):
        customers = args['data']

        req.cursor.executemany(INSERT_CUSTOMER_QUERY, customers)

        customers_id = req.cursor.lastrowid
        resp.location = '/customers/' + str(customers_id)
        resp.status = falcon.HTTP_CREATED
