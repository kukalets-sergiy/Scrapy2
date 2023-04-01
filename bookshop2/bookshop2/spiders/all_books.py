import scrapy
import csv

class BookSpider(scrapy.Spider):
    name = 'all_books'
    start_urls = ['https://bookclub.ua/catalog/books/thriller_horror_books/']

    def parse(self, response):
        for link in response.css('div.book-inlist-img a::attr(href)'):
            yield response.follow(link, callback=self.parse_book)

        for i in range(1, 10):
            next_page = f'https://bookclub.ua/catalog/books/thriller_horror_books/?i={i}'
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        yield{
            'name': response.css('article.prd-m-info-block h1::text').get().strip(),
            'price': response.css('div.prd-your-price-numb::text').get().strip(),
            'pages': response.css('div.pereplet::text').get().split(' ')[1],
            'genre': response.css('div.prd-attr-descr a::text')[1].get()
        }

    def closed(self, reason):
        books = list(self.parse_book(response=None))
        fieldnames = ['name', 'price', 'pages', 'genre']

        with open('all_books.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(books)
