from colorama import Fore
import json, sys

from ABvalidator import determine_user, print_description, print_correct_answer, print_wrong_answer, get_questionnaire, run_questions, check_boolean_answers, check_math_answers, filter_questions, srmTest, noveltyTest, detect_outliers

def main():
    #Welcome
    print_description(colour=Fore.GREEN, spacing=False, description="Welcome to ABvalidator. Please read the documentation on github.com/ernstmul/ABvalidator for more info.")

    # determine what questionnaire to ask
    isExperimenter = determine_user()

    # get questionnaire for the user type
    questions = get_questionnaire(isExperimenter)
    if len(sys.argv) > 1:
        questions = filter_questions(questions, sys.argv)
    
    # run questions
    answers = run_questions(questions)

    # check answers
    check_boolean_answers(answers, questions)
    check_math_answers(answers)
    

if __name__ == '__main__':
    main()    