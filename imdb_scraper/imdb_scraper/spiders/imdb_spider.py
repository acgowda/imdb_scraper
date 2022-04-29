import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    # Set the movie page to scrape data from.
    start_urls = ['https://www.imdb.com/title/tt1596343/']

    def parse(self, response):
        """
        Callback used by Scrapy to process downloaded responses.

        Args:
            response (Response): An object that represents an HTTP response, fed to the Spiders for processing

        Yields:
            A new request with the movie's credits page and a callback to parse_full_credits(). 
        """
        # Set the url to go to next.
        next_page = response.urljoin('fullcredits/')
        yield scrapy.Request(next_page, callback=self.parse_full_credits)

    def parse_full_credits(self, response):
        """
        Callback used to process each actor included in the credits page.

        Args:
            response (Response): An object that represents an HTTP response, fed to the Spiders for processing

        Yields:
            A new request with an actor's page and a callback to parse_full_credits(). 
        """
        # Get relative links for all actors who worked on the specified movie.
        links = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        for link in links:
            # Set the url to go to next.
            next_page = response.urljoin(link)
            yield scrapy.Request(next_page, callback=self.parse_actor_page)
           

    def parse_actor_page(self, response):
        """
        Callback used to process each actor's credits page and read each movie or show they have acted in.

        Args:
            response (Response): An object that represents an HTTP response, fed to the Spiders for processing

        Yields:
            A dictionary containing the actor's name and the movie's name. 
        """
        # Get the actor's name.
        actor = response.css('h1.header span.itemprop::text').get()

        # Only looks at movies and shows the actor has acted in. (Not produced, written, etc.)
        for movie in response.css('div#filmo-head-actor + div > div.filmo-row'):  
            # Get the movie's name  
            name = movie.css('a::text').get()

            yield {
                "actor" : actor,
                "movie_or_TV_name" : name
                }