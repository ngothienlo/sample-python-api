import falcon
from webargs import fields
from webargs.falconparser import use_args
import json


PAGE_SIZE = 10

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
    DELETE FROM     customer
    WHERE           id=%(id)s"""

GET_COLLECTION_QUERY = """
    SELECT  *
    FROM    customer
    LIMIT   %(page_size)s;"""

GET_COLLECTION_PAGINATION_QUERY = """
    SELECT  *
    FROM    customer
    WHERE   id > %(last_id)s
    LIMIT   %(page_size)s;"""

GET_CUSTOMER_QUERY = """
    SELECT  *
    FROM    customer
    WHERE   id=%(id)s;"""

INSERT_CUSTOMER_QUERY = """
    INSERT INTO     customer(name, dob)
    VALUE           (%(name)s, %(dob)s)"""

UPDATE_CUSTOMER_QUERY = """
    UPDATE  customer
    SET     name=%(name)s,
            dob=%(dob)s
    WHERE   id=%(id)s;"""


def get_only_result(conn, query, params):
    """
    Given conn, query, and params, return customer
    """
    rs = conn.execute(query, [params])

    def dictfetchall(ResultProxy_):
        dict_rs = dict(zip(ResultProxy_.keys(), ResultProxy_.fetchone()))
        dict_rs['dob'] = dict_rs['dob'].strftime("%Y-%m-%d")
        return dict_rs

    return dictfetchall(rs)


class CustomersResource:
    """
    Single resource
    """

    def on_get(self, req, resp, id_):
        customers = get_only_result(
            req.conn, GET_CUSTOMER_QUERY, {'id': id_})

        if not customers:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK

        results = {
            'data': customers,
            'error': '',
        }
        resp.body = json.dumps(results)

    @use_args(create_customer_args)
    def on_put(self, req, resp, args, id_):
        # check to see if exists
        customers = get_only_result(
            req.conn, GET_CUSTOMER_QUERY, {'id': id_})

        if not customers:
            raise falcon.HTTPNotFound()

        data = {
            'id': id_,
            'name': args['name'],
            'dob': args['dob'],
        }

        req.conn.execute(UPDATE_CUSTOMER_QUERY, data)
        resp.status = falcon.HTTP_OK

    def on_delete(self, req, resp, id_):
        # check to see if exists
        customers = get_only_result(
            req.conn, GET_CUSTOMER_QUERY, {'id': id_})

        if not customers:
            raise falcon.HTTPNotFound()

        req.conn.execute(DELETE_CUSTOMER_QUERY, {'id': id_})
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

        req.conn.execute(sql_query, data)
        customers = req.conn.fetchall()

        if not customers:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK

        results = {
            'data': customers,
            'last_id': customers[-1]['id'],
            'error': '',
        }

        resp.body = json.dumps(results)

    @use_args(create_customer_args)
    def on_post(self, req, resp, args):
        data = {
            'name': args['name'],
            'dob': args['dob'],
        }

        req.conn.execute(INSERT_CUSTOMER_QUERY, data)

        customers_id = req.conn.lastrowid
        resp.location = '/customers/' + str(customers_id)
        resp.status = falcon.HTTP_CREATED


class CustomersBulkAddResource:
    """
    Customers Bulk Add Resource
    """

    @use_args(bulk_create_customer_args)
    def on_post(self, req, resp, args):
        customers = args['data']

        req.conn.executemany(INSERT_CUSTOMER_QUERY, customers)

        customers_id = req.conn.lastrowid
        resp.location = '/customers/' + str(customers_id)
        resp.status = falcon.HTTP_CREATED
