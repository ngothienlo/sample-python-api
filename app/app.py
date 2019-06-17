import falcon
# from sqlalchemy import create_engine
# from falcon_autocrud.middleware import Middleware
# from resources import CustomerCollectionResource, CustomerResource
from .resources.customers import (
    CustomersCollectionResource, CustomersResource, CustomersBulkAddResource)
from .middleware.database import DatabaseCursor
from .utils.database import database_connection

# old_func = Middleware.process_response


# NOTE: fix `process_response` functin on library
# def process_response(self, req, resp, resource, req_succeeded):
#     old_func(self, req, resp, resource)


# Middleware.process_response = process_response

app_middleware = [
    DatabaseCursor(database_connection),
]
app = application = falcon.API(middleware=app_middleware)

# db_engine = create_engine(
#     'postgresql+psycopg2://assign_user:assign_123@localhost/assignment_api')
# app = application = falcon.API(middleware=[Middleware()])


app.add_route('/customers', CustomersCollectionResource())
app.add_route('/customers/{id}', CustomersResource())
app.add_route('/movies/bulk', CustomersBulkAddResource())