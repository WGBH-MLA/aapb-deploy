from random import choice

from bs4 import BeautifulSoup
from faker import Faker

from locust import HttpUser, between, task


class AAPBUser(HttpUser):
    wait_time = between(1, 5)
    host = 'http://localhost:3000'

    def get_local_assets(self, html: str) -> list:
        # Return a list of local assets (css, js, img) from an html string

        html = BeautifulSoup(html, 'html.parser')
        css = [
            c['href']
            for c in html.select('link[rel="stylesheet"]')
            if c['href'].startswith((self.host, '/'))
        ]
        js = [
            j['src']
            for j in html.select('script')
            if j.get('src', '').startswith((self.host, '/'))
        ]
        img = [
            i['src']
            for i in html.select('img')
            if i['src'].startswith((self.host, '/'))
        ]

        return list(set(css + js + img))

    def load_page(self, page):
        # Load a page and all its local assets
        html = self.client.get(f'/{page}').text
        assets = self.get_local_assets(html)
        for i in assets:
            # print('GET:', i)
            self.client.get(i)
        return html

    @task
    def home(self):
        self.load_page('')

    @task(2)
    def static(self):
        # Load a random static page

        pages = [
            'participating-orgs',
            'on-location',
            'search',
            'faq',
            'national-history-day',
            'contact-us',
            'resources',
            'donate',
        ]
        page = choice(pages)
        self.load_page(page)

    @task(2)
    def about(self):
        # Load a random about page
        about_pages = [
            '',
            'library-and-education-collaborators',
            'vision-and-mission',
            'history',
            'whats-new',
            'projects',
            'funding',
            'advisory-committees',
            'newsletter',
            'volunteer',
            'podcast',
            'webinars',
            'feedback',
        ]
        page = choice(about_pages)
        self.load_page(f'about-the-american-archive/{page}')

    @task(2)
    def help_page(self):
        # Load a random help page
        help_pages = [
            'contribute',
            'using-the-ams',
            'obtain-metadata',
            'station-communications-toolkit',
        ]
        page = choice(help_pages)
        self.load_page(f'help/{page}')

    @task(5)
    def catalog_search(self):
        from random import randint

        # Perform a search
        query = Faker().words(randint(1, 5))
        query = ' '.join(query)
        html = self.load_page(f'catalog?q={query}&f[access_types][]=online')
        page = BeautifulSoup(html, 'html.parser')

        # Follow a random search result
        links = [a['href'] for a in page.select('#documents article h2 a')]
        if links:
            result = choice(links)
            self.load_page(result)
