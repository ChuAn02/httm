import mysql.connector
# import fake_voice_detection.train_model
from train_model import  train_model
from model import Model
from fake_voice_regconition import fake_voice_regconition
from modelDAO import ModelDAO

class ServiceDAO:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost", user="root", password="chuan28112002", database="pthttm"
        )
        self.mycursor = self.mydb.cursor()

    # Insert new Model and set it as the default Model when perform train or retrain model.
    def train_or_retrain(self):
        model = train_model()
        # Get the sample quantity in order to check the condition to retrain model in the future.
        sql = 'SELECT COUNT(*) FROM sample;'
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        sample_quantity = myresult[0][0]

        sql = 'UPDATE sample SET status  = 1;'
        self.mycursor.execute(sql)
        self.mydb.commit()

        # Insert the new Model to database.
        sql = 'INSERT INTO model VALUES (%s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s);'

        print(sql)
        val = (model.id, model.name, model.path, float(model.acc), float(model.pre), float(model.recall), float(model.f1_score), model.des, model.status, sample_quantity)

        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def fake_voice_detection(self, file_path):
        # Get the active model's id.

        model_DAO = ModelDAO()
        active_model = model_DAO.getActiveModel()
        id = active_model.id

        return fake_voice_regconition(file_path, model_id= id)

# service_DAO = ServiceDAO()
# # service_DAO.train_or_retrain()
#
# print(service_DAO.fake_voice_detection())
