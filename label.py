import mysql.connector


class Label:
    def __init__(self, name, value):
        self.id = None
        self.name = name
        self.value = value

    def setID(self, id):
        self.id = id

class LabelDAO:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost", user="root", password="chuan28112002", database="pthttm"
        )
        self.cursor = self.db.cursor()

    def getAllLabel(self):
        query = "SELECT * FROM label"
        self.cursor.execute(query)
        rs = self.cursor.fetchall()
        self.cursor.close()
        labelList = []
        for row in rs:
            label = Label(row[1], row[2])
            label.setID(row[0])
            labelList.append(label)
        return labelList

    def findLabelByName(self, name):
        query = "SELECT * FROM label WHERE name=%s"
        self.cursor.execute(query, (name,))
        rs = self.cursor.fetchall()
        self.cursor.close()
        labelList = []
        for row in rs:
            label = Label(row[1], row[2])
            label.setID(row[0])
            labelList.append(label)
        return labelList

    def findLabelById(self, id):
        query = "SELECT * FROM label WHERE id=%s"
        self.cursor.execute(query, (id,))
        rs = self.cursor.fetchall()
        self.cursor.close()
        labelList = []
        for row in rs:
            label = Label(row[1], row[2])
            label.setID(row[0])
            labelList.append(label)
        return labelList


    def updateLabel(self, label, id):
        try:
            query = "UPDATE label SET name=%s, value=%s WHERE id =%s"
            self.cursor.execute(
                query,
                (
                    label.name,
                    label.value,
                    id,
                ),
            )
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False

    def deleteLabel(self, id):
        try:
            query = "DELETE FROM label WHERE id=%s"
            self.cursor.execute(query, (id,))
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False

    def findLabelById(self, id):
        query = "SELECT * FROM label WHERE id=%s"
        self.cursor.execute(query, (id,))
        rs = self.cursor.fetchall()
        self.cursor.close()
        labelList = []
        for row in rs:
            label = Label(row[1], row[2])
            label.setID(row[0])
            labelList.append(label)
        return labelList

    def insertLabel(self,label):
        try:
            query = "INSERT INTO label (name, value) VALUES (%s,%s)"
            self.cursor.execute(
                query,
                (
                    label.name,
                    label.value,
                ),
            )
            self.db.commit()
            self.cursor.close()
            return True
        except:
            return False

    def findLabelByValue(self,value):
        query = "Select id from label where value=%s limit 1"
        self.cursor.execute(query,(value,))
        rs=self.cursor.fetchall()
        for row in rs:
            labelID = row[0]
            
        return labelID

