from whoosh.fields import *

schema = Schema(
    authority=TEXT(stored=True),
    name=TEXT(stored=True),
    page_number=NUMERIC(stored=True),
    uid=ID(stored=True),
    content=TEXT
)
