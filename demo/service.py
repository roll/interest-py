import sys
from interest import Service, http


class Service(Service):

    # Public

    @http.get('/<key:path>')
    def hello(self, request, key):
        return http.Response(text='Hello World!')


# Create server
service = Service()

# Listen forever
argv = dict(enumerate(sys.argv))
service.listen(host=argv.get(1, '127.0.0.1'), port=argv.get(2, 9000))