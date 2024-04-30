from random import choice

from bs4 import BeautifulSoup

from locust import HttpUser, between, task


class AAPBUser(HttpUser):
    wait_time = between(1, 10)
    host = 'http://localhost:3000'

    def get_local_assets(self, html: str) -> list:
        # Return a list of local assets (css, js, img) from an html string

        html = BeautifulSoup(html.text, 'html.parser')
        css = [
            c
            for c in html.select('link[rel="stylesheet"]')
            if c['href'].startswith((self.host, '/'))
        ]
        js = [
            j
            for j in html.select('script')
            if j.get('src', '').startswith((self.host, '/'))
        ]
        img = [i for i in html.select('img') if i['src'].startswith((self.host, '/'))]
        return css + js + img

    def load_page(self, page):
        # Load a page and all its local assets
        home = self.client.get(f'/{page}')
        assets = self.get_local_assets(home)
        for i in assets:
            # print('GET:', i)
            self.client.get(i.get('src', i.get('href')))

    @task
    def home(self):
        self.load_page('')

    @task(5)
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

    @task(10)
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
            'advistory-committees',
            'newsletter',
            'volunteer',
            'podcast',
            'webinars',
            'feedback',
        ]
        page = choice(about_pages)
        self.load_page(f'about-the-american-archive/{page}')

    @task(5)
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
