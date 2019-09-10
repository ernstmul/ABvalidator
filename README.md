# ABvalidator

ABvalidator is a python tool that helps to validate A/B experiments, and experiment platforms used to conduct A/B tests in a continuous experimentation environment.


## Installation and usage
Currently the package is not yet available through pip. Until that moment you can download a copy of this repository, and run the following command in your terminal from the main folder of the project:

    python setup.py build; python setup.py install; clear; python ABvalidator

 ### Arguments
 By using the following arguments you can skip to specific calculation questions:

Skip to the question about randomisation:

    --randomisation 

Skip to the question about Sample Ratio Mismatch:

    --srm 

Skip to the question about the Novelty Effect:

    --novelty 

Skip to the question about the skewed data:

    --skewed_data

 

Skip to the question about the minimum number of participants:

    --statistics 


### Structure of CSV files
Since the additional information pages are currently not yet available per question, the anticipated structure of the CSV files in some questions is explained here.

For the Sample Ratio Mismatch question the first column is expected to contain the vistor numbers of each variant, and the second column is expected to have the percentage of users that should be directed to this variant. 
For example:

    100,0.25
    100,0.25
    70,0.25
    100,0.25

For all other CSV questions the current format is the following. Each row contains the metric information of a variant, with the first cell being the name of that variant.
For example:

    variant 1,2,1,1,4,2,2.2,1.8,2
    variant 2,15,10,34,18,26,18,19,20
