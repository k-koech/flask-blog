import urllib.request,json
from .models import Quote


# Getting the quotes base url
quote_url = None

def configure_request(app):
    global quote_url
    quote_url = app.config["QUOTE_URL"]


def get_quotes():
    '''
    Function that gets the random quotes
    '''  
    get_article_details_url = 'http://quotes.stormconsultancy.co.uk/random.json'.format()
    with urllib.request.urlopen(get_article_details_url) as url:
        quote_data = url.read()
        quote_data_response = json.loads(quote_data)

        quote_object = None
        if quote_data_response:
            author = quote_data_response.get('author')
            id = quote_data_response.get('id')
            quote = quote_data_response.get('quote')
            permalink =  quote_data_response.get('permalink') 
        quote_object = Quote(author,id,quote,permalink)
    return quote_data
     
     
