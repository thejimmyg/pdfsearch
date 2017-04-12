from whoosh.index import open_dir
from whoosh.qparser import QueryParser

ix = open_dir("build/search_index")

def search(authority, q):
    r = []
    hits = 0
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(q)
        results = searcher.search(query)
        if results:
            hits = results.estimated_length
            r = [hit.fields() for hit in results]
    return hits, r

if __name__ == '__main__':
    import sys
    count, results = search(sys.argv[1], sys.argv[2])
    print(count, results)
