class DatabaseCursor(object):

    def __init__(self, db_conn):
        self.db_conn = db_conn

    def process_request(self, req, resp):

        if req is not None:
            req.conn = self.db_conn()

    def process_response(self, req, resp, resource, req_succeeded):
        # import pdb;pdb.set_trace()
        if hasattr(req, 'conn'):
            req.conn.close()
