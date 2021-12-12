from flask import Flask, request, render_template, redirect, flash
# from flask_debugtoolbar import DebugToolbarExtension
import surveys

app = Flask(__name__)
# app.config['SECRET_KEY'] = "surveys"

# debug = DebugToolbarExtension(app)

responses = []
survey = surveys.satisfaction_survey
question_number = len(responses)

@app.route('/')
def homepage(): 
    """Return homepage"""
    title = survey.title
    instructions = survey.instructions
    response_list = responses
    return render_template("homepage.html", title = title, instructions=instructions, responses=response_list)

@app.route('/question/<question_number>')
def question(question_number):
    """Show survey question and answer choices"""
    question_number = len(responses)

    if (question_number == len(survey.questions)):
        return redirect('/confirmation')

    if (question_number != len(responses)):
        flash("You must access the questions in order!")
        return redirect(f"/question/{question_number}")
    
    question = survey.questions[int(question_number)]
    title = survey.title
    instructions = survey.instructions

    return render_template("question.html", question = question, title = title, instructions=instructions)

@app.route('/answer', methods=["POST"])
def record_answer():
    """Record answer then redirect to show next question"""
    answer = request.form["answer"]
    responses.append(answer)
    question_number = len(responses)

    if (question_number == len(survey.questions)):
        return redirect('/confirmation')
    else:
        return redirect(f"/question/{question_number}")


@app.route('/confirmation')
def show_confirmation():
    """Show that the survey responses have been saved"""
    return render_template("confirmation.html")

