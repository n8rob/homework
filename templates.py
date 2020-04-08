import re
import random
import sys

import the_graph
authorIDs = the_graph.loadAuthorIDs()
bookIDs = the_graph.loadBookIDs()

# TODO: Add additional templates (and modify existing ones as needed)
templates = ["<<author>> wrote <<book>>",
             "<<author>> wrote <<book1>> and <<book2>>",
             "<<author>> was born in <<placeOfBirth>>",
             "<<author>> was born in <<placeOfBirth>>, which is in <<country>>",
             "<<book>> was written by <<author>>",
             "<<book>> was written by <<author1>> and <<author2>>",
             "<<author>> is an author",
             "There is a book called <<book>>",
             "Have you ever read <<book>> by <<author>>"]

def extractKeys(template):
    return re.findall(r'\<<(.*?)\>>',template)

def fill_templates(**kwargs):
    matches = []
    for t in templates:
        keys = extractKeys(t)
        if all([key in kwargs for key in keys]):
            # this template matches our kwargs, so we'll fill it in
            for key in kwargs:
                t=t.replace("<<%s>>"%key,kwargs[key])
            matches.append(t)
    return matches

def fallback_response():
    #TODO: replace fun_stuff with fallback responses that have
    # something to do with books. These could be pre-coded topic switches,
    # or they could be programmatically generated sentences based
    # on recent conversation. Your choice.
    fun_stuff = ['The unicorn is the national animal of Scotland','The Giant Pacific Octopus has 2,240 sucker cups, at least on females.','A recent U.K. study observed that small children ask their parents up to 300 questions per day, on average.','The total weight of ants on earth once equaled the total weight of people','Did you know that Pringles aren\'t actually potato chips?','During World War I, a dog named Rags saved the lives of many soldiers, and was decorated as a war hero.']#
    response = 'Sorry, I didn\'t catch that, but ' + random.choice(fun_stuff)
    return response


def response(text):
    #TODO: Extract author names and book titles from the user's utterance
    authorNames = ["Jane Austen"]
    bookTitles = ["Sense and Sensibility", "Emma", "Pride and Prejudice"]

    #TODO: Modify this code to provide an interesting
    #      conversational framework. For this assignment,
    #      you must occasionally utilize the function
    #      the_graph.birthplaceOfAuthor(), as well as
    #      additional graph functions described in the
    #      assignment spec on LearningSuite.
    authors=[]
    books=[]
    active_phrase = "that"
    if random.randint(0,1):
        if authorNames:
            author = random.choice(authorNames)
            active_phrase = author
            authors = [author]
            if author in authorIDs:
                books = the_graph.booksForAuthor(authorIDs[author])
    else:
        if bookTitles:
            book = random.choice(bookTitles)
            active_phrase = book
            books = [book]
            if book in bookIDs:
                authors = the_graph.authorsForBook(bookIDs[book])

    # choose the kwargs for our template-matching
    # algorithm
    kwargs = {}
    if authors:
        kwargs['author'] = random.choice(authors)
    if books:
        if len(books) > 1 and random.randint(0,1):
            kwargs['book1'] = random.choice(books)
            books.remove(kwargs['book1'])
            kwargs['book2'] = random.choice(books)
        else:
            kwargs['book'] = random.choice(books)
    
    # Compose the response
    response = "I don't know what to say about " + active_phrase + "."
    if kwargs:
        matches = fill_templates(**kwargs)
        if matches:
            response = random.choice(fill_templates(**kwargs))
    return response

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("input: ", sys.argv[1])
        print("response: ", response(sys.argv[1]))
    else:
        print(fill_templates(author1="Jane Austen", author2="Fred", book="Comet"))
        print(fill_templates(author="Philip K. Dick"))
        print(fill_templates(book="Mistborn", author="Brandon Sanderson"))
        print(fill_templates(author="Jane Austen", placeOfBirth="Stevenson"))
        print(fallback_response())
