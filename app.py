from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "surveys"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

responses = []
survey = surveys.satisfaction_survey

@app.route('/')
def homepage(): 
    """Return homepage"""
    title = survey.title
    instructions = survey.instructions

    return render_template("homepage.html", title = title, instructions=instructions)

@app.route('/start')
def start():
    """Create session"""
    session['responses'] = []
    return redirect('/question/0')

@app.route('/question/<int:question_id>')
def question(question_id):
    """Show survey question and answer choices"""
    qId = question_id
    responses = session['responses']
    question_number = len(responses)

    if (question_number == len(survey.questions)):
        return redirect('/confirmation')

    if (question_number != qId):        
        flash("You must access the questions in order!")
        return redirect(f"/question/{question_number}")
    
    question = survey.questions[question_number]
    title = survey.title
    instructions = survey.instructions

    return render_template("question.html", question = question, title = title, instructions=instructions)

@app.route('/answer', methods=["POST", "GET"])
def record_answer():
    """Record answer then redirect to show next question"""
    answer = request.form["answer"]
    responses = session['responses']
    responses.append(answer)
    question_number = len(responses)
    session['responses'] = responses


    if (question_number == len(survey.questions)):
        return redirect('/confirmation')
    else:
        return redirect(f"/question/{question_number}")


@app.route('/confirmation')
def show_confirmation():
    """Show that the survey responses have been saved"""
    return render_template("confirmation.html")

