from werkzeug.routing import BaseConverter


class HashtagConverter(BaseConverter):
    def to_python(self, value):
        return '#' + value

    def to_url(self, value):
        return value[1:]
