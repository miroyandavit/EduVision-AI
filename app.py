import os
import json
import openai
from flask import Flask, request, jsonify, render_template

from Instructions.instructions_applied_math import *
from Instructions.instructions_review_math import *
from Instructions.instructions_code_feedback import *

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
from utils import generate, translate_fields_arm_to_eng, translate_text_arm_to_eng, translate_text_eng_to_arm


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/applied_math/<language>')
def render_applied_math(language):
    if language == 'english':
        return render_template('applied_math_english.html')
    elif language == 'armenian':
        return render_template('applied_math_armenian.html')
    

    
@app.route('/review_problem/<language>')
def render_review_problem(language):
    if language == 'english':
        return render_template('review_problem_english.html')
    elif language == 'armenian':
        return render_template('review_problem_armenian.html')
    
    
    
@app.route('/error_feeback/<language>')
def render_error_feedback(language):
    if language == 'english':
        return render_template('error_feedback_english.html')
    elif language == 'armenian':
        return render_template('error_feedback_armenian.html')
    

# Applied Math Problem Generator Methods
@app.route('/generate_applied_problem/<language>', methods=['POST'])
def generate_applied_problem(language):
    data = request.json
    chapter_content = data.get('chapterContent')
    application_area = data.get('applicationArea')
    if(language=="armenian"):
        chapter_content, application_area = translate_fields_arm_to_eng(chapter_content, application_area)
    try:
        user_prompt=f"Please create an applied math problem in the context of {application_area} based on the following learning outcomes:\n\n{chapter_content}"
        generated_problem = generate(messages=[
            {"role": "system", "content": AM_generate_problem_system_inst},
            {"role": "user", "content": user_prompt}
        ])
        if(language=="armenian"):
            generated_problem = translate_text_eng_to_arm(generated_problem)
        return jsonify({'answer': generated_problem})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/change_applied_problem/<language>', methods=['POST'])
def change_applied_problem(language):
    data = request.json
    chapter_content = data.get('chapterContent')
    application_area = data.get('applicationArea')
    curr_problem = data.get('currentProblem')
    user_instructions = data.get('instruction')
    if language == "armenian":
        chapter_content, application_area = translate_fields_arm_to_eng(chapter_content, application_area)
        curr_problem = translate_text_arm_to_eng(curr_problem)
        user_instructions = translate_text_arm_to_eng(user_instructions)
    try:
        user_prompt = f"""
        Applied math problem:\n{curr_problem}\n\nThe above mathematics problem was created in the context of {application_area} based on the following mathematical concepts:\n\n{chapter_content}.
        Change the problem based on the following user instructions:\n\n{user_instructions}
        """
        changed_problem = generate(messages=[
            {"role": "system", "content": AM_change_problem_system_inst},
            {"role": "user", "content": user_prompt}
        ])
        if language == "armenian":
            changed_problem = translate_text_eng_to_arm(changed_problem)
        return jsonify({'answer': changed_problem})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/generate_applied_solution/<language>', methods=['POST'])
def generate_applied_solution(language):
    data = request.json
    currProblem = data.get('problem')
    if language == "armenian":
        currProblem = translate_text_arm_to_eng(currProblem)
    try:
        user_prompt = f"Please create solutions for the following applied math problem: {currProblem}."
        generated_solution = generate(messages=[
            {"role": "system", "content": AM_generate_sol_system_inst},
            {"role": "user", "content": user_prompt}
        ])
        if language == "armenian":
            generated_solution = translate_text_eng_to_arm(generated_solution)
        return jsonify({'answer': generated_solution})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/change_applied_solution/<language>', methods=['POST'])
def change_applied_solution(language):
    data = request.json
    problem = data.get('problem')
    user_instructions = data.get('instruction')
    curr_sol = data.get('currentSolution')
    if language == "armenian":
        problem = translate_text_arm_to_eng(problem)
        user_instructions = translate_text_arm_to_eng(user_instructions)
        curr_sol = translate_text_arm_to_eng(curr_sol)
    try:
        user_prompt = f"""
        Applied math problem:\n{problem}\n\nProblem solutions:\n{curr_sol}.
        Change the solutions based on the following user instructions:\n\n{user_instructions}
        """
        changed_solution = generate(messages=[
            {"role": "system", "content": AM_change_sol_system_inst},
            {"role": "user", "content": user_prompt}
        ])
        if language == "armenian":
            changed_solution = translate_text_eng_to_arm(changed_solution)
        return jsonify({'answer': changed_solution})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500
    

# Review Math Problem Generator Methods
@app.route('/generate_review_problem/<language>', methods=['POST'])
def generate_review_problem(language):
    data = request.json
    example_problem = data.get('exampleProblem')
    mistake = data.get('mistakeDescription')
    if language == "armenian":
        example_problem = translate_text_arm_to_eng(example_problem)
        mistake = translate_text_arm_to_eng(mistake)
    try:
        user_prompt=f"A student has made a mistake while solving the following math problem:\n\n{example_problem}\n\nHere is the mistake:\n\n{mistake}\n\n Identify the weaknesses of the student that resulted in that mistake."
        identified_weakness = generate(messages=[
            {"role": "system", "content": RM_identify_weakness_system_inst},
            {"role": "user", "content": "A student has made a mistake while solving the following math problem :'when p(x) = x^2 -2x -c is divided by (x-r), the remainder is -5. Find the smallest possible value of c' Here is a more specific description of the mistake: 'The student succeded to apply the remainder theorem by plugging r instead of x and equating it to -5 and expressed c in terms of r but failed to find the functions's minimum value.' Identify the weak areas of knowledge that may have resulted in that mistake."},
            {"role": "assistant", "content": "Finding the vertice coordinates of a parabola, visualizing a parabola on the x-y plane, applying the vertex form of the quadratic equation y=a(x-h)^2 + k "},
            {"role": "user", "content": user_prompt}
        ])
        user_prompt=f"Based on the following list of mathematical concepts:\n\n{identified_weakness}\n\n generate a math problem solving which will require the student apply those concepts."
        generated_problem = generate(messages=[
            {"role": "system", "content": RM_generate_problem_system_inst},
            {"role": "user", "content": user_prompt}
        ])
        if language == "armenian":
            generated_problem = translate_text_eng_to_arm(generated_problem)
        return jsonify({'answer': generated_problem})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/change_review_problem/<language>', methods=['POST'])
def change_review_problem(language):
    data = request.json
    mistake_description = data.get('mistakeDescription')
    curr_problem = data.get('currentProblem')
    user_instructions = data.get('instruction')
    try:
        if language == "armenian":
            curr_problem = translate_text_arm_to_eng(curr_problem)
            mistake_description = translate_text_arm_to_eng(mistake_description)
            user_instructions = translate_text_arm_to_eng(user_instructions)
        user_prompt = f"""Math problem for review:\n\n{curr_problem}\n\nThe above mathematics problem is tailored towards improving a student's math skills based the problem and the mistake he/she made in the problem\n\n Problem:\n\n{curr_problem}\n\nMistake description:\n\n{mistake_description}\n\n.
        Change the problem based on the following user instructions:\n\n{user_instructions}."""
        changed_problem = generate(messages=[
            {"role": "system", "content": RM_change_problem_system_inst},
            {"role": "user", "content": user_prompt}
        ])
        if language == "armenian":
            changed_problem = translate_text_eng_to_arm(changed_problem)
        return jsonify({'answer': changed_problem})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/generate_review_solution/<language>', methods=['POST'])
def generate_review_solution(language):
    data = request.json
    curr_problem = data.get('problem')
    try:
        if language == "armenian":
            curr_problem = translate_text_arm_to_eng(curr_problem)
        user_prompt = f"Please create solutions for the math problem: {curr_problem}."
        generated_solution = generate(messages=[
            {"role": "system", "content": RM_generate_sol_system_inst},
            {"role": "user", "content": user_prompt}
        ])
        if language == "armenian":
            generated_solution = translate_text_eng_to_arm(generated_solution)
        return jsonify({'answer': generated_solution})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/change_review_solution/<language>', methods=['POST'])
def change_review_solution(language):
    data = request.json
    problem = data.get('problem')
    user_instructions = data.get('instruction')
    curr_sol = data.get('currentSolution')
    try:
        if language == "armenian":
            problem = translate_text_arm_to_eng(problem)
            user_instructions = translate_text_arm_to_eng(user_instructions)
            curr_sol = translate_text_arm_to_eng(curr_sol)
        user_prompt = f"""
        Math problem:\n{problem}\n\nProblem solutions:\n{curr_sol}\n.
        Change the solutions based on the following user instructions:\n\n{user_instructions}
        """
        changed_solution = generate(messages=[
            {"role": "system", "content": RM_change_sol_system_inst},
            {"role": "user", "content": user_prompt}
        ])
        if language == "armenian":
            changed_solution = translate_text_eng_to_arm(changed_solution)
        return jsonify({'answer': changed_solution})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500


# Generate Feedback Methods
@app.route('/generate_feedback/<language>', methods=['POST'])
def generate_feedback(language):
    data = request.json
    code = data.get('code')
    error_message = data.get('errorMessage')
    try:
        user_prompt = f"""
        Given the code:\n\n{code}\n\n and the error message:\n\n{error_message}\n\n generate a feedback.
        """
        generated_feedback = generate(messages=[
            {"role": "system", "content": code_feedback_system_inst},
            {"role": "user", "content": "Given the code: my_list = [1, 2, 3, 4, 5]  print(my_list[5]) and the error message: IndexError: list index out of range, generate a feedback."},
            {"role": "assistant", "content": "An IndexError happens when you try to access a position in a list that doesn't exist. In this specific case, you're trying to access the item at position 5 in my_list, but the list only has items from positions 0 to 4"},
            {"role": "user", "content": user_prompt}
        ])
        if language == "armenian":
            generated_feedback = translate_text_eng_to_arm(generated_feedback)
        return jsonify({'answer': generated_feedback})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)