# This file contain all routes of student (This file is for Roberto)

####################################################################
#                             import
####################################################################
from api.student import student  # to use api
from flask_restx import Resource, reqparse, fields  # to use Resource, that expose http request method
from mysql.connector import Error
from api.student.models import student_model,login_student_model
import mysql.connector


####################################################################
#                             function
####################################################################
def loginStudent(matricola_studente, password_studente):
    records = []

    try:
        connects = mysql.connector
        connects.connect()
        connection = mysql.connector.connect(host='localhost',
                                             database='my_university_db',
                                             user='root',
                                             password='')
        cursor = connection.cursor()

        sql_select_Query = """SELECT persona.cf,
                                     persona.nome,
                                     persona.cognome, 
                                     persona.data_di_nascita, 
                                     persona.luogo_di_nascita, 
                                     persona.cap, 
                                     persona.via_piazza, 
                                     persona.civico, 
                                     studente.matricola_studente,
                                     studente.email_studente, 
                                     studente.data_immatricolazione
                                FROM persona INNER JOIN studente 
                                ON persona.cf = studente.cf 
                                WHERE studente.matricola_studente = %s
                                AND studente.password_studente = %s"""


        student_tuple = (matricola_studente, password_studente)

        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_select_Query, student_tuple)
        records = cursor.fetchall()


        print('prima del for')
        print(records)

        mysql_query_contacts = """SELECT tipo_contatto, valore_contatto
                                          FROM contatto_persona
                                          WHERE cf = %s"""

        record_tuple = (records[0]['cf'],)
        cursor.execute(mysql_query_contacts, record_tuple)
        contacts = cursor.fetchall()

        print(contacts)

        records[0]['contatti'] = contacts

        print("Fetching each row using column name")

    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
            return records


####################################################################
#                             routing
####################################################################
# ============================    studente    ========================== #
@student.route('/login')
class Login(Resource):

    @student.expect(login_student_model)
    @student.marshal_with(student_model)
    def post(self):
        # arguments
        parser = reqparse.RequestParser()
        parser.add_argument('matricola_studente', type=str, help='bd of student')
        parser.add_argument('password_studente', type=str, help='bd of student')
        args = parser.parse_args(strict=True)

        return loginStudent(args['matricola_studente'], args['password_studente']), 201


# ============================    update password    ========================== #
@student.route('/password')
class Password(Resource):

    def post(self):
        return {'password': '1'}


# ============================    get contatto   ========================== #
@student.route('/contatti')
class GetContact(Resource):

    def post(self):
        return {'contatti': '1'}


# ============================    get discipline   ========================== #
@student.route('/discipline')
class Discipline(Resource):

    def post(self):
        return {'riceve disciplina': '1'}


# ============================    segui disciplina   ========================== #
@student.route('/follow_disciplina')
class FollowDiscipline(Resource):

    def post(self):
        return {'segui disciplina': '1'}


# ============================    unfollow disciplina   ========================== #
@student.route('/unfollow_disciplina')
class UnfollowDiscipline(Resource):

    def post(self):
        return {'segui disciplina': '1'}


# ============================    calendario   ========================== #
@student.route('/calendario')
class Calendario(Resource):

    def post(self):
        return {'iscrizione newsletter': '1'}
