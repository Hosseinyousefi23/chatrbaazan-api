from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class CustomJSONRenderer:
    def render(self, response=None, status=200):
        # call super to render the response

        return Response(response, status=status)

    def renderData(self, data=None, status=200):
        # call super to render the response
        response = {
            'data': data
        ***REMOVED***
        return Response(response, status=status)

    def render404(self, model_name, params):
        response_data = {
            "errors": [
                {
                    "param": params,
                    "status": 404,
                    "code": "not-found",
                    "title": "{***REMOVED*** Not Found".format(model_name),
                    "detail": "{***REMOVED*** is not available on this server".format(model_name)
                ***REMOVED***
            ]
        ***REMOVED***

        return Response(response_data)

    def render401(self, detail):
        response_data = {
            "errors": [
                {
                    "status": 401,
                    "code": "Can Not Accept Request.",
                    "detail": "{***REMOVED***".format(detail)
                ***REMOVED***
            ]
        ***REMOVED***

        return Response(response_data)

    def render400(self):
        response_data = {
            "errors": [
                {
                    "status": 400,
                    "code": "Bad Request!",
                ***REMOVED***
            ]
        ***REMOVED***

        return Response(response_data)

    def render500(self, error, message):
        response_data = {
            'message': message,
            'data': None,
            'error': error,
            'status': 500

        ***REMOVED***
        # call super to render the response

        return Response(response_data, status=500)
