# coding = 'utf-8'


class DXResponse(object):

    def __init__(self, code=0, description='', data=None):
        self.code = code
        self.description = description
        self.data = data
