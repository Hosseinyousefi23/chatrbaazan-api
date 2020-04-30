from rest_framework.response import Response


class CustomJSONRenderer:
    def render(self, response=None, status=200):
        # call super to render the response

        return Response(response, status=status)

    def renderData(self, data=None, status=200):
        # call super to render the response
        response = {
            'data': data
        }
        return Response(response, status=status)

    def render404(self, model_name, params):
        response_data = {
            "errors": [
                {
                    "param": params,
                    "status": 404,
                    "code": "not-found",
                    "title": "{} Not Found".format(model_name),
                    "detail": "{} is not available on this server".format(model_name)
                }
            ]
        }

        return Response(response_data, status=404)

    def render401(self, detail):
        response_data = {
            "errors": [
                {
                    "status": 401,
                    "code": "Can Not Accept Request.",
                    "detail": "{}".format(detail)
                }
            ]
        }

        return Response(response_data)

    def render400(self):
        response_data = {
            "errors": [
                {
                    "status": 400,
                    "code": "Bad Request!",
                }
            ]
        }

        return Response(response_data)

    def render500(self, error, message):
        response_data = {
            'message': message,
            'data': None,
            'error': error,
            'status': 500

        }
        # call super to render the response

        return Response(response_data, status=500)
