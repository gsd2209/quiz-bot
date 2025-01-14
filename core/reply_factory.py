
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to the session.
    '''
    # Perform basic validation (for example, non-empty answer)
    if not answer or len(answer.strip()) == 0:
        return False, "Answer cannot be empty."

    # Assuming answers are stored in a session dictionary
    if 'answers' not in session:
        session['answers'] = {}

    session['answers'][current_question_id] = answer
    session.save()  # Save session data to persistent storage
    
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question based on the current_question_id.
    '''
    try:
        next_question_id = current_question_id + 1
        if next_question_id < len(PYTHON_QUESTION_LIST):
            next_question = PYTHON_QUESTION_LIST[next_question_id]
            return next_question, next_question_id
        else:
            return None, -1  # No more questions left
    except Exception as e:
        return None, -1  # Handle any error



def generate_final_response(session):
    '''
    Generates a final result message, including the score based on the answers.
    '''
    # Calculate score based on the user's answers
    correct_answers = 0
    total_questions = len(PYTHON_QUESTION_LIST)
    
    for question_id, user_answer in session.get('answers', {}).items():
        # Compare user answer with the correct answer (assuming we have a way to fetch correct answers)
        correct_answer = PYTHON_QUESTION_LIST[question_id].get('correct_answer')
        if user_answer.strip().lower() == correct_answer.strip().lower():
            correct_answers += 1
    
    # Create the result message
    result_message = f"Quiz Completed! You scored {correct_answers} out of {total_questions}."
    
    return result_message
