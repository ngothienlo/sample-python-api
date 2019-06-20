import falcon
from resources.customers import \
    CustomersCollectionResource, CustomersResource, CustomersBulkAddResource
from middleware.database import DatabaseCursor
from utils.database import database_connection

app_middleware = [
    DatabaseCursor(database_connection),
]
app = application = falcon.API(middleware=app_middleware)


app.add_route('/customers', CustomersCollectionResource())
app.add_route('/customers/{id_:int}', CustomersResource())
app.add_route('/movies/bulk', CustomersBulkAddResource())
