# server.py
from interest import Service, http


class Service(Service):

    # Public

    @http.get('/')
    def hello(self, request, key):
        return http.Response(text='Hello World!')


# Listen forever
service = Service()
service.listen(host='127.0.0.1', port=9000, override=True, forever=True)
