from colorama import Fore, Style, init

init() #for colorama

def print_description(description,colour=Fore.CYAN,spacing=True):
    if spacing:
        print("\n")
    print(colour + description)
    print(Style.RESET_ALL)

def print_correct_answer(question):
	line = "[" + Fore.GREEN + "V" + Style.RESET_ALL + "] " + question['message']
	print(line)

def print_wrong_answer(question):
	line = "[" + Fore.RED + "X" + Style.RESET_ALL + "] " + question['message']	
	print(line)
	print("    " + Fore.CYAN + "For more information go to: " + question['more_info'] + Style.RESET_ALL + "\n")


def print_line(message):
	print(Style.RESET_ALL + message)

def print_correct_line(message):
	line = "[" + Fore.GREEN + "V" + Style.RESET_ALL + "] " + message
	print(line)

def print_wrong_line(message):
	line = "[" + Fore.RED + "X" + Style.RESET_ALL + "] " + message	
	print(line)	