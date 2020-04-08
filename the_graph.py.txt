from qwikidata.sparql import (get_subclasses_of_item,
                              return_sparql_query_results)
from qwikidata.linked_data_interface import get_entity_dict_from_api

def extractAuthorIDs(numQueries=1000):
    sparql_query = """
       SELECT DISTINCT ?author ?authorLabel WHERE {
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
          ?book wdt:P50 ?author.
          { ?author wdt:P106 wd:Q36180 } UNION {?author wdt:P106 wd:Q482980} UNION {?author wdt:P106 wd:Q6625963} .
       }
       LIMIT %d
    """ % numQueries
    res = return_sparql_query_results(sparql_query)
    authorIDs = {}
    for result in res['results']['bindings']:
        authorName = result['authorLabel']['value']
        authorID = result['author']['value'][result['author']['value'].find('Q'):]
        authorIDs[authorName] = authorID
    return authorIDs

def cacheAuthorIDs(numQueries=1000):
    authorIDs = extractAuthorIDs(numQueries)
    #print(authorIDs)
    with open('cached_author_IDs.txt', 'w') as f:
       for author in authorIDs.keys():
           f.write(author + '\t' + authorIDs[author] + '\n')
    f.close()
    return authorIDs

def loadAuthorIDs():
    authorIDs = {}
    with open('cached_author_IDs.txt', 'r') as f:
        for line in f.readlines():
            values = line.split('\t')
            authorIDs[values[0]] = values[1].strip()
    return authorIDs

def extractBookIDs(numQueries=1000):
    sparql_query = """
       SELECT DISTINCT ?book ?bookLabel WHERE {
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
          ?book wdt:P50 ?author.
          { ?author wdt:P106 wd:Q36180 } UNION {?author wdt:P106 wd:Q482980} UNION {?author wdt:P106 wd:Q6625963} .
       }
       LIMIT %d
    """ % numQueries
    res = return_sparql_query_results(sparql_query)
    bookIDs = {}
    for result in res['results']['bindings']:
        bookTitle = result['bookLabel']['value']
        bookID = result['book']['value'][result['book']['value'].find('Q'):]
        if bookTitle[0] != 'Q':
            bookIDs[bookTitle] = bookID
    return bookIDs

def cacheBookIDs(numQueries=1000):
    bookIDs = extractBookIDs(numQueries)
    #print(bookIDs)
    with open('cached_book_IDs.txt', 'w') as f:
       for book in bookIDs.keys():
           f.write(book + '\t' + bookIDs[book] + '\n')
    f.close()
    return bookIDs

def loadBookIDs():
    bookIDs = {}
    with open('cached_book_IDs.txt', 'r') as f:
        for line in f.readlines():
            values = line.split('\t')
            bookIDs[values[0]] = values[1].strip()
    return bookIDs


def booksAndAuthors(numQueries=1000):
    sparql_query = """
       SELECT ?authorLabel ?bookLabel WHERE {
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
          ?author wdt:P106/wdt:P279 wd:Q36180.
          ?book wdt:P50 ?author.
       }
       LIMIT %d
    """ % numQueries
    res = return_sparql_query_results(sparql_query)
    #for result in res['results']['bindings']:
    #    print(result['authorLabel']['value'], result ['bookLabel']['value'])
    return [(result['authorLabel']['value'], 
              result['bookLabel']['value'])
              for result in res['results']['bindings']]

def booksForAuthor(authorID):
    sparql_query = """
       SELECT ?bookLabel WHERE {
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
          ?book wdt:P50 wd:%s .
       }
       LIMIT 1000
    """ % authorID
    #print(sparql_query)
    res = return_sparql_query_results(sparql_query)
    return [result['bookLabel']['value'] 
              for result in res['results']['bindings']]

def authorsForBook(bookID):
    sparql_query = """
       SELECT ?authorLabel WHERE {
          SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
          wd:%s wdt:P50 ?author .
       }
       LIMIT 1000
    """ % bookID
    #print(sparql_query)
    res = return_sparql_query_results(sparql_query)
    return [result['authorLabel']['value'] 
        for result in res['results']['bindings']]
    return res

def birthplaceOfAuthor(authorID):
    #TODO: Create and execute a SPARQL query that returns
    #      the place of birth for the author with authorID.
    #      The query should include an optional argument
    #      that will return the country in which ?placeOfBirth
    #      is located, if such a relationship exists.

    #      You can generate simple queries using the query
    #      helper at https://query.wikidata.org. (click the
    #      round blue info icon to get started.) You can learn 
    #      about the OPTIONAL keyword at:
    #      https://medium.com/freely-sharing-the-sum-of-all-knowledge/writing-a-wikidata-query-discovering-women-writers-from-north-africa-d020634f0f6c
    return [('Unknown city', 'Unknown country')]


if __name__ == "__main__":
    #print(booksAndAuthors(100))

    #authorIDs = cacheAuthorIDs(10000)
    authorIDs = loadAuthorIDs()
    #print(authorIDs)
    print(booksForAuthor(authorIDs['Brandon Sanderson']))

    #bookIDs = cacheBookIDs(10000)
    bookIDs = loadBookIDs()
    #print(bookIDs)
    print(authorsForBook(bookIDs['Comet']))

    print(birthplaceOfAuthor(authorIDs['Jane Austen']))
