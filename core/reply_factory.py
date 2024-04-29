
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)
        current_question_id = 0
        session['answers'] = []
        session['score'] = 0

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    if current_question_id < len(PYTHON_QUESTION_LIST):

        next_question, next_question_id = get_next_question(current_question_id)
        bot_responses.append(next_question)
        session["current_question_id"] = next_question_id

    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''

    if current_question_id > 0:
        current_question = PYTHON_QUESTION_LIST[current_question_id - 1]

        session['answers'].append(
            {"question_id": current_question_id, "answer": answer}
        )

        # Validate the answer
        if answer.lower() == current_question['answer'].lower():
            # If the answer is correct, store it in the session
            session['score'] += 1
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question_text = PYTHON_QUESTION_LIST[current_question_id]['question_text']
    next_question_options = PYTHON_QUESTION_LIST[current_question_id]['options']
    next_question = f"{next_question_text}\nOptions:\n{next_question_options}"

    return next_question, current_question_id + 1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    # Calculate the score based on the number of correct answers
    num_correct_answers = session['score']
    total_questions = len(PYTHON_QUESTION_LIST)
    score_percentage = (num_correct_answers / total_questions) * 100

    # Generate the final response message
    final_response = f"Your quiz has been completed.\nYou answered {num_correct_answers} out of {total_questions} questions correctly."
    final_response += f"\nYour score: {score_percentage:.2f}%"

    return final_response
