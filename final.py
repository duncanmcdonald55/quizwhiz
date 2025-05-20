import sqlite3
from prettytable import PrettyTable #type: ignore
from random import shuffle

conn = sqlite3.connect("Quizzes.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Questions (questionid INTEGER PRIMARY KEY, question TEXT NOT NULL, category TEXT NOT NULL);")
cur.execute("CREATE TABLE IF NOT EXISTS Answers (answerid INTEGER PRIMARY KEY, answer_1 TEXT NOT NULL, answer_2 TEXT NOT NULL, correct_answer TEXT NOT NULL, answer_4 TEXT NOT NULL, qid INTEGER NOT NULL, FOREIGN KEY (qid) REFERENCES Questions(questionid));")

    
def insert_question():

    question = input("Enter a question: ")
    category = input("What is the category?: ")
    cur.execute("INSERT INTO Questions(question, category) VALUES (?, ?);",(question,category))
    print()
    conn.commit()
    correct = input("What is the answer? ")
    while True:
        invalids = input("Enter three invalid answers, separated by -- <invalid1--invalid2--invalid3>: ").split('--')

        if not invalids or len(invalids) != 3:
            print("Invalid Length follow format instructions")
            continue
        break
    qid = cur.execute("SELECT questionid FROM Questions WHERE question = ? and category = ?;",(question, category))
    result = cur.fetchone()
    qid = result[0]
    cur.execute("INSERT INTO Answers(answer_1, answer_2, correct_answer, answer_4, qid) VALUES (?,?,?,?,?)",(invalids[0], invalids[1], correct, invalids[2], qid))
    conn.commit()

def view(name):

    if name in ["Answers", "Questions"]:

        try:

            cur.execute(f"SELECT * FROM {name};")
            data = cur.fetchall()

            table = PrettyTable()
            columns = [description[0] for description in cur.description]
            table.field_names = columns

            for row in data:
                table.add_row(row)
            print(table)

        except EOFError as e:
            print(f"Error! {e}")

def qanda():

    cur.execute("SELECT q.question, a.correct_answer FROM Questions q JOIN Answers a ON (a.qid = q.questionid);")
    data = cur.fetchall()

    table = PrettyTable()

    columns = [description[0] for description in cur.description]
    table.field_names = columns

    for row in data:
        table.add_row(row)
    print(table)    

def test_time():

    cur.execute("SELECT DISTINCT category FROM Questions")
    data = cur.fetchall()
    result = [row[0].lower() for row in data]
    result.append("all")

    print("Categories to quiz from!")

    for category in result:
        print(category)


    while True:

    
        command = input("What category do you want to study? <all> for the whole list: ").lower()

        if command not in result:
            print("ERROR WRONG CATEGORY")
            continue
        break
    

    if command == 'all':
        question_index = cur.execute("SELECT question FROM Questions;")
        questions = cur.fetchall()

        answer_index = cur.execute("SELECT answer_1, answer_2, correct_answer, answer_4 From Answers;")
        answers = cur.fetchall()
        print()
        print()
        print("Alright: you will begin a comprehensive quiz of various disciplines.  Get ready.")

    else:
        command = command.capitalize()

        question_index = cur.execute("SELECT question FROM Questions WHERE category = (?);",(command,))
        questions = cur.fetchall()

        answer_index = cur.execute("SELECT a.answer_1, a.answer_2, a.correct_answer, a.answer_4 FROM Answers a JOIN Questions q ON (q.questionid = a.qid) WHERE category = (?);",(command,))
        answers = cur.fetchall()
        print()
        print()
        print(f"Alright: You will begin a {command} Quiz.  There are {len(questions)} questions.  Good Luck!")


    print()

    j = 0
    score = 0

    while j < len(questions):

        for i, item in enumerate(questions):

            print(f"Question {i + 1}: {item[0]}")
            print()
            j += 1

            raw_answers = list(answers[i])
            correct_answer = raw_answers[2]
            shuffled_answers = raw_answers[:]
            shuffle(shuffled_answers)

            choices = ['a','b','c','d']

            answer_key = dict(zip(choices, shuffled_answers))

            for choice, text in answer_key.items():
                if text == correct_answer:
                    correct_letter = choice

            print(f"a. {shuffled_answers[0]}")
            print(f"b. {shuffled_answers[1]}")
            print(f"c. {shuffled_answers[2]}")
            print(f"d. {shuffled_answers[3]}")

            print()

            while True:

                user_answer = input("What is your answer?  Enter a, b, c, or d: ").lower()
                print()

                if user_answer not in "abcd":
                    print("Incorrect Output")
                    continue
                
                if user_answer == correct_letter:
                    print("Correct!!")
                    score += 1
                else:
                    print("I am sorry but that is Incorrect :(")
                break

    print()
    
    print("You have successfully finished the quiz")
    print()
    print(f"You have scored {score} / {len(questions)} Which is %{(score/len(questions) * 100):.2f}")
    print()

if __name__ == '__main__':

    test_time()




   


            


















    
    





    








