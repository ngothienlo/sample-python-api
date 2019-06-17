# config
DB_NAME = 'assignment_api'
DB_USER = 'assign_user'
DB_PWD = 'assign_123'
DB_HOST = 'localhost'

DATABASE_URL = 'postgresql+psycopg2://%s:%s@%s/%s' % (
    DB_USER, DB_PWD, DB_HOST, DB_NAME)
print('=================> DATABASE_URL: ', DATABASE_URL)

PAGE_SIZE = 10
