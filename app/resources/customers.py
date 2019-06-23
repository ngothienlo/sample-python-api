import falcon
import traceback
from webargs import fields
from webargs.falconparser import use_args
import json
from datetime import datetime


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

# for args input
create_customer_args = {
    'name': fields.String(location='json', required=True),
    'dob': fields.Date(location='json', required=True),
}

update_customer_args = {
    'name': fields.String(location='json'),
    'dob': fields.Date(location='json'),
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
    WHERE           id=%(id)s;"""

GET_COLLECTION_QUERY = """
    SELECT  id, name, dob::VARCHAR, updated_at::VARCHAR
    FROM    customer;"""

GET_COLLECTION_PAGINATION_QUERY = """
    SELECT  *
    FROM    customer
    WHERE   id > %(last_id)s
    LIMIT   %(page_size)s;"""

GET_CUSTOMER_QUERY = """
    SELECT  id, name, dob::VARCHAR, updated_at::VARCHAR
    FROM    customer
    WHERE   id=%(id)s;"""

INSERT_CUSTOMER_QUERY = """
    INSERT INTO     customer(name, dob)
    VALUES           (%(name)s, %(dob)s)
    RETURNING id;"""

UPDATE_CUSTOMER_QUERY = """
    UPDATE  customer
    SET """


def get_only_result(conn, query, params):
    """
    Given conn, query, and params, return customer
    """
    rs = conn.execute(query, [params])

    def dictfetchone(ResultProxy_):
        result = ResultProxy_.fetchone()
        if result:
            dict_rs = dict(zip(ResultProxy_.keys(), result))
            return dict_rs
        else:
            return {}

    return dictfetchone(rs)


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
            'error': 'None',
        }
        resp.body = json.dumps(results)

    @use_args(update_customer_args)
    def on_put(self, req, resp, args, id_):
        sql = UPDATE_CUSTOMER_QUERY
        # check to see if exists
        customers = get_only_result(
            req.conn, GET_CUSTOMER_QUERY, {'id': id_})

        if not customers:
            raise falcon.HTTPNotFound()

        data = {
            'id': id_,
        }

        if 'name' in args or 'name' in req.params:
            data['name'] = args.get('name') and args.get(
                'name') or req.params.get('name')
            sql += "name=%(name)s"
        if 'dob' in args or 'dob' in req.params:
            data['dob'] = args.get('dob') and args.get(
                'dob') or req.params.get('dob')
            sql = sql + (', ' if (
                'name' in args or 'name' in req.params) else ''
                ) + "dob=%(dob)s"
        if sql != UPDATE_CUSTOMER_QUERY:
            sql += ', updated_at=NOW()'
            req.conn.execute(sql, data)
            resp.status = falcon.HTTP_OK
            data['updated_at'] = str(datetime.now())
            resp.body = json.dumps(data)
        else:
            results = {
                'Warning': "Don't you change anything ?",
            }
            resp.body = json.dumps(results)

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

        cursor = req.conn.execute(sql_query, data)

        def dictfetchall(ResultProxy_):
            dict_rs = ResultProxy_.fetchall()
            keys = ResultProxy_.keys()
            rs_formated = []
            for line in dict_rs:
                line = dict(zip(keys, line))
                rs_formated.append(line)
            return rs_formated

        customers = dictfetchall(cursor)
        if not customers:
            raise falcon.HTTPNotFound()

        resp.status = falcon.HTTP_OK

        results = {
            'data': customers,
            'last_id': customers[-1]['id'],
            'error': '',
        }

        resp.body = json.dumps(results)

    def on_post(self, req, resp):
        if 'name' not in req.params or 'dob' not in req.params:
            raise falcon.HTTPBadRequest(
                'You must fill both name and dob for create new cus',
                traceback.format_exc())
        data = {
            'name': req.params['name'],
            'dob': req.params['dob'],
        }
        cursor = req.conn.execute(INSERT_CUSTOMER_QUERY, data)

        customers_id = cursor.fetchone()[0]
        resp.location = '/customers/' + str(customers_id)
        resp.status = falcon.HTTP_CREATED
        resp.body = json.dumps({'new_id': str(customers_id)})


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
