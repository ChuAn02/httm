class Model:
    def __init__(self, model=None):
        if model != None:
            self.create(
                model[0],
                model[1],
                model[2],
                model[3],
                model[4],
                model[5],
                model[6],
                model[7],
                model[8],
                model[9],
                model[10],
            )

    def create(self, id, name, path, date, acc, pre, recall, f1_score, des, status, quanlity):
        self.id = id
        self.name = name
        self.path = path
        self.date = date.strftime("%d-%m-%Y")
        self.acc = acc
        self.pre = pre
        self.recall = recall
        self.f1_score = f1_score
        self.des = des
        self.status = status
        self.quanlity = quanlity
