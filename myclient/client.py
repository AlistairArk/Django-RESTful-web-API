import requests

s = requests.Session()  # Create session in which all requests will take place
webAddress = "http://127.0.0.1:8000" # Address of my site / webAPI (not hard-coded for the sake of local testing)
supportedURLs = ["http://127.0.0.1:8000", "sc17jhd.pythonanywhere.com"]
command = []
mainLoop = 1    # used to keep the main loop running until the program terminates

def main():
    global mainLoop, command

    while mainLoop:
        # Get user input - strip it of trailing spaces - split it into it's components
        command = input("Please enter a command: ").strip().split(" ")

        if command[0] == "register" and ArgumentsSupplied(1):
            Register()
        elif command[0] == "login" and ArgumentsSupplied(2):
            Login()
        elif command[0] == "logout" and ArgumentsSupplied(1):
            Logout()
        elif command[0] == "list" and ArgumentsSupplied(1):
            List()
        elif command[0] == "view" and ArgumentsSupplied(1):
            View()
        elif command[0] == "average" and ArgumentsSupplied(3):
            Average()
        elif command[0] == "rate" and ArgumentsSupplied(1):
            Rate()
        elif command[0] == "help" and ArgumentsSupplied(1):
            Help()      # Display a list of commands
        elif command[0] == "exit" and ArgumentsSupplied(1):
            # Exit()      # Terminate the program
            return
        else:
            Invalid()   # The command entered could not be found



def ArgumentsSupplied(requiredArguments):
    '''Check and output messages to notify the user if too many or too few arguments are supplied'''
    suppliedArguments = len(command)
    print(suppliedArguments,requiredArguments,command)
    if requiredArguments==suppliedArguments: # Amount of arguments required and supplied match
        return True
    elif requiredArguments>suppliedArguments:
        print("Too few arguments supplied. Please try again.")
    elif requiredArguments<suppliedArguments:
        print("Too many arguments supplied. Please try again.")




def Help():
    ''' Present a list of available commands to the user'''

    print("\n== Help ==\n")

    print("Register to the service.\n    register\n")
    print("Login to the service.\n    login sc17jhd.pythonanywhere.com\n")
    print("Logout from the current session.\n    logout\n")
    print("View a list of all module instances and the professor(s) teaching each of them.\n    list\n")
    print("View the rating of all professors.\n    view\n")
    print("View the average rating of a certain professor in a certain module\n    average professor_id module_code\n")
    print("Rate the teaching of a certain professor in a certain module instance\n    rate professor_id module_code year semester rating\n")


# def Exit():
#     ''' End the program '''
#     global mainLoop
#     mainLoop = 0
#     return



def Invalid():
    print("\nSorry, the command you entered is invalid.\nPlease type 'help' if you wish to show a list of available commands.\n")



def Register(): # POST (sending account details)
    ''' This is used to allow a user to register to the service using a username, email and a password.
    When the command is invoked, the program prompts the user to enter the username, email, and password
    of the new user.'''

    # notRegistered = 0
    # while notRegistered: # Loop until registration is carried out successfully

    print("\n== Register ==\n")
    username = input("Please enter a username: ")
    password = input("Please enter a password: ")
    email = input("Please enter your email: ")

    payload = { "username": username,
                "password": password,
                "email": email }
    global s
    r = s.get(webAddress + "/api/register", params=payload)
    
    if "\n"+r.text+"\n" == "":
        print("User registered successfully!")
    else:
        print("Your registration request was denied for the following reasons:\n"+"\n"+r.text+"\n")




def Login(): # POST (sending login details)
    '''This command is used to log in to the service.'''

    if (command[1] in supportedURLs):
        print("\n== Login ==\n")
        print("Attempting to login to: " + command[1])
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        payload = { "username": username,
                    "password": password}

        try:
            global s
            r = s.post(command[1] + "/api/login", params=payload)
            print("\n"+r.text+"\n")
        except Exception as e:
            serviceReachError()
    else:
        print("Sorry, the URL you have entered is either unsupported or invalid.")
        print("Consider using the following URL and try again: "+supportedURLs[1])



def serviceReachError():
    print("Sorry, the service you are trying to reach could not be accessed at this time.")
    print("The service may be down, or you may be missing required modules.")



def Logout(): # GET (No payload being sent)
    ''' This causes the user to logout from the current session '''
    global s
    r = s.post(webAddress+"/api/logout")
    print("\n"+r.text+"\n")



def List(): # GET (Getting list of module instances)
    '''This is used to view a list of all module instances and the professor(s) teaching each of them'''
    global s
    r = s.get(webAddress+"/api/list")
    print("\n"+r.text+"\n")



def View(): # GET (Getting list of professor ratings)
    ''' This command is used to view the rating of all professors '''
    global s
    r = s.get(webAddress+"/api/view")
    print("\n"+r.text+"\n")



def Average():
    ''' This command is used to view the average rating of a certain professor in a certain module'''
    payload = { "professorID": command[1],
                "moduleCode": command[2]}

    global s
    r = s.post(webAddress+"/api/average", data=payload)
    print("\n"+r.text+"\n")

    



def Rate(): # POST
    '''This is used to rate the teaching of a certain professor in a certain module instance'''
    payload = { "professorID":  command[1],
                "moduleCode":   command[2],
                "year":         command[3],
                "semester":     command[4],
                "rating":       command[5]}

    global s
    r = s.post(webAddress+"/api/rate", data=payload)
    print("\n"+r.text+"\n")




print("=== Ratings Client Application ===\n")
main() # Run Main Loop
