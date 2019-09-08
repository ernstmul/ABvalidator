from __future__ import print_function, unicode_literals
from PyInquirer import prompt

from ABvalidator.outputUtil import print_description

def determine_user():

    print_description("In order to ask questions better suited to your needs we first like to know from what perspective you are using ABvalidator.\nAre you an experimenter looking to validate the results of an A/B test you conducted? Or are you an experiment platform maintainer looking to validate your A/B test platform?")
    
    questions = [
        {
            'type': 'list',
            'name': 'user_type',
            'message': 'Please select from what perspective you want to user ABvalidator',
            'choices': [
                'Experimenter',
                'Maintainer'
            ]
        }
    ]
    answers = prompt(questions)

    return answers['user_type'] == 'Experimenter'