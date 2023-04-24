
#=====importing libraries===========
'''This is the section where you will import libraries'''
from datetime import date 
import datetime
import os

#=====importing libraries===========
os.chdir("C:\\Users\\nazza\\Documents\\Nazmus\\HyperionDev\\Capstone 3")        #Use to change working directory (so tasks.txt and user.txt files are correctly detected)
#print (os.getcwd())            #Uncomment to check your working directory

#=====functions=====

def reg_user():
    valid_username = False  #check is false by default
    if(username == "admin"):        #only allow register user if admin
        while valid_username == False:
            new_username = input("Please enter new username: ")     #get new username
            with open ("user.txt", "r") as f:
                for line in f:                          #check through each line in "user.txt"
                    split_line = line.split(",")        #convert to list
                    if new_username == split_line[0]:      #compare username element in list with new username
                        valid_username = False          #If match is found, set "valid_username" to false and break loop
                        break
                    else:
                        valid_username = True           #If it does not match, set to True and loop through remaining lines
            if valid_username == False:
                print("That username is taken. Please try again!\n")    #error message if username taken
                    
        #only runs once above loop is complete ("valid_username = True")
        #get new password
        new_password = input("Please enter new password: ")
        confirm_password = input("Please confirm password: ")   #password match check
        if (confirm_password == new_password):
            with open ("user.txt", "a") as f:
                f.write(("\n") + (new_username) + (", ") + (new_password))     #add new user if passwords match
        else:
            print("Error - passwords do not match")             #If passwords do not match
    else:
        print("You do not have the correct permissions.\n")     #if not admin user redirect

def add_task():
         #get task details from user
        assigned_user = input("Please enter username to assign task to: ")
        task_title = input("Please enter the title of task: ")
        task_description = input("Please describe the task: ")
        due_date = input("Please enter the due date of the task: ")

        with open ("tasks.txt", "a") as f:
            f.write (f"\n{assigned_user}, {task_title}, {task_description}, {date.today()}, {due_date}, No")    #add task details to file in correct order

def view_all():
    with open ("tasks.txt", "r") as f:
        #Read each line in tasks file, print out with formatting
        for line in f:                      
            split_line = line.split(", ")
            print(f'''
            Task:\t{split_line[1]}
            Assigned to:\t{split_line[0]}
            Date Asssigned:\t{split_line[3]}
            Due Date:\t{split_line[-2]}
            Task Complete?:\t{split_line[-1]}
            Task Description:
            {split_line[2]}
            _________________________________''')

def view_mine():
    with open ("tasks.txt", "r") as f:
        line_counter = 0
        #read the tasks file
        for line in f:
            line_counter += 1
            split_line = line.split(", ")
            #Only print the task which matches the username
            if(username == split_line[0]): 
                #print task with proper formatting 
                print(f'''
            Task Number:\t{line_counter}                             
            Task:\t{split_line[1]}
            Assigned to:\t{split_line[0]}
            Date Asssigned:\t{split_line[3]}
            Due Date:\t{split_line[-2]}
            Task Complete?:\t{split_line[-1]}
            Task Description:
            {split_line[2]}
            _________________________________''')
        
        #get task select input
        task_select = int(input("Please select a task (by number): "))
        if (task_select != -1):             #call "task_select function" with the task number parameter unless input is -1
            task_selector(task_select)
        else:
            print("Returning back to menu\n")

#task selector function
def task_selector (task_select):
    #read contents of file before changes into a list ("lines")
    with open ("tasks.txt", "r") as f:
        lines = f.readlines()
    #Get the line of the selected task as a string and split the selected string into a list
    selected_line = lines[task_select-1].strip().split(", ")    #index starts at 0
    #Check if task complete --> exit if so
    if selected_line[-1] == "Yes":
        print("This task is already complete.\n")
        return      #end function

    #continue if task not complete --> open file for (over)writing
    with open ("tasks.txt", "w+") as f:
        task_action = input("Would you like to mark task as complete (mark) or edit task (edit)? ")     #user selects specific change to make
        #Mark a task as complete
        if task_action.lower() == "mark":  
            selected_line[-1] = "Yes\n"                       #Change the list to "Yes" in the "completed" field
            #Convert the list back into a string and assign it to the "lines" list at the same index (replacing the original string)
            selected_line_string = ", ".join(selected_line)
            lines[task_select-1] = selected_line_string         

        #Edit a task
        elif task_action.lower() == "edit":
            edit_action = input("Would you like to change user (user) or due date (due date)?") #Get type of edit
            #Change user
            if edit_action.lower() == "user":
                new_user = input("Who would you like to assign this task to?")  #get new user
                selected_line[0] = new_user                                     #assign new user to "selected_line" list
            #Change due date
            elif edit_action.lower() == "due date":
                due_date = input("Enter the new due date: ")      #get new due date
                selected_line[-2] = due_date                      #assign new due date to "selected_line" list

        #Once a task has been edited in "selected_line" list, convert it back into a string and assign it to the original "lines" list  
        selected_line_string = ", ".join(selected_line)
        lines[task_select-1] = selected_line_string
        #Write the updated "lines" list in output.txt 
        f.writelines (lines) 
        print(f"Task {task_select} updated")

def view_statistics():
    if is_report_generated == False:        #Check if reports has been generated
        gen_reports()                        #Run function to check reports if false
    
    #Open and print "task overview" report (with formatting)
    with open ("task_overview.txt","r") as t:       
        print(f"Task Overview:\n{t.read()}\n")
    #Open and print "user overview" report (with formatting)
    with open("user_overview.txt","r") as u:
        print(f"User Overview:\n{u.read()}\n")


def date_convert(task):
    #Convert the due date string (in task list) to a datetime object depending on formatting
    #.find returns -1 if character not found
    if task[-2].find("/") != -1:            
        due_date = datetime.datetime.strptime(task[-2], "%d/%m/%y") #if "/" char found date is in dd/mm/yy format
    elif task[-2].find(".") != -1:
        due_date = datetime.datetime.strptime(task[-2],"%d.%m.%y")  #if "." char found date is in dd.mm.yy format
    else:
        due_date = datetime.datetime.strptime(task[-2],"%d %b %Y")  #otherwise date is in dd mmm yyyy format

    return due_date     #return the due date as a datetime object

def user_overview():
    username_list = []              #create empty username list
    is_summary_written = False      #variable to keep track if top level user/task summary written to user_overview.txt yet
    
    with open ("user.txt","r") as f:
        total_number_users = len(f.readlines()) #Number of lines in user.txt = number of users
        f.seek(0)                               #Reset cursor position to beginning for loop below
        for line in f:
            #Get each username in each line by converting into list and appending first element of the list to "username_list"
            user_info = line.strip().split(", ")
            username_list.append(user_info[0])          
    #This section to read the tasks data for each user
    with open ("tasks.txt","r") as f:
        number_of_tasks = len(f.readlines())    #Get number of tasks
        f.seek(0)                               #reset cursor position for next loop
        for user in username_list:              #step through each username 
            #reset counter variables to 0 for new username
            uncompleted_tasks = 0
            completed_tasks = 0
            overdue_tasks = 0
            f.seek(0)                       #reset seek position
            for line in f:
                task = line.strip().split(", ")
                if(user == task[0]):                #compare the username of each task with the selected user in "username_list"
                    if (task[-1] == "No"):
                        #iterate counter for incomplete task and check date to see if overdue
                        uncompleted_tasks += 1      
                        due_date = date_convert(task)       #call date convert function to return datetime object (to allow to be compared to today's date)
                        if (date.today()>due_date.date()):
                            overdue_tasks += 1              #check if overdue and iterate variable
                    elif (task[-1] == "Yes"):
                        completed_tasks += 1                #else iterate "completed_tasks" variable

            #Work out percentages
            if (completed_tasks + uncompleted_tasks > 0):
                uncompleted_percentage = (uncompleted_tasks / (completed_tasks + uncompleted_tasks)) *100
                completed_percentage = (completed_tasks / (completed_tasks + uncompleted_tasks)) *100
                overdue_percentage = (overdue_tasks / (completed_tasks + uncompleted_tasks)) *100
            else:
                #default percentages to avoid divisionbyzero error
                uncompleted_percentage = 0
                completed_percentage = 0
                overdue_percentage = 0
            #Write summary lines only once (and clear file)
            if is_summary_written == False:
                with open ("user_overview.txt","w+") as o:
                    o.write(f"Users: {total_number_users}\nTasks: {number_of_tasks}")
                    is_summary_written = True
            #Write info for each user with formatting
            with open ("user_overview.txt", "a+") as o:
                o.write(f'''
For User: {user}
\tTasks: {uncompleted_tasks + completed_tasks}
\tPercentage of tasks: {((uncompleted_tasks + completed_tasks)/number_of_tasks)*100}
\tPercentage of assigned tasks completed: {completed_percentage}
\tPercentage of assigned tasks uncompleted: {uncompleted_percentage}
\tPercentage overdue: {overdue_percentage}
-----------------------------------------------------------''')

def task_overview():
    #reset counter variables
    uncompleted_tasks = 0
    completed_tasks = 0
    overdue_tasks = 0

    with open ("user.txt","r") as f:
        total_number_users = len(f.readlines())   #number of users = lines in "users.txt"
   
    with open ("tasks.txt","r+") as f:
        number_of_tasks = len(f.readlines())    #number of tasks = lines in "tasks.txt"
        f.seek(0)                               #reset cursor position for below loop
        for line in f:
            #Check if line is complete or not --> iterate appropriate counter variable
            task = line.strip().split(", ")  
            if (task[-1] == "No"):      
                uncompleted_tasks += 1
            if (task[-1] == "Yes"):
                completed_tasks += 1

            #Converting dates into date-time objects
            due_date = date_convert(task)

            #Overdue tasks
            if (date.today()>due_date.date()):
                overdue_tasks += 1
    #Write tasks info with proper formatting     
    with open ("task_overview.txt", "w+") as o:
        o.write(f'''
Users: {total_number_users}
Tasks: {number_of_tasks}
Tasks completed: {completed_tasks}
Tasks uncompleted: {uncompleted_tasks}
Overdue tasks: {overdue_tasks}''')


def gen_reports():
    #User overview
    user_overview()
    #Task Overview  
    task_overview()
    is_report_generated = True      #set to true to track that reports have been generated

#Global variable to check if reports have been generated (set to false by default)
is_report_generated = False

#====Login Section====
#Variables to check if user is registered, and credentials are correct set to false by default
is_registered_user = False
username_correct = False
password_correct = False


while is_registered_user == False:              #Ask for username/password until registered_user is true
    username = input("Please enter username: ") #Get username/password from user
    password = input("Please enter password: ")
    username_correct = False                    #Reset username_correct variable to false (useful if asking for new credentials after failed login)
    #Read user.txt to check credentials
    with open ("user.txt","r") as f:
        for line in f:                                  #check each line in user.txt
            user_info = line.strip("\n").split(", ")    #strip '\n' characters from line and split line by ", " to get seperate username and password elements
            if (user_info[0]) == (username):        
                username_correct = True         #if username matches set username_correct = true and check if password
                if(user_info[1]) == (password):   
                    password_correct = True     #if password also matches, set password_correct = true and set is_registered = true
                    is_registered_user = True
                    break                       #Once correct credentials matched, break for loop
        
        #Message to be printed depending on if login succesful or what credentials were wrong
        if (username_correct) and (password_correct == False):
            print("Incorrect password")
        if(username_correct == False):
            print("Incorrect username")
        if (username_correct) and (password_correct):
            print("Login successful")
        
                       
while is_registered_user:
    #presenting the menu to the user and 
    #making sure that the user input is converted to lower case.
    if (username == "admin"):                                           #Display admin menu
        menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
s - statistics
gr - generate reports
e - Exit
: ''').lower()
    else:                                                              #else display normal menu
        menu = input('''Select one of the following Options below:      
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
e - Exit
: ''').lower()      

    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()        
    elif menu == 'vm':
        view_mine()
    elif menu == 's':
        view_statistics()
    elif menu == "gr":
        gen_reports()
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")
