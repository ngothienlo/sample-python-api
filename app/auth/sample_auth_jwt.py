from datetime import datetime, timedelta
import json
import logging
import falcon
import jwt
from passlib.hash import sha256_crypt

DEFAULT_TOKEN_OPTS = {"name": "auth_token", "location": "cookie"}


class LoginResource(object):

    def __init__(
            self, get_user, secret, token_expiration_seconds, **token_opts):
        self.get_user = get_user
        self.secret = secret
        self.token_expiration_seconds = token_expiration_seconds
        self.token_opts = token_opts or DEFAULT_TOKEN_OPTS
        logging.debug(token_opts)

    def on_post(self, req, resp):
        logging.debug("Reached on_post() in Login")
        if 'email' not in req.params or 'pwd' not in req.params:
            raise falcon.HTTPUnauthorized(
                'Missing email or password, please try again',
                ['Something wrong'])
        email = req.params["email"]
        password = req.params["pwd"]
        user = self.get_user(email)
        if user and sha256_crypt.verify(password, user["password"]):
            logging.debug("Valid user, jwt'ing!")
            self.add_new_jwtoken(resp, email)
        else:
            raise falcon.HTTPUnauthorized(
                'Bad email/password combination, please try again',
                ['Something wrong'])

    # given a user identifier, this will add a new token to the response
    # Typically you would call this from within your login function, after the
    # back end has OK'd the username/password
    def add_new_jwtoken(self, resp, user_identifier=None):
        # add a JSON web token to the response headers
        if not user_identifier:
            raise Exception('Empty user_identifer passed to set JWT')
        logging.debug(
            "Creating new JWT, user_identifier is: {}".format(user_identifier))
        token = jwt.encode({'user_identifier': user_identifier,
                            'exp': datetime.utcnow() + timedelta(
                                seconds=self.token_expiration_seconds)},
                           self.secret,
                           algorithm='HS256').decode("utf-8")
        logging.debug("Setting TOKEN!")
        self.token_opts["value"] = token
        logging.debug(self.token_opts)

        # default to cookie
        if self.token_opts.get('location', 'cookie') == 'cookie':
            resp.set_cookie(**self.token_opts)
        elif self.token_opts['location'] == 'header':
            resp.body = json.dumps({
                self.token_opts['name']: self.token_opts['value']
                })
        else:
            raise falcon.HTTPInternalServerError(
                'Unrecognized jwt token location specifier')


class AuthMiddleware(object):

    def __init__(self, secret, **token_opts):
        self.secret = secret
        self.token_opts = token_opts or DEFAULT_TOKEN_OPTS

    def process_resource(self, req, resp, resource, params):
        logging.debug("Processing request in AuthMiddleware: ")
        if isinstance(resource, LoginResource):
            logging.debug("LOGIN, DON'T NEED TOKEN")
            return

        challenges = ['Token="You do not know, haha"']

        token = req.get_header('Authorization')

        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized('Auth token required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')

        if not self._token_is_valid(token):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized('Authentication required',
                                          description,
                                          challenges,
                                          href='http://docs.example.com/auth')

    def _token_is_valid(self, token):
        try:
            options = {'verify_exp': True}
            jwt.decode(
                token, self.secret,
                verify='True',
                algorithms=['HS256'],
                options=options)
            return True
        except jwt.DecodeError as err:
            logging.debug("Token validation failed Error :{}".format(str(err)))
            return False


# pylint: disable=dangerous-default-value
def get_auth_objects(
        get_user, secret, token_expiration_seconds,
        token_opts=DEFAULT_TOKEN_OPTS):
    return LoginResource(
        get_user, secret, token_expiration_seconds, **token_opts), \
        AuthMiddleware(secret, **token_opts)
