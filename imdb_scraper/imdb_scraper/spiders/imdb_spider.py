import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt1596343/']

    def parse(self, response):
        next_page = response.urljoin('fullcredits/')
        yield scrapy.Request(next_page, callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        links = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        for link in links:
            next_page = response.urljoin(link)
            yield scrapy.Request(next_page, callback=self.parse_actor_page)
           

    def parse_actor_page(self, response):
        actor = response.css('h1.header span.itemprop::text').get()
        for movie in response.css('div#filmo-head-actor + div > div.filmo-row'):    
            name = movie.css('a::text').get()

            yield {
                "actor" : actor,
                "movie_or_TV_name" : name   
                }