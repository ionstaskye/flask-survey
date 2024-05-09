from flask import Flask, request , render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "Secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
RESPONSES_KEYS = "responses"

survey = satisfaction_survey
@app.route("/")
def get_home_page():
    title = survey.title
    instructions = survey.instructions
    return render_template("survey_home.html",title= title, instructions= instructions )

@app.route("/begin", methods = ["POST"])
def begin_survey():

    session[RESPONSES_KEYS] = []

    return redirect("/questions/0")

@app.route("/questions/<int:question>")
def show_question(question):
    current_responses = session.get(RESPONSES_KEYS)
    question = len(current_responses)
    current_question = survey.questions[question]
    if question == len(survey.questions):
            return redirect("/completed")
    if question != question:
        flash("Not currently on that question!")
        return redirect (f"/questions/{len(current_responses)}")
    else:
        return render_template("Question.html", question = current_question, question_number = question)

@app.route("/answer", methods= ['POST'])
def submit_answer():

    survey_answer = request.form['answer']
    answers = session[RESPONSES_KEYS]
    answers.append(survey_answer)
    session[RESPONSES_KEYS] = answers

    if len(answers) == len(survey.questions):
        return redirect("/completed")
    else:
        return redirect(f"/questions/{len(answers)}")

@app.route("/completed")
def thank_you():
    return render_template("/thank_you.html")

