# This file contain all database functions of the students

####################################################################
#                             import
####################################################################
from mysql.connector import Error  # to use error


####################################################################
#                             DB_functions
####################################################################

def insert_richiesta_ricevimento(matricola_docente,
                                 data_ricevimento,
                                 matricola_studente,
                                 motivazione_ricevimento,
                                 connection):
    try:
        cursor = connection.cursor()
        sql_insert_richiesta_ricevimento_Query = """ 
        INSERT INTO richiesta_ricevimento 
        (matricola_docente, data_ricevimento, matricola_studente, motivazione_ricevimento) 
        VALUES (%s, %s, %s, %s);"""

        print('matricola_docente', matricola_docente)
        print('data_ricevimento', data_ricevimento)
        print('matricola_studente', matricola_studente)
        print('motivazione_ricevimento', motivazione_ricevimento)

        insert_tuple = (matricola_docente, data_ricevimento, matricola_studente, motivazione_ricevimento)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_insert_richiesta_ricevimento_Query, insert_tuple)
        connection.commit()
        print("Richiesta ricevimento inviata!")
    except Error as e:
        print("Error from MySQL", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

def delete_richiesta_ricevimento(matricola_docente,
                                 data_ricevimento,
                                 matricola_studente,
                                 connection):
    try:
        cursor = connection.cursor()
        sql_delete_richiesta_ricevimento_Query = """ 
            DELETE FROM richiesta_ricevimento
            WHERE matricola_docente  = %s
            AND data_ricevimento = %s
            AND matricola_studente = %s """

        print('matricola_docente', matricola_docente)
        print('data_ricevimento', data_ricevimento)
        print('matricola_studente', matricola_studente)

        delete_tuple = (matricola_docente, data_ricevimento, matricola_studente)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_delete_richiesta_ricevimento_Query, delete_tuple)
        connection.commit()
        print("delete Richiesta ricevimento effettuata!")
    except Error as e:
        print("Error from MySQL", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

def insert_iscrizione_newsletter(codice_corso,
                                 codice_disciplina,
                                 matricola_studente,
                                 data_iscrizione,
                                 connection):
    try:
        cursor = connection.cursor()
        sql_insert_richiesta_ricevimento_Query = """ 
        INSERT INTO iscrizione_newsletter 
        (codice_corso, codice_disciplina, matricola_studente, data_iscrizione) 
        VALUES (%s, %s, %s, %s);"""

        print('codice_corso', codice_corso)
        print('codice_disciplina', codice_disciplina)
        print('matricola_studente', matricola_studente)
        print('data_iscrizione', data_iscrizione)

        insert_tuple = (codice_corso, codice_disciplina, matricola_studente, data_iscrizione)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_insert_richiesta_ricevimento_Query, insert_tuple)
        connection.commit()
        print("Iscrizione newsletter effettuata!")
    except Error as e:
        print("Error from MySQL", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

def reperimento_news_studente(matricola_studente, connection):
    records = []
    try:
        cursor = connection.cursor()
        sql_select_Query = """    SELECT persona.nome, persona.cognome, docente.email_docente, 
                                    avviso.codice_disciplina, disciplina.nome_disciplina, 
                                    avviso.data_avviso, avviso.titolo_avviso, avviso.corpo_avviso
                                    FROM iscrizione_newsletter
                                    INNER JOIN disciplina
                                    ON( iscrizione_newsletter.codice_corso = disciplina.codice_corso 
                                        AND iscrizione_newsletter.codice_disciplina = disciplina.codice_disciplina)
                                    INNER JOIN avviso
                                    ON(disciplina.codice_corso = avviso.codice_corso 
                                        AND disciplina.codice_disciplina = avviso.codice_disciplina)
                                    INNER JOIN docente
                                    ON avviso.matricola_docente = docente.matricola_docente
                                    INNER JOIN persona
                                    ON docente.cf = persona.cf
                                    WHERE iscrizione_newsletter.matricola_studente = %s
                                    ORDER BY avviso.data_avviso DESC;"""
        student_tuple = (matricola_studente,)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_select_Query, student_tuple)
        records = cursor.fetchall()
        print(records)
        print("Fetching each row")
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
            return records

def reperimento_prenotazioni_ricevimento_studente(matricola_studente, connection):
    records = []
    try:
        cursor = connection.cursor()
        sql_select_Query = """SELECT
            richiesta_ricevimento.data_ricevimento,
            persona.nome, persona.cognome,
            docente.email_docente,
            richiesta_ricevimento.motivazione_ricevimento,
            richiesta_ricevimento.data_ricevimento,
            richiesta_ricevimento.durata
            FROM richiesta_ricevimento
            inner join ricevimento
            on richiesta_ricevimento.matricola_docente = richiesta_ricevimento.matricola_docente 
                and richiesta_ricevimento.data_ricevimento = ricevimento.data_ricevimento
            inner join docente
            on richiesta_ricevimento.matricola_docente = docente.matricola_docente
            inner join persona
            on docente.cf = persona.cf
            where richiesta_ricevimento.matricola_studente = %s
            ORDER by richiesta_ricevimento.data_ricevimento DESC;"""
        student_tuple = (matricola_studente,)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_select_Query, student_tuple)
        records = cursor.fetchall()
        print(records)
        print("Fetching each row")
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
            return records


# function to login the studente
def loginStudent(matricola_studente, password_studente, connection):
    students = []

    try:
        cursor = connection.cursor(dictionary=True)
        student_tuple = (matricola_studente, password_studente)
        mySQL_query_login_studente = """SELECT persona.cf,
                                               persona.nome,
                                               persona.cognome, 
                                               persona.data_di_nascita, 
                                               persona.luogo_di_nascita, 
                                               persona.cap, 
                                               persona.via_piazza, 
                                               persona.civico, 
                                               studente.matricola_studente,
                                               studente.email_studente, 
                                               studente.data_immatricolazione,
                                               studente.anno_in_corso
                                        FROM persona INNER JOIN studente 
                                        ON persona.cf = studente.cf 
                                        WHERE studente.matricola_studente = %s
                                        AND studente.password_studente = %s"""
        cursor.execute(mySQL_query_login_studente, student_tuple)
        students = cursor.fetchall()

        mySQL_query_get_student_contacts = """SELECT tipo_contatto, valore_contatto
                                              FROM contatto_persona
                                              WHERE cf = %s"""

        for temp_student in students:
            cursor.execute(mySQL_query_get_student_contacts, (temp_student['cf'],))
            temp_student['contatti'] = cursor.fetchall()

    except Error as e:
        print('Error reading data from MySQL table', e)
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print('MySQL connection is closed')
            return students


# function to update student password
def updatePassword(nuova_password_studente, matricola_studente, password_studente, connection):
    try:

        mySQL_query_update_password = """UPDATE studente 
                                         SET password_studente = %s 
                                         WHERE (matricola_studente = %s 
                                         AND password_studente = %s)"""

        student_tuple = (nuova_password_studente, matricola_studente, password_studente)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(mySQL_query_update_password, student_tuple)
        connection.commit()

        print('Password Updated!')
    except Error as error:
        print(f'Error from MySQL: {error}')
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print('MySQL connection is closed')


# function to follow a discipline
def followDiscipline(codice_corso, codice_disciplina, matricola_studente, connection):
    try:
        cursor = connection.cursor(dictionary=True)

        mySQL_query_follow_discipline = """INSERT INTO disciplina_seguita(codice_corso, codice_disciplina, matricola_studente)
                                           VALUES(%s, %s, %s)"""
        follow_discipline_tuple = (codice_corso, codice_disciplina, matricola_studente)
        cursor.execute(mySQL_query_follow_discipline, follow_discipline_tuple)
        connection.commit()
        print('Discipline followed')
    except Error as error:
        print(f"Error from mySQL: {error}")
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print('MySQL connection is closed')


# function to unfollow discipline
def unFollowDiscipline(codice_corso, codice_disciplina, matricola_studente, connection):
    try:
        cursor = connection.cursor(dictionary=True)

        mySQL_query_delete_follow_discipline = """DELETE FROM disciplina_seguita
                                                  WHERE codice_corso = %s
                                                  AND codice_disciplina = %s
                                                  AND matricola_studente = %s"""

        unFollow_discipline_tuple = (codice_corso, codice_disciplina, matricola_studente)
        cursor.execute(mySQL_query_delete_follow_discipline, unFollow_discipline_tuple)
        connection.commit()

        print('Discipline unfollowed')
    except Error as error:
        print(f"Error from mySQL: {error}")
    finally:
        if connection.is_connected():
            connection.close()
            cursor.close()
            print('MySQL connection is closed')


# function to get student calendar
def getCalendar(matricola_studente, connection):

    lessons = []
    try:
        mySQL_query_get_calendar = """SELECT disciplina_seguita.codice_corso,
                                             corso_di_laurea.nome_corso,
                                             doc.matricola_docente,
                                             doc.nome,
                                             doc.cognome,
                                             disciplina_seguita.codice_disciplina,
                                             disciplina.nome_disciplina,
                                             lezione.nome_sede,
                                             lezione.numero_piano,
                                             lezione.numero_aula,
                                             lezione.numero_ore,
                                             lezione.data_inizio,
                                             lezione.titolo,
                                             lezione.descrizione
                                       FROM studente
                                       NATURAL JOIN disciplina_seguita
                                       NATURAL JOIN disciplina
                                       NATURAL JOIN corso_di_laurea
                                       NATURAL JOIN lezione
                                       NATURAL JOIN aula
                                       NATURAL JOIN sede
                                       INNER JOIN (SELECT *  FROM persona
                                                   NATURAL JOIN docente
                                                   NATURAL JOIN insegna) AS doc
                                       ON disciplina.codice_disciplina = doc.codice_disciplina
                                       WHERE studente.matricola_studente = %s"""
        cursor = connection.cursor(dictionary=True)
        cursor.execute(mySQL_query_get_calendar, (matricola_studente,))
        lessons = cursor.fetchall()
    except Error as error:
        print(f"Error from mySQL: {error}")
    finally:
        if connection.is_connected():
            print('cacca')
            connection.close()
            cursor.close()
            print('MySQL connection is closed')
            return lessons