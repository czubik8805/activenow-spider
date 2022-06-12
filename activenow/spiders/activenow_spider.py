import scrapy
from scrapy import FormRequest
from scrapy.http import Request


class QuotesSpider(scrapy.Spider):
    name = "active_now"

    def start_requests(self):
        urls = [
            'https://app.activenow.io/users/sign_in',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        return [FormRequest.from_response(
            response,
            formdata={
                'user[email]': 'michalczuba88@gmail.com',
                'user[password]': '8r5#WPxcTNvi6GxBi^4k'
            },
            callback=self.after_login)]

    def after_login(self, response):
        if "Błędny adres email lub hasło" in response.text:
            return
        return Request(
            url="https://app.activenow.io/client_panel/cancellations/making_up_absences",
            callback=self.parse_tastypage
        )

    def parse_tastypage(self, response):
        # page = response.url.split("/")[-2]
        if "Brak proponowanych terminów" in response.text:
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX >>>>>>>>>>>>>>>>> brak terminów')
            return

        # send notification here!
        import pdb;pdb.set_trace()
