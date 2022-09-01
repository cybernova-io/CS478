from flask import jsonify

class WebHelpers:

    @staticmethod
    def EasyResponse(msg, status_code):
        
        data = {
            'msg': msg
        }

        resp = jsonify(data)
        resp.status_code = status_code

        return resp