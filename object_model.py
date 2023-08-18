class Object:
    def __init__(self, data: list):
        self.title = []
        self.values = []
        if type(data) is list:
            for dat in data:
                if type(dict(dat).values()) is dict:
                    self.values.append(Object(dict(dat).values()))
                else:
                    self.values.append(list(dict(dat).values()))
                    if self.values:
                        self.title = list(dict(dat).keys())
        else:
            if type(dict(data).values()) is dict:
                [Object(dat) for dat in data.values() if type(dat) is dict]
                self.values.append(Object(dict(data).values()))
            else:
                self.values.append(list(data.values()))
                if self.values:
                    self.title = list(data.keys())