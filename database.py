# ----------------------------------------------------------
# Aristeia Academy
# GPL-3.0 Licensed
# See LICENSE for details.
# ----------------------------------------------------------

# BACKEND DATABASE LOGIC
import mysql.connector
from mysql.connector import Error # catch errors from mysql
from setup_questions import load_default_questions

DATABASE_NAME = "aristeiaDB"  # REPLACE WITH YOUR DB name
SUBJECTS = {
    "PHYSICS": [
        "Electric Charges and Fields", "Electrostatic Potential and Capacitance",
        "Current Electricity", "Moving Charges and Magnetism", "Magnetism and Matter",
        "Electromagnetic Induction", "Alternating Current", "Electromagnetic Waves",
        "Ray Optics and Optical Instruments", "Wave Optics", "Dual Nature of Radiation",
        "Atoms", "Nuclei", "Semiconductor Electronics"
    ],
    "CHEMISTRY": [
        "Solutions", "Electrochemistry", "Chemical Kinetics", "d and f Block Elements",
        "Coordination Compounds", "Haloalkanes and Haloarenes", "Alcohols, Phenols",
        "Aldehydes, Ketones and Acids", "Amines", "Biomolecules"
    ],
    "MATHEMATICS": [
        "Relations and Functions", "Inverse Trigonometric Functions", "Matrices",
        "Determinants", "Continuity and Differentiability", "Derivatives Application",
        "Integrals", "Integrals Application", "Differential Equations", "Vector Algebra",
        "Three Dimensional Geometry", "Linear Programming", "Probability"
    ],
    "ENGLISH": [
        "The Last Lesson", "Lost Spring", "Deep Water", "The Rattrap", "Indigo",
        "Poets and Pancakes", "The Interview", "Going Places", "My Mother at Sixty-Six",
        "Keeping Quiet", "A Thing of Beauty", "A Roadside Stand", "Aunt Jennifer's Tigers"
    ],
    "COMP SCI": [
        "Functions", "Recursion", "File Handling", "Binary Files", "CSV Files",
        "Exception Handling", "Database Concepts", "SQL Queries", "DDL Commands",
        "DML Commands", "Aggregate Functions", "GROUP BY", "JOINS", "Networks"
    ]
}

def get_server_connection(): # returns the connection object (needs to do "use table" command)
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="9090"  # REPLACE WITH YOUR MYSQL PASSWORD
        )
    except Error as e:
        print("Server connection failed:", e)
        return None

def get_database_connection(): # returns the connection object to database (no need of "use table" command)
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="9090",  # REPLACE WITH YOUR MYSQL PASSWORD
            database=DATABASE_NAME
        )
    except Error as e:
        print("Database connection failed:", e)
        return None

def create_database():
    conn = get_server_connection()
    if conn is None: return False # if it is none then return false, that means exit the function
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"Database '{DATABASE_NAME}' ready.")
        return True
    except Error as e:
        print("Database creation failed:", e)
        return False
    finally:
        cursor.close() # clean up
        conn.close()   # clean up


# function to create tables.
# auto increment: automatically id count goes like 1,2,3 etc
# on delete cascase: delete all foreign key references if the original column was dropped
# UNIQUE(subject_id, chapter_name) : their "combination" must be unique

def create_tables():
    conn = get_database_connection()
    if conn is None: return # if it is none then return false, that means exit the function
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects(
                subject_id INT AUTO_INCREMENT PRIMARY KEY,
                subject_name VARCHAR(100) UNIQUE NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chapters(
                chapter_id INT AUTO_INCREMENT PRIMARY KEY,
                subject_id INT NOT NULL,
                chapter_name VARCHAR(200) NOT NULL,
                FOREIGN KEY(subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
                UNIQUE(subject_id, chapter_name)
            )
        """)
        # default values -> difficulty = EASY, is_done = 0 (false)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions(
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                subject_id INT NOT NULL,
                chapter_id INT NOT NULL,
                question_text VARCHAR(500) NOT NULL UNIQUE,
                answer_text LONGTEXT,
                difficulty VARCHAR(20) DEFAULT 'EASY',
                is_done TINYINT(1) DEFAULT 0,
                FOREIGN KEY(subject_id) REFERENCES subjects(subject_id),
                FOREIGN KEY(chapter_id) REFERENCES chapters(chapter_id)
            )
        """)
        # default values -> task_priority = priority 3 (LOW)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todo(
                task_id INT AUTO_INCREMENT PRIMARY KEY,
                task_text TEXT NOT NULL,
                task_priority VARCHAR(20) DEFAULT 'P3 (LOW)'
            )
        """)
        # default values -> current_theme = LIGHT, xp = 0 (xp is updated only when question is done or deleted)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data(
                user_data_id INT PRIMARY KEY AUTO_INCREMENT,
                current_theme VARCHAR(50) DEFAULT 'LIGHT',
                xp INT DEFAULT 0
            )
        """)
        conn.commit() # just in case...
        print("Tables ready.")
    except Error as e:
        print("Table creation failed:", e)
    finally:
        cursor.close() # clean up
        conn.close()   # clean up

def insert_default_subjects_and_chapters(): # inserts values into hardcoded tables, ie fill with subject names and chapter names
    conn = get_database_connection()
    if conn is None: return
    try:
        cursor = conn.cursor()
        for subject_name, chapters in SUBJECTS.items(): # from the dict, subject names and its chapters are iterated
            cursor.execute("INSERT IGNORE INTO subjects(subject_name) VALUES(%s)", (subject_name,)) # ignore : to ignore if the row already added,  we only pass subject_name as subject_id auto_incremented
            cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = %s", (subject_name,)) # selects the auto_incremented subject_id
            subject_id = cursor.fetchone()[0] # fetches the data, eg: (1,)[0] = 1, so subject_id = 1 , loops like that ...
            
            # inner loop
            # iterates through each chapters of each subjects one by one
            # subject_id from outer loop's fetchone()[0] , chapter_name for inner loop, chapter_id : auto incremented

            for chapter in chapters:
                cursor.execute("INSERT IGNORE INTO chapters(subject_id, chapter_name) VALUES(%s, %s)", (subject_id, chapter))
        conn.commit() # commit DML changes
        print("Subjects and chapters inserted.")
    except Error as e:
        print("Default data insertion failed:", e)
    finally:
        cursor.close() # clean up
        conn.close()   #clean up

def create_default_user(): # table for storing theme data and xp levels
    conn = get_database_connection()
    if conn is None: return
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT IGNORE INTO user_data(user_data_id, current_theme, xp) VALUES(1, 'LIGHT', 0)") # we need only one row, we update the row values -> set themes and update xp levels
        conn.commit() # commit DML changes
        print("Default user data ready.")
    except Error as e:
        print("User data creation failed:", e)
    finally:
        cursor.close() # clean up
        conn.close()   # clean up


# function to call all the above defined functions
# we have been returing booleans through out
# so only if create_database returns true then we run it and other functions

def initialize_database():
    print("+-----------------------------------+")
    print("| Initializing Aristeia DB...       |")
    print("+-----------------------------------+")
    if create_database(): # checks if the function is truthy
        create_tables()
        insert_default_subjects_and_chapters()
        create_default_user()
        # run only if no Qs exist
        conn = get_database_connection()
        if conn and not conn.cursor().execute("SELECT 1 FROM questions LIMIT 1") or not conn.cursor().fetchone(): # fetches the first row, if no rows then load default questions
            load_default_questions() # load  default Qs into the db
    print("+-----------------------------------+")
    print("| Initialization complete.          |")
    print("+-----------------------------------+")

# CRUD for Questions 
# ADD questions
def add_question(sub_name, ch_name, q, a, diff): # here a: answer column is nullable
    conn = get_database_connection()
    if not conn: return False
    cursor = None # init cursor to avoid finally block crash
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT subject_id FROM subjects WHERE subject_name = %s", (sub_name,)) # we will pass the argument for subject_name from the selected data of dropdown in the ui
        sub_res = cursor.fetchone() # grab the 1st tuple
        if not sub_res: return False # exit if didnt got the tuple
        sub_id = sub_res[0] # index zero of the retrieved tuple is the subject_id
        
        cursor.execute("SELECT chapter_id FROM chapters WHERE chapter_name = %s AND subject_id = %s", (ch_name, sub_id)) # we will pass the argument for chapter_name from the selected data of dropdown in the ui
        ch_res = cursor.fetchone() # grab the 1st tuple
        if not ch_res: return False # exit if didnt got the tuple
        ch_id = ch_res[0] # index zero of the retrieved tuple is the chapter_id
        
        # inserting new question, answer will be null now, we will later update its value.
        cursor.execute("""
            INSERT INTO questions(subject_id, chapter_id, question_text, answer_text, difficulty) 
            VALUES(%s, %s, %s, %s, %s)
        """, (sub_id, ch_id, q, a, diff)) # sub_id and ch_id attained with help of fetchone() . question , difficulty comes directly from user
        
        conn.commit() # reflect the changes after DML
        return True # all the processes ran successfully
    except Error as e:
        if conn: conn.rollback() # FIX: undo partial inserts if things break midway
        print("Error adding question:", e)
        return False # didnot ran successfully
    finally:
        if cursor: cursor.close() # clean up (if curson is truthy)
        if conn: conn.close()   # clean up (if curson is truthy)


# function to get all the questions of the chapter selected by user, for home page : after clikcing the chapter card 
# returns a list of data about stored questions, if no questions then empty list
def get_questions_by_chapter(ch_name): 
    conn = get_database_connection()
    if not conn: return [] # returns empty list for failed connection
    questions = []
    try:
        cursor = conn.cursor(dictionary=True) # dictionary=True makes results come back as a Python dict instead of a tuple 
        
        # q,s,c are aliases for respective tables, id, sub, ch, q, a, diff are aliases for the columns we SELECTed
        # order of working: first we natural join the tables, then select the columns of the conditioned chapter, then fetchall() to get all the questions of that chapter
        cursor.execute("""
            SELECT q.question_id as id, s.subject_name as sub, c.chapter_name as ch,
                   q.question_text as q, q.answer_text as a, q.difficulty as diff, q.is_done
            FROM questions q
            NATURAL JOIN subjects s
            NATURAL JOIN chapters c
            WHERE c.chapter_name = %s
        """, (ch_name,))
        questions = cursor.fetchall() # to get ALL the questions
    except Error as e:
        print("Error getting questions:", e)
    finally:
        cursor.close() # clean up
        conn.close()   # clean up
    return questions


# q,s,c are aliases for respective tables, id, sub, ch, q, a, diff are aliases for the columns we SELECTed
# we use natural join to get the resulting set as per requirement, order by q_id in descending order helps get the last added row at top
# LIMIT 1 : to stop selecting rows after it grabs one row, here the one row it will grab is the last added row as it is at top due to DESC
def get_latest_question(): 
    conn = get_database_connection()
    if not conn: return None
    try:
        cursor = conn.cursor(dictionary=True) # results come back as a Python dict instead of a tuple
        cursor.execute("""
            SELECT q.question_id as id, s.subject_name as sub, c.chapter_name as ch,
                   q.question_text as q, q.answer_text as a, q.difficulty as diff
            FROM questions q
            NATURAL JOIN subjects s
            NATURAL JOIN chapters c
            ORDER BY q.question_id DESC LIMIT 1
        """)
        return cursor.fetchone() # return the 1st row as a result of running this fn
    except Error as e:
        print("Error getting latest question:", e)
        return None
    finally:
        cursor.close() # clean up
        conn.close()   # clean up

# for the QLineEdit (search bar) , takes a query as argument, returns a list
# q,s,c are aliases for respective tables, id, sub, ch, q, a, diff are aliases for the columns we SELECTed
# the argument query is a search keyword, we use it as a substring, with use of LIKE operator we can select data about the question
# the substring can be a part of the question or its answer that is already present in the database OR even search 'EASY' and get all easy questions
def search_questions(query):
    conn = get_database_connection()
    if not conn: return [] # empty list if fails
    try:
        cursor = conn.cursor(dictionary=True) # result as dict instead of a tuple
        cursor.execute("""
            SELECT q.question_id as id, s.subject_name as sub, c.chapter_name as ch,
                   q.question_text as q, q.answer_text as a, q.difficulty as diff
            FROM questions q
            NATURAL JOIN subjects s
            NATURAL JOIN chapters c
            WHERE q.question_text LIKE %s OR q.answer_text LIKE %s OR q.difficulty LIKE %s
        """, (f"%{query}%", f"%{query}%" , f"%{query}%"))
        return cursor.fetchall() # returns data filled list of dictionarie(s)
    except Error as e:
        print("Error searching questions:", e)
        return [] # empty list if error occurs
    finally:
        cursor.close() # clean up
        conn.close()   # clean up


# new question and q_id comes from frontend codes as arguments
def update_question_text(q_id, new_q): # to edit the existing questions
    conn = get_database_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE questions SET question_text = %s WHERE question_id = %s", (new_q, q_id))
        conn.commit() # reflect the change
        return True   # success
    except Error as e:
        print("Error updating question:", e)
        return False # failed
    finally:
        cursor.close() # clean up
        conn.close()   # clean up


# new answer and q_id comes from frontend codes as arguments
def update_question_answer(q_id, new_a): # to edit the existing answers
    conn = get_database_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE questions SET answer_text = %s WHERE question_id = %s", (new_a, q_id))
        conn.commit() # reflect changes
        return True   # success
    except Error as e:
        print("Error updating answer:", e)
        return False # failed
    finally:
        cursor.close() # clean up
        conn.close()   # clean up

# CRUD DELETE question
def delete_question(q_id): # to permanently delete the question
    conn = get_database_connection()
    if not conn: return False
    cursor = None # init cursor to avoid finally block crash
    try:
        cursor = conn.cursor()
        
        # fetch difficulty before deleting so we know how much XP to drop
        cursor.execute("SELECT difficulty FROM questions WHERE question_id = %s", (q_id,))
        q_res = cursor.fetchone()
        if not q_res: return False # exit if question doesn't exist
        diff = q_res[0]
        
        cursor.execute("DELETE FROM questions WHERE question_id = %s", (q_id,))
        
        # update xp (we dont make new rows, only update the one and only one row in the user_data table)
        # to calculate xp we use simple logic based on the difficulty of the added question.
        xp_loss = 1 # default difficulty is EASY ie -1 xp
        if diff.upper() == "MODERATE": xp_loss = 3 
        elif diff.upper() == "HARD": xp_loss = 5 
        
        # we use IF() function to ensure that xp doesnt go below 0, if so then set it to 0
        cursor.execute("""
            UPDATE user_data 
            SET xp = IF(xp < %s, 0, xp - %s) 
            WHERE user_data_id = 1
        """, (xp_loss, xp_loss)) # loss as argument
        
        conn.commit() # reflect the change
        return True # success
    except Error as e:
        if conn: conn.rollback() # undo delete if XP update fails , tnx stackoverflow ...
        print("Error deleting question:", e)
        return False # failed
    finally:
        if cursor: cursor.close() # clean up (if curson is truthy)
        if conn: conn.close()   # clean up (if curson is truthy)

# to update xp based on toggle btn (old logic was to update on upload)
def toggle_question_status(q_id, is_done, diff):
    conn = get_database_connection()
    if not conn: return False # exit if no conn
    cursor = None 
    try:
        cursor = conn.cursor()
        
        # 1 means True (done), 0 means false (undone)
        status_val = 1 if is_done else 0 # means -> if is_done is True then its value = 1, else 0
        cursor.execute("UPDATE questions SET is_done = %s WHERE question_id = %s AND is_done != %s", (status_val, q_id, status_val))
        
        # simple xp logic based on the difficulty of added question.
        xp_val = 1 # default diff is EASY ie 1xp
        if diff.upper() == "MODERATE": xp_val = 3 
        elif diff.upper() == "HARD": xp_val = 5 
        
        if is_done:
            # question done -> add xp
            if cursor.rowcount > 0:
                cursor.execute("UPDATE user_data SET xp = xp + %s WHERE user_data_id = 1", (xp_val,))
        else:
            # question unchecked -> remove xp (no -negatives)
            if cursor.rowcount > 0:
                cursor.execute("""
                    UPDATE user_data 
                    SET xp = IF(xp < %s, 0, xp - %s) 
                    WHERE user_data_id = 1
                """, (xp_val, xp_val))
            
        conn.commit() # reflect the change
        return True # success
    except Exception as e:
        if conn: conn.rollback() # undo changes if anything fails
        print("Error toggling question status:", e)
        return False # failed
    finally:
        if cursor: cursor.close() # clean up
        if conn: conn.close()   # clean up

# CRUD for Tasks
def get_tasks(): # to get all the added tasks to render them in the ui (as a list of dict)
    conn = get_database_connection()
    if not conn: return [] # empty list : no tasks
    try:
        cursor = conn.cursor(dictionary=True) # result in dict, not tuple
        cursor.execute("SELECT task_id as id, task_text as task, task_priority as priority FROM todo")
        return cursor.fetchall() # to fetch ALL the added tasks
    except Error as e:
        print("Error getting tasks:", e)
        return [] # empty list : no tasks
    finally:
        cursor.close() # clean up
        conn.close()   # clean up

# task text and its priority comes from frontend codes as arguments. task_id have auto_increment
def add_task(task, priority): # to add new tasks
    conn = get_database_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todo(task_text, task_priority) VALUES(%s, %s)", (task, priority))
        conn.commit() # reflect the change
        return True   # success
    except Error as e:
        print("Error adding task:", e)
        return False # falied
    finally:
        cursor.close() # clean up
        conn.close()   # clean up

# new task_text and its task_id come from frontend codes as arguments
def update_task(t_id, new_task): # to edit the existing tasks
    conn = get_database_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE todo SET task_text = %s WHERE task_id = %s", (new_task, t_id)) 
        conn.commit() # reflect changes
        return True # success
    except Error as e:
        print("Error updating task:", e)
        return False # failed
    finally:
        cursor.close() # clean up
        conn.close()   # clean up

def delete_task(t_id): # to permanently delete a task
    conn = get_database_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todo WHERE task_id = %s", (t_id,))
        conn.commit() # reflect the change
        return True # success
    except Error as e:
        print("Error deleting task:", e)
        return False # failed
    finally:
        cursor.close() # clean up
        conn.close()   # clean up



# User & Dashboard Stats 
def get_user_data():
    conn = get_database_connection()
    if not conn: return {"current_theme": "LIGHT", "xp": 0} # our default theme and initial xp
    try:
        cursor = conn.cursor(dictionary=True) # result as dict, not a tuple
        cursor.execute("SELECT current_theme, xp FROM user_data WHERE user_data_id = 1") # there is only one row anyway
        return cursor.fetchone() # retrives and returns the only existing one row
    except Error as e:
        print("Error getting user data:", e)
        return {"current_theme": "LIGHT", "xp": 0} # return default in case of errors
    finally:
        cursor.close() # clean up
        conn.close()   # clean up

# theme engine backend
# we update the default value of "LIGHT" to new respective value for the selected theme.
# new theme_name comes from frontend part of theme engine
def update_theme(theme_name): # to switch themes
    conn = get_database_connection()
    if not conn: return
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE user_data SET current_theme = %s WHERE user_data_id = 1", (theme_name,))
        conn.commit() # reflect the theme switch to as it make style changes in UI
    except Error as e:
        print("Error updating theme:", e)
    finally:
        cursor.close() # clean up
        conn.close()   # clean up


# to get data for graphs in dashboard
# stats is a nested dict to store required data for plotting graphs using matplot lib
def get_dashboard_stats():
    conn = get_database_connection()
    stats = {
        "diff_counts": {"EASY": 0, "MODERATE": 0, "HARD": 0},
        "subject_counts": {},
        "answered_ratio": {"Answered": 0, "Unanswered": 0}
    }
    if not conn: return stats # returns data with zero values
    try:
        cursor = conn.cursor()
        

        # Difficulty counts
        # working: row[0] means difficulty of the retrieved row, as row is a grouped by tuple having (difficulty, count)
        # if row[0] is truthy -> update the key of that purticular difficulty to the count value we got
        cursor.execute("SELECT difficulty, COUNT(*) FROM questions GROUP BY difficulty")
        for row in cursor.fetchall(): # ALL of the rows , it returns a list of tuples, eg: [('EASY', 4),('MODERATE', 3),('HARD' , 7)]
            if row[0]: 
                stats["diff_counts"][row[0].upper()] = row[1] 


        # Subject counts
        # we joins the tables and select subject_name and total no.of rows in question table after grouping them by individual subjects
        # so we get total no.of questions of each subjects
        cursor.execute("""
            SELECT s.subject_name, COUNT(q.question_id)
            FROM subjects s
            LEFT JOIN questions q ON s.subject_id = q.subject_id
            GROUP BY s.subject_name
        """)
        for row in cursor.fetchall(): # gets a list of tuples like: [('ENGLISH' , 6),('PHYSICS' , 2)]
            stats["subject_counts"][row[0]] = row[1] # updates the subject_counts with the subject names and its count as key:value pairs


        # Answered ratio
        # by default when a new question is added the answer_text has a value = 'Solution missing.'
        cursor.execute("SELECT COUNT(*) FROM questions WHERE answer_text NOT LIKE 'Solution missing.%%' AND answer_text IS NOT NULL AND TRIM(answer_text) != ''") # if answer_text is NOT : 'Solution missing.' AND not Null AND not an empty string.
        ans_count = cursor.fetchone()[0] # only one row to select anyway
        cursor.execute("SELECT COUNT(*) FROM questions WHERE answer_text LIKE 'Solution missing.%%' OR answer_text IS NULL OR TRIM(answer_text) = ''") # if answer_text is : 'Solution missing.' OR Null OR an empty string.
        unans_count = cursor.fetchone()[0] # only one row to select anyway
        
        # updating the values of the two keys
        stats["answered_ratio"]["Answered"] = ans_count
        stats["answered_ratio"]["Unanswered"] = unans_count
        
    except Error as e:
        print("Error getting dashboard stats:", e)
    finally:
        cursor.close() # clean up
        conn.close()   # clean up
    return stats # return to dictionary of data to the fn caller in frontend


# we will import the file to main.py
# prevent running while importing
if __name__ == "__main__":
    initialize_database()



