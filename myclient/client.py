import requests

s = requests.Session()  # Create session in which all requests will take place
supportedURLs = ["sc17jhd.pythonanywhere.com","http://127.0.0.1:8000"]
webAddress = supportedURLs[0] # Address of my site / webAPI (not hard-coded for the sake of local testing)
command = []
mainLoop = 1     # Used to keep the main loop running until the program terminates
wrongArg = 0     # Used in handling which error messages are displayed to the user 
sessionName = "" # Name of the client which is currently logged in

def main():
    global mainLoop, command, wrongArg, sessionName

    while mainLoop:
        wrongArg = 0

        # Get user input - strip it of trailing spaces - split it into it's components
        command = input(sessionName+"Please enter a command: ").strip().split(" ")
        

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
        elif command[0] == "rate" and ArgumentsSupplied(6):
            Rate()
        elif command[0] == "help" and ArgumentsSupplied(1):
            Help()      # Display a list of commands
        elif command[0] == "exit" and ArgumentsSupplied(1):
            # Exit()      # Terminate the program
            return
        elif not wrongArg:
            print("\nSorry, the command you entered was invalid.")
            Invalid()   # The command entered could not be found



def ArgumentsSupplied(requiredArguments):
    '''Check and output messages to notify the user if too many or too few arguments are supplied'''
    global wrongArg
    wrongArg = 1
    suppliedArguments = len(command)

    if requiredArguments==suppliedArguments: # Amount of arguments required and supplied match
        return True
    elif requiredArguments>suppliedArguments:
        print("\nToo few arguments supplied.")
    elif requiredArguments<suppliedArguments:
        print("\nToo many arguments supplied.")

    Invalid()



def Help():
    ''' Present a list of available commands to the user'''

    print("\n\n== Help ==")

    print("Register to the service.\n    register")
    print("Login to the service.\n    login sc17jhd.pythonanywhere.com")
    print("Logout from the current session.\n    logout")
    print("List all module instances and the professor(s) teaching each of them.\n    list")
    print("View the rating of all professors.\n    view")
    print("View the average rating of a certain professor in a certain module\n    average professor_id module_code")
    print("Rate the teaching of a certain professor in a certain module instance\n    rate professor_id module_code year semester rating")
    print("Terminate the program.\n    exit")
    print()

# def Exit():
#     ''' End the program '''
#     global mainLoop
#     mainLoop = 0
#     return



def Invalid():
    print("Please type 'help' if you wish to view a list of available commands.\n")



def Register(): # POST (sending account details)
    ''' This is used to allow a user to register to the service using a username, email and a password.
    When the command is invoked, the program prompts the user to enter the username, email, and password
    of the new user.'''

    # notRegistered = 0
    # while notRegistered: # Loop until registration is carried out successfully

    print("\n\n== Register ==")
    username = input("Please enter a username: ")
    password = input("Please enter a password: ")
    email = input("Please enter your email: ")

    payload = { "username": username,
                "password": password,
                "email": email }
    global s
    r = s.post(webAddress + "/api/register", data=payload)
    
    if r.text == "":
        print("\nUser registered successfully!\n")
    else:
        print("\nYour registration request was denied for the following reasons:\n"+r.text+"\n")




def Login(): # POST (sending login details)
    '''This command is used to log in to the service.'''
    global sessionName

    if (command[1] in supportedURLs):
        print("\n\n== Login ==")
        print("Attempting to login to: " + command[1])
        username = input("Please enter your username: ")
        password = input("Please enter your password: ")
        payload = { "username": username,
                    "password": password}

        try:
            global s
            r = s.post(webAddress + "/api/login", data=payload)
            if r.text==username:
                sessionName = "("+username+") "
                print("\nLogin successful!\n")
            else:
                print("\n"+r.text+"\n")


        except Exception as e:
            serviceReachError()
    else:
        print("\nSorry, the URL you have entered is either unsupported or invalid.")
        print("Consider using the following URL and try again: "+supportedURLs[0]+"\n")



def serviceReachError():
    print("\nSorry, the service you are trying to reach could not be accessed at this time.")
    print("The service may be down, or you may be missing required modules.\n")



def Logout(): # GET (No payload being sent)
    ''' This causes the user to logout from the current session '''
    global s, sessionName
    print("\n\n== Logout ==")

    try:
        sessionName = ""
        r = s.post(webAddress+"/api/logout")
        print(r.text+"\n")

    except Exception as e:
        serviceReachError()





def List(): # GET (Getting list of module instances)
    '''This is used to view a list of all module instances and the professor(s) teaching each of them'''
    global s
    print("\n\n== List ==")

    try:
        r = s.get(webAddress+"/api/list")
        print(r.text+"\n")

    except Exception as e:
        serviceReachError()


def View(): # GET (Getting list of professor ratings)
    ''' This command is used to view the rating of all professors '''
    global s
    print("\n\n== View ==")

    try:
        r = s.get(webAddress+"/api/view")
        print(r.text+"\n")
    
    except Exception as e:
        serviceReachError()



def Average():
    ''' This command is used to view the average rating of a certain professor in a certain module'''
    global s
    print("\n\n== Average ==")

    try:
        payload = { "professorID": command[1],
                    "moduleCode": command[2]}

        r = s.post(webAddress+"/api/average", data=payload)
        print(r.text+"\n")

    except Exception as e:
        serviceReachError()




def Rate(): # POST
    '''This is used to rate the teaching of a certain professor in a certain module instance'''
    global s
    print("\n\n== Rate ==")

    try:
        payload = { "professorID":  command[1],
                    "moduleCode":   command[2],
                    "year":         command[3],
                    "semester":     command[4],
                    "rating":       command[5]}

        r = s.post(webAddress+"/api/rate", data=payload)
        print(r.text+"\n")

    except Exception as e:
        serviceReachError()



print("=== Ratings Client Application ===\n")
main() # Run Main Loop

