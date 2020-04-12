import re
import random
import sys
import pdb

import the_graph
authorIDs = the_graph.loadAuthorIDs()
bookIDs = the_graph.loadBookIDs()

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

intents = ["books_from_author","author_of_book","about_author","about_book","like_author","ever_read_book","birthplace","multiple"]

# Add additional templates (and modify existing ones as needed)
templates = ["<<author>> wrote <<book>>",
             "<<author>> wrote <<book1>> and <<book2>>",
             "Two really awesome books by <<author>> are <<book1>> and <<book2>>",
             "<<author>> fares from the land of <<placeOfBirth>>",
             "<<author>> was born in <<placeOfBirth>>",
             "<<book>> was written by <<author>>",
             "<<book>> was written by <<author1>> and <<author2>>",
             "<<book>> had more than one author; <<author1>> and <<author2>> were among the writers",
             "<<author>> is an author",
             "There is a book called <<book>>",
             "Ah, <<book>>. A truly wonderful story",
             "Ah, <<book>>. One of <<author>>'s finest",
             "Ah, <<book>>. One of <<author1>>'s and <<author2>>'s finest",
             "Have you ever read <<book>> by <<author>>",
             "Oh I also love <<author>>",
             "Really! I like <<author>> too",
             "<<author>> does write so wonderfully",
             "I have not. How is it?",
             "Yes, <<book>> is one of my favorite books",
             "<<author>> was born in <<dateOfBirth>>",
             "<<dateOfBirth>> was a marvelous year, the year <<author>> was born, in fact",
             "<<author>> died in <<dateOfDeath>>",
             "<<dateOfDeath>>. What a tragic year. The year <<author>> died",
             "<<book>> was published in <<publishDate>>",
             "<<book>> was published in <<publishDate>>. True story"
             ]

templates_dict = {
        "books_from_author":templates[:3]+templates[5:7]+[templates[13]],
        "author_of_book":templates[:2]+templates[5:8]+templates[11:13],
        "about_author":templates[:8]+[templates[13]]+templates[19:23],
        "about_book":templates[:3]+templates[5:8]+templates[10:13]+templates[23:25],
        "like_author":templates[13:17],
        "ever_read_book":templates[17:19],
        "birthplace":templates[3:5],
        "multiple":templates
        }

def extractKeys(template):
    return re.findall(r'\<<(.*?)\>>',template)

def fill_templates(intent_,**kwargs):
    matches = []
    for t in templates_dict[intent_]:
        keys = extractKeys(t)
        if all([key in kwargs for key in keys]):
            # this template matches our kwargs, so we'll fill it in
            for key in kwargs:
                t=t.replace("<<%s>>"%key,kwargs[key])
            matches.append(t)
    return matches

def fallback_response():
    # replace fun_stuff with fallback responses that have
    # something to do with books. These could be pre-coded topic switches,
    # or they could be programmatically generated sentences based
    # on recent conversation. Your choice.
    fun_stuff = ['the earlest known work of literature is a Mesopotamian epic poem titled Epic of Gilgamesh','the first ever published book was the Gutenberg Bible, printed in 1453','the United States Library of Congress houses more than 38 million books','the act of smelling books is called bibliosmia','Harry Potter was the most banned book series in the 21st century','Fraz Kafka never actually finished a novel. His friend Max Brod organized his writings into novels after his death. Kafka had actually asked Brod to destroy them.','George Orwell borrowed the plot for 1984 from another novel titled We','David Foster Wallace\'s novel Infinite Jest began as three separate stories']#
    response = random.choice(fun_stuff)
    return response


def response(text):

    doc = nlp(text)
    text_ = text.lower()
    # Extract author names from text
    ne_tups = [(X.text,X.label_) for X in doc.ents]
    ne_persons = [tup[0] for tup in ne_tups if tup[1] == 'PERSON']
    authorNames = [name for name in ne_persons if name in authorIDs] 

    # Extract book titles from the user's utterance
    ESCAPE_CHARS = "[]\^$.|?*+()'\""
    bookTitles = []
    for bookName in bookIDs:
        book_name = bookName.lower()
        for e_char in ESCAPE_CHARS:
            book_name = book_name.replace(e_char,"\\"+e_char)
        try:
            book_regex = re.compile(r''+book_name)
        except:
            print("***",book_name,flush=True)
            break
        if book_regex.search(text_):
            bookTitles.append(bookName)

    # I personally don't like book titles that are parts of authors' names
    for a_n in authorNames:
        for b_t in bookTitles:
            if b_t in a_n:
                bookTitles.remove(b_t)

    #TODO: Modify this code to provide an interesting
    #      conversational framework. For this assignment,
    #      you must occasionally utilize the function
    #      the_graph.birthplaceOfAuthor(), as well as
    #      additional graph functions described in the
    #      assignment spec on LearningSuite.
    authors=[]
    books=[]
    active_phrase = "that"
    authorNamesAndBookTitles = authorNames+bookTitles
    if authorNamesAndBookTitles: # if any authors or books were mentioned
        abchoice = random.choice(authorNamesAndBookTitles)
        # note abchoice is a random choice of entity from the input text
        if abchoice in authorNames:
            author = abchoice
            active_phrase = author
            authors = [author]
            if author in authorIDs:
                books = the_graph.booksForAuthor(authorIDs[author])

        if abchoice in bookTitles:
            book = abchoice
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

    if "author" in kwargs:
        # Some authors names from SPARQL are not formated to be drawn from authorIDs. Just ignore these
        try:
            kwargs["placeOfBirth"] = random.choice(the_graph.birthplaceOfAuthor(authorIDs[kwargs['author']]))
            kwargs["dateOfBirth"] = the_graph.birthdateOfAuthor(authorIDs[kwargs['author']])[0][:4]
            kwargs["dateOfDeath"] = the_graph.deathdateOfAuthor(authorIDs[kwargs['author']])[0][:4]
        except:
            pass
    if "book" in kwargs:
        # The book might not be in our unfortunately small book IDs
        try:
            kwargs["publishDate"] = the_graph.publishdateOfBook(bookIDs[kwargs['book']])[0][:4]
        except:
            pass
    
    # find intent
    intent_ = "multiple"

    if not bookTitles:
        # Tell me about <author>
        intent_ = "about_author"
        # I like <author>
        if "i like" in text_:
            intent_ = "like_author"
        # What did <author> write?
        if "wrote" in text_ or "write" in text_ or "book" in text_:
            intent_ = "books_from_author"
        # Where was <author> from?
        if ("where" in text_ or "place" in text) and ("birth" in text_ or "born" in text_ or "live" in text_ or "from" in text_ or "raise" in text_ or "grow up" in text_):
            intent_ = "birthplace"
    
    if not authorNames:
        # Tell me about <book>
        intent_ = "about_book"
        if "you" in text_ and "read" in text_:
            intent_ = "ever_read_book"
        if "who" in text_ or "author" in text_:
            intent_ = "author_of_book"

    # Compose the response
    response = "Sorry, I'm not sure about " + active_phrase +", but " + fallback_response() #"I don't know what to say about " + active_phrase + "."
    if kwargs:
        matches = fill_templates(intent_,**kwargs)
        if matches:
            response = random.choice(matches)
    return response

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("input: ", sys.argv[1])
        print("response: ", response(sys.argv[1]))
    else:
        print(fill_templates(intent_="multiple",author1="Jane Austen", author2="Fred", book="Comet"))
        print(fill_templates(intent_="about_author",author="Philip K. Dick"))
        print(fill_templates(intent_="multiple",book="Mistborn", author="Brandon Sanderson"))
        print(fill_templates(intent_="birthplace",author="Jane Austen", placeOfBirth="Stevenson"))
        print(fill_templates(intent_="books_from_author",author="George Orwell"))
        print(fill_templates(intent_="like_author",author="Mary Shelley"))
        print(fill_templates(intent_="ever_read_book",book="Of Mice and Men"))
        print("Sorry, I didn't catch that. But " + fallback_response())
