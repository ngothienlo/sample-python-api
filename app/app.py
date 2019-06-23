import falcon
from resources.customers import CustomersCollectionResource, CustomersResource
from middleware.database import DatabaseCursor
from utils.database import database_connection
from passlib.hash import sha256_crypt
from auth import sample_auth_jwt

# User for testing
USERS = {
    "user_test@sample.test":
    {
        "email": "user_test@sample.test",
        "password": sha256_crypt.encrypt("user_test_pwd")
    }
}
COOKIE_OPTS = {"name": "my_auth_token",
               "max_age": 86400,
               "path": "/customers",
               "http_only": True}

login, auth_middleware = sample_auth_jwt.get_auth_objects(
    USERS.get,
    "UPe6Qqp8xJeRyavxup8GzMTYT6yDwYND",  # random secret
    3600,
    token_opts=COOKIE_OPTS)

app_middleware = [
    auth_middleware,
    DatabaseCursor(database_connection),
]

app = application = falcon.API(middleware=app_middleware)


# Add login resource
app.add_route('/login', login)


# Add api method
app.add_route('/customers', CustomersCollectionResource())
app.add_route('/customers/{id_:int}', CustomersResource())
