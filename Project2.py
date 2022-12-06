# FALL 2021
# SI 206
# Name: Adam Brenner
# Who did you work with:

from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest


def get_titles_from_search_results():
    """
    Write a function that creates a BeautifulSoup object on "search_results.html". Parse
    through the object and return a list of tuples containing book titles, authors, and rating
    (as printed on the Goodreads website) in the format given below. Make sure to strip()
    any newlines from the book titles and author names.

    [('Book title 1', 'Author 1','Rating 1'), ('Book title 2', 'Author 2', 'Rating 2')...]
    """
    f = open('search_results.html', 'r')
    fileData = f.read()
    f.close()
    soup = BeautifulSoup(fileData, 'html.parser')
    table = soup.find('table', {'class':'tableList'})
    rows = table.find_all('tr')
    titles_list = []
    for row in rows:
        bookTitle = row.find_all('a',{'class':'bookTitle'})
        title = bookTitle[0].text.strip()
        authorContainer = row.find_all('div', {'class':'authorName__container'})
        author = authorContainer[0].text.strip()
        bookRating = row.find_all('span',{'class':'minirating'})
        rating = (bookRating[0].text.strip())[:4]
        tup = (title,author,rating)
        titles_list.append(tup)
    return titles_list


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "/book/show/" to 
    your list, and be sure to append the full path (https://www.goodreads.com) to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    soup = BeautifulSoup(requests.get("https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc").text, 'html.parser')
    linkList = []
    table = soup.find('table', {'class':'tableList'})
    rows = table.find_all('tr')
    for row in rows[:10]:
        link = row.find_all('a',{'class':'bookTitle'})
        linkString = 'https://www.goodreads.com' + link[0]['href'].strip()
        linkList.append(linkString)
    return linkList


def get_book_summary(book_html):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the HTML file of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, number of pages, 
    and book rating. This function should return a tuple in the following format:
    
    ('Some book title', 'the book's author', number of pages, book rating)
    
    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title, number of pages, and rating.


    """
    f = open(book_html, 'r')
    fileData = f.read()
    f.close()
    soup = BeautifulSoup(fileData, 'html.parser')
    title = soup.find('h1', {'id':'bookTitle'}).text.strip()
    author = soup.find('a', {'class':'authorName'}).text.strip()
    pages = soup.find('span', {'itemprop':'numberOfPages'}).text.strip(' pages')
    rating = soup.find('span', {'itemprop':'ratingValue'}).text.strip()
    tup = (title, author, int(pages), float(rating))
    return tup

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST 
    BOOKS OF 2021" page in "best_books_2021.html". This function should create a 
    BeautifulSoup object from a filepath and return a list of (category, book title, 
    URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The 
    Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should 
    append("Fiction", "The Testaments (The Handmaid's Tale, #2)", 
    "https://www.goodreads.com/choiceawards/best-fiction-books-2020")
    to your list of tuples.

    """
    f = open(filepath, 'r')
    fileData = f.read()
    f.close()
    soup = BeautifulSoup(fileData, 'html.parser')
    table = soup.find('div', {'class':'categoryContainer'})
    rows = table.find_all('div',{'class':'category clearFix'})
    bestBookList = []
    for row in rows:
        category = row.find('h4',{'class':'category__copy'}).text.strip()
        title = row.find_all('img',{'class':'category__winnerImage'})
        bookTitle = title[0]['alt'].strip()
        link = row.find_all('a')
        linkString = link[0]['href'].strip()
        tup = (category,bookTitle,linkString)
        bestBookList.append(tup)
    return bestBookList


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
   one that is returned by get_titles_from_search_results()), sorts the tuples in 
   descending order by largest rating, writes the data to a csv file, and saves it to 
   the passed filename.
   The first row of the csv should contain "Book title", "Author Name", “Rating”, 
   respectively as column headers. For each tuple in data, write a new
   row to the csv, placing each element of the tuple in the correct column.
 
   When you are done your CSV file should look like this:
 
   Book title,Author Name,Rating
   Book1,Author1,Rating1
   Book2,Author2,Rating2
   Book3,Author3,Rating3
   
   In order of highest rating to lowest rating.
 
   This function should not return anything.

    """
    with open(filename, "w", newline="") as fileout:
        
        header = ("Book title", "Author Name", "Rating")
        writer = csv.writer(fileout, delimiter=',')
        writer.writerow(header)
        output = sorted(data, key=lambda x: x[-1], reverse=True)
        for row in output:
            writer.writerow(row)




def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() and save to a local variable
        search_results = get_titles_from_search_results()
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(search_results),20)
        # check that the variable you saved after calling the function is a list
        self.assertEqual(type(search_results),list)
        # check that each item in the list is a tuple
        for item in search_results:
            self.assertEqual(type(item),tuple)
        # check that the first book and author tuple is correct (open search_results.html and find it)
        self.assertEqual(search_results[0],('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling', '4.62'))
        # check that the last title is correct (open search_results.html and find it)
        self.assertEqual(search_results[-1],('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling', '4.18'))

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        self.assertEqual(type(TestCases.search_urls),list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(TestCases.search_urls),10)
        # check that each URL in the TestCases.search_urls is a string
        for url in TestCases.search_urls:
            self.assertEqual(type(url),str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
            self.assertEqual(url[:36],'https://www.goodreads.com/book/show/')

    def test_get_book_summary(self):
        # the list of webpages you want to pass in one by one into get_book_summary
        summary_list = []
        html_list = ['book_summary_html_files/Fantasy Lover (Hunter Legends, #1) by Sherrilyn Kenyon.html',
                        'book_summary_html_files/Fantasy in Death (In Death, #30) by J.D. Robb.html',
                        'book_summary_html_files/Fantasy of Frost (The Tainted Accords, #1) by Kelly St. Clare.html',
                        'book_summary_html_files/The Mind’s I_ Fantasies and Reflections on Self and Soul by Douglas R. Hofstadter.html',
                        'book_summary_html_files/Gods and Mortals_ Fourteen Free Urban Fantasy & Paranormal Novels Featuring Thor, Loki, Greek Gods, Native American Spirits, Vampires, Werewolves, & More by C. Gockel.html',
                        'book_summary_html_files/Epic_ Legends of Fantasy by John Joseph Adams.html',
                        'book_summary_html_files/The Kingdom of Fantasy by Geronimo Stilton.html',
                        'book_summary_html_files/How to Write Science Fiction & Fantasy by Orson Scott Card.html',
                        'book_summary_html_files/Kurintor Nyusi_ Diverse Epic Fantasy by Aaron-Michael Hall.html',
                        'book_summary_html_files/Die, Vol. 1_ Fantasy Heartbreaker by Kieron Gillen.html']
        for html in html_list:
            book_summary = get_book_summary(html)
            summary_list.append(book_summary)
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summary_list),10)
            # check that each item in the list is a tuple
        for i in summary_list:
            self.assertEqual(type(i),tuple)
            # check that each tuple has 4 elements
            self.assertEqual(len(i),4)
            # check that the first two elements in the tuple are string
            self.assertEqual(type(i[0]) and type(i[1]), str)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(type(i[2]),int)
            # check that the fourth element in the tuple, i.e. rating is a float
            self.assertEqual(type(i[3]),float)
        # check that the first book in the search has 337 pages
        self.assertEqual(summary_list[0][2],337)
        # check the last book has 4.02 rating
        self.assertEqual(summary_list[-1][3],4.02)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        best_books = summarize_best_books('best_books_2020.html')
        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books),20)
            # assert each item in the list of best books is a tuple
        for i in best_books:
            self.assertEqual(type(i),tuple)
            # check that each tuple has a length of 3
            self.assertEqual(len(i),3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books[0],('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books[-1],('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))

    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.html and save the result to a variable
        result = get_titles_from_search_results()
        # call write csv on the variable you saved and 'test.csv'
        write_csv(result,'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv', 'r') as object:
            x = csv.reader(object)
            csv_lines = list(map(tuple,x))
        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines),21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0],('Book title', 'Author Name', 'Rating'))
        # check that the next row is 'Harry Potter Boxed Set, Books 1-5 (Harry Potter, #1-5)', 'J.K. Rowling,', '4.78'
        # ^^this version has a comma after J.K Rowling, however other versions of the answer might not have a comma. We accept both
        self.assertEqual(csv_lines[1],('Harry Potter Boxed Set, Books 1-5 (Harry Potter, #1-5)', 'J.K. Rowling,', '4.78'))
        # check that the last row is 'Harry Potter and the Cursed Child: Parts One and Two (Harry Potter, #8)', 'John Tiffany (Adaptation),', '3.62'
        # ^^^again in a different answer the result for authoer is J.K Rowling. We should accept both
        self.assertEqual(csv_lines[-1],('Harry Potter and the Cursed Child: Parts One and Two (Harry Potter, #8)', 'John Tiffany (Adaptation),', '3.62'))


if __name__ == '__main__':
    print(extra_credit("extra_credit.html"))
    unittest.main(verbosity=2)



