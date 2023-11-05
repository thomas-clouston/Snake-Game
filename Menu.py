# Imports
from tkinter import *
from tkinter import messagebox
import xml.etree.ElementTree as ET
import os


# Sign up setup
signup_window = Tk()
signup_window.configure(background="Light Blue")


# Login window
def login():
    # Login setup
    signup_window.destroy()
    login_window = Tk()
    login_window.configure(background="Light Blue")

    # Menu window
    def menu():
        global user
        # Menu setup
        menu_window = Tk()
        menu_window.configure(background="Light Blue")

        # Quit
        def exit():
            menu_window.destroy()
            quit()

        # Play
        def play():
            menu_window.destroy()
            os.system('Game.py')
            menu()

        # Leaderboard
        def leaderboard():
            leaderboard_window = Tk()
            leaderboard_window.configure(background="Light Blue")

            # XML file to string concentration
            tree = ET.parse("Data.xml")
            root = tree.getroot()

            score_text = ""
            count = 0
            scores = []

            # Finding users and their high scores
            for user_search in root:
                username = user_search.text
                score = user_search.find('Score')
                score = score.text
                scores.append(int(score))
                scores.append(username)

            # Sorting high scores

            # Defines smallest item index value
            for iteration_1 in range(0, len(scores), 2):
                smallest = iteration_1

                # Compares current smallest to rest of array
                for iteration_2 in range(iteration_1 + 2, len(scores), 2):

                    # Defines new smallest item index value
                    if scores[iteration_2] < scores[smallest]:
                        smallest = iteration_2

                # Swap new smallest value with current value
                scores[smallest], scores[iteration_1], scores[smallest + 1], scores[iteration_1 + 1] = scores[
                    iteration_1], scores[
                    smallest], scores[iteration_1 + 1], scores[smallest + 1]

            # Reverse score list from largest to smallest
            scores.reverse()

            # String concentration
            for iteration in range(0, len(scores), 2):
                count += 1
                score_text = f"{score_text} {str(count)}. {scores[iteration]}: {str(scores[iteration+1])} \n"

            # Objects
            lblTitle = Label(leaderboard_window, text='Leader Board', fg='Dark Blue', font=('Arial Black', 24), bg='Light Blue')
            lblLeaderboard = Label(leaderboard_window, text=score_text, fg='Yellow', font=('Arial Black', 12), bg='Light Blue')

            lblTitle.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
            lblLeaderboard.grid(row=1, column=0, columnspan=3)

        # Finding user's high score
        high_score = user.find('Score')
        high_score = f"High Score: {high_score.text}"

        # Creating objects

        # Labels
        lblTitle = Label(menu_window, text='Main Menu', fg='Dark Blue', font=('Arial Black', 24), bg='Light Blue')
        lblScore = Label(menu_window, text=high_score, fg='Yellow', font=('Arial Black', 12), bg='Light Blue')

        # Buttons
        btnPlay = Button(menu_window, text='Play', command=play, fg='Green', font=('Arial Black', 12), bg='Light Blue')
        btnExit = Button(menu_window, text='Exit', command=exit, fg='Red', font=('Arial Black', 12), bg='Light Blue')
        btnLeader = Button(menu_window, text='Leader Board', command=leaderboard, fg='Blue', font=('Arial Black', 12), bg='Light Blue')

        # Placing objects
        lblTitle.grid(row=0, column=1, padx=10, pady=10)
        lblScore.grid(row=2, column=2)
        btnPlay.grid(row=2, column=1, pady=5)
        btnExit.grid(row=3, column=1, pady=5)
        btnLeader.grid(row=2, column=0, columnspan=1, padx=5)

        menu_window.mainloop()

    # Creating objects

    # Creating labels
    lblTitle = Label(login_window, text='Login', fg='Dark Blue', font=('Arial Black', 24), bg='Light Blue')
    lblUser = Label(login_window, text='Username', font=('Arial', 16), bg='Light Blue')
    lblPass = Label(login_window, text='Password', font=('Arial', 16), bg='Light Blue')

    # Creating entries
    entUsername = Entry(login_window, font=('Arial', 12))
    entPassword = Entry(login_window, font=('Arial', 12))

    # Validate login credentials
    def login_validation():
        global user
        # Getting entries
        username = entUsername.get()
        password = entPassword.get()

        tree = ET.parse("Data.xml")
        root = tree.getroot()

        # Existence check
        if username == '' or password == '':
            messagebox.showerror('Existence check', 'Please fill in missing information')
        else:
            # Validating user
            for user in root:
                if user.text == username:
                    found = True
                    break
                else:
                    found = False

            if found is False:
                messagebox.showerror('Validation check', 'Username does not exist')
            else:
                # Validating password
                passCheck = user.find('Password')

                # Login success
                if password == passCheck.text:
                    # Write username to temp file for game to access
                    file = open("temp.txt", "w")
                    file.write(username)
                    file.close()

                    login_window.destroy()
                    menu()

                else:
                    messagebox.showerror('Validation check', 'Incorrect password')

    # Buttons
    btnValidation = Button(login_window, text="Login", command=login_validation, fg='Dark Blue', bg='Light Blue', font=("Arial Black", 12))

    # Placing Objects
    lblTitle.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
    lblUser.grid(row=1, column=0, padx=5, pady=5)
    lblPass.grid(row=2, column=0, padx=5, pady=5)

    entUsername.grid(row=1, column=1, padx=5)
    entPassword.grid(row=2, column=1, padx=5)

    btnValidation.grid(row=4, column=0, columnspan=3)


# Creating objects

# Creating labels
lblTitle = Label(signup_window, text='Sign Up', fg='Dark Blue', font=('Arial Black', 24), bg='Light Blue')
lblUser = Label(signup_window, text='Username', font=('Arial', 16), bg='Light Blue')
lblPass = Label(signup_window, text='Password', font=('Arial', 16), bg='Light Blue')
lblConfirm = Label(signup_window, text='Confirm Password', font=('Arial', 16), bg='Light Blue')

# Creating entries
entUsername = Entry(signup_window, font=('Arial', 12))
entPassword = Entry(signup_window, font=('Arial', 12))
entCfmPassword = Entry(signup_window, font=('Arial', 12))


# Validate sign up credentials
def signup_validation():
    # Getting entries
    username = entUsername.get()
    password = entPassword.get()
    password2 = entCfmPassword.get()

    user_list = []

    tree = ET.parse("Data.xml")
    root = tree.getroot()

    for user_search in root:
        User = user_search.text
        user_list.append(User)

    # Validation checks
    if username == '' or password == '' or password2 == '':
        messagebox.showerror('Existence check', 'Please fill in missing information')
    elif username.isalpha() is False:
        messagebox.showerror('Type check', 'Username must be a string')
    elif password.isalpha() is False:
        messagebox.showerror('Type check', 'Password must be a string')
    elif password2.isalpha() is False:
        messagebox.showerror('Type check', 'Password must be a string')
    elif password != password2:
        messagebox.showerror('Consistency check', 'Passwords must be the same')
    elif username in user_list:
        messagebox.showerror('Existence check', 'Username already exists')
    else:
        # Assigning credentials
        userTag = ET.SubElement(root, "Username")
        userTag.text = username
        passTag = ET.SubElement(userTag, "Password")
        passTag.text = password
        scoreTag = ET.SubElement(userTag, "Score")
        scoreTag.text = '0'

        # Writing credentials to xml file
        tree.write("Data.xml")

        login()


# Buttons
btnValidation = Button(signup_window, text="Sign Up", command=signup_validation, fg='Dark Blue', bg='Light Blue', font=("Arial Black", 12))
btnLogin = Button(signup_window, text="Sign In Instead", command=login, fg='Dark Blue', bg='Light Blue', font=("Arial Black", 12))


# Placing Objects

# Placing labels
lblTitle.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
lblUser.grid(row=1, column=0, padx=5, pady=5)
lblPass.grid(row=2, column=0, padx=5, pady=5)
lblConfirm.grid(row=3, column=0, padx=5, pady=5)

# Placing entry
entUsername.grid(row=1, column=1, padx=5)
entPassword.grid(row=2, column=1, padx=5)
entCfmPassword.grid(row=3, column=1)

# Placing buttons
btnValidation.grid(row=5, column=0, columnspan=3)
btnLogin.grid(row=6, column=0, columnspan=3, pady=5)

signup_window.mainloop()
