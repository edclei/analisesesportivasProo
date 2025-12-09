# minimal psycopg2 shim for tests

def connect(*args, **kwargs):
    class DummyConn:
        def cursor(self):
            class DummyCur:
                def execute(self, *a, **k):
                    pass
                def fetchone(self):
                    return None
                def fetchall(self):
                    return []
                def close(self):
                    pass
            return DummyCur()
        def close(self):
            pass
    return DummyConn()
