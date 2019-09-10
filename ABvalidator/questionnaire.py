import json, os
import regex

from PyInquirer import prompt, Validator, ValidationError

from ABvalidator.outputUtil import print_description, print_correct_answer, print_wrong_answer, print_line, print_correct_line, print_wrong_line
from ABvalidator.formulas import isRatioSignificantlyCorrect, srmTest, noveltyTest, detect_outliers, calculateMinimalSampleSize, calculateStdViaBootstrapMethod

import pandas as pd

class NumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^[0-9]*(\.)?[0-9]*$', document.text)
        if not ok or document.text is '':
            raise ValidationError(
                message='Please enter a valid number',
                cursor_position=len(document.text))  # Move cursor to end

class PathValidator(Validator):
    def validate(self, document):
        filename = document.text
        if not os.path.isfile(filename) and filename is not '':
            raise ValidationError(
                message='No file found in location: ' + filename + " (leave empty to skip question)",
                cursor_position=len(document.text))  # Move cursor to end            

def get_questionnaire(isExperimenter):
    
    HERE = os.path.abspath(os.path.dirname(__file__))

    if isExperimenter:
        file_name = HERE + "/./data/questions_experimenter.json"
    else:
        file_name = HERE + "/./data/questions_maintainer.json"

    with open(file_name) as json_file:
        data = json.load(json_file)
        return data['questions'] 

def filter_questions(questions, argv):

    filters = []

    if "--randomisation" in argv:
        filters += ['randomisation_user_count', 'randomisation_user_variant', 'randomisation_user_division']

    if "--srm" in argv:
        filters += ['data_quality']

    if "--novelty" in argv:
        filters += ['novelty_effect']    

    if "--skewed_data" in argv:
        filters += ['skewed_data'] 

    if "--statistics" in argv:
        filters += ['statistics_std', 'statistics_sensitivity', 'statistics_path']     

    if len(filters) == 0:
        return questions

    filtered_questions = []
    for question in questions:
        if question['name'] in filters:
            filtered_questions.append(question)

    return filtered_questions    


def run_questions(questions):
    answers = {}

    # Ask all questions
    for question in questions:

        # check if the questions has prerequisites from previous questions
        canAsk = True
        if len(question['requires']) > 0:
            for prereq in question['requires']:
                if answers[prereq] == False:
                    canAsk = False
                    break

        if canAsk:
            if question['context'] is not None:
                print_description(question['context'])
            
            #restructure the questionObject to lose keys that PyInquirer otherwise does not like
            questionObject = {"type" : question['type'], "name" : question['name'], "message" : question['message']}
            if 'validator' in question:
                if question['validator'] == 'NumberValidator':
                    questionObject['validate'] = NumberValidator
                elif question['validator'] == 'PathValidator':
                    questionObject['validate'] = PathValidator

            answer = prompt(questionObject)

            if question['name'] in answer:
                answers[question['name']] = answer[question['name']]

    return answers        
        

def check_boolean_answers(answers, questions):

    for question in questions:
        if question['type'] == 'confirm':
            if question['name'] in answers:
                if answers[question['name']]:
                    print_correct_answer(question)
                else:
                    print_wrong_answer(question) 

def check_math_answers(answers):
    # used thresholds for several calculations
    thresholds = [0.05, 0.01, 0.001]

    #check randomisation question
    if (
        'randomisation_user_count' in answers and 
        'randomisation_user_variant' in answers and 
        'randomisation_user_division' in answers
        ):
            print_line("Checking randomisation:")

            for threshold in thresholds:
                correct, lower_bound, upper_bound = isRatioSignificantlyCorrect(int(answers['randomisation_user_variant']), int(answers['randomisation_user_count']), float(answers['randomisation_user_division']), threshold)
                if correct:
                    print_correct_line("Randomisation sufficient for threshold {}".format(threshold))
                else:
                    print_wrong_line("Randomisation insufficient for {}, lower bound is: {}, upper bound is: {}, but variant count is: {}".format(threshold, lower_bound, upper_bound, answers['randomisation_user_variant']))    

    #SRM
    if 'data_quality' in answers:
        print_line("Checking SRM")

        #load csv into Pandas      
        df_quality = pd.read_csv(answers['data_quality'], header=None)        

        #confirm two columns exist
        if 0 not in df_quality or 1 not in df_quality:
            print_wrong_line("Data quality CSV missing columns.")
        else:
        
            #confirm the percentages add to 100%
            if df_quality[1].sum() != 1:
                print_wrong_line("Data quality variant percentages (2nd column) don't add up to 1 (100%). It currently sums to: {}".format(df_quality[1].sum()))
            else:
                p = srmTest(df_quality)

                for threshold in thresholds:
                    if p < threshold:
                        print_wrong_line("SRM found for threshold {} (p value is {})".format(threshold, p))
                    else:
                        print_correct_line("No SRM found for threshold {}".format(threshold))    
    
    #Novelty effect
    if 'novelty_effect' in answers:
        print_line("Checking Novelty effect")

        #load csv into Pands
        df_novelty = pd.read_csv(answers['novelty_effect'], header=None)

        #every row is a variant, check every variant
        for index, row in df_novelty.iterrows():
            variant_list = row.tolist()
            variant_name = variant_list[0]
            variant_list.pop(0) #pop the name of the list

            if not noveltyTest(variant_list):
                print_correct_line("No sign of novelty effect detected in variant '{}'".format(variant_name))
            else:
                print_wrong_line("Signs of novelty effect detected in variant '{}'".format(variant_name))   

    # Skewed data
    if 'skewed_data' in answers:
        print_line("Checking skewed data")

        #load csv into Pands
        df_novelty = pd.read_csv(answers['skewed_data'], header=None)

        #every row is a variant, check every variant
        for index, row in df_novelty.iterrows():
            variant_list = row.tolist()
            variant_name = variant_list[0]
            variant_list.pop(0) #pop the name of the list

            outliers = detect_outliers(variant_list)

            if len(outliers) > 0:
                print_wrong_line("The following outliers are found in variant '{}': {}".format(variant_name, outliers))   
            else:
                print_correct_line("No outliers found in variant '{}'".format(variant_name))   

    #Statistics
    if (
        'statistics_std' in answers and 
        'statistics_sensitivity' in answers and 
        'statistics_path' in answers
        ):  
        print_line("Checking statistics")

        #load csv into Pands
        df_statistics = pd.read_csv(answers['statistics_path'], header=None)

        #every row is a variant, check every variant
        for index, row in df_statistics.iterrows():
            variant_list = row.tolist()
            variant_name = variant_list[0]
            variant_list.pop(0) #pop the name of the list

            std = calculateStdViaBootstrapMethod(variant_list) if (int(answers['statistics_std']) == 0) else float(answers['statistics_std'])
            sample_size = calculateMinimalSampleSize(std, float(answers['statistics_sensitivity']), variant_list)
            
            print_line("For variant '{}' the minimum number of required participants is {}".format(variant_name, sample_size));


            


