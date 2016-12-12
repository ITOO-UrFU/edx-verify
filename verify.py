from tkinter import *
import os
import csv

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

courses = []
profile_files = []

for file in os.listdir(DATA_DIR):
    if file.endswith("csv"):
        profile_files.append(file)

for file in profile_files:
        courses.append("_".join(file.split("_")[1:4]))

root = Tk()
root.title("Edx verify")

frame = Frame(root)
frame_text = Frame(root)

courses_list = Listbox(frame, height=14, width=15, selectmode=SINGLE)
emails = Text(frame_text, height=10, width=80, font='Consolas 10', wrap=WORD)
verify_text = Text(frame_text, height=10, width=80, font='Consolas 10', wrap=WORD, fg="green")
errors = Text(frame_text, height=10, width=80, font='Consolas 10', wrap=WORD, fg="red")


def run():
    verify_text.delete('1.0', END)
    errors.delete('1.0', END)

    try:
        profiles_file = os.path.join(DATA_DIR, profile_files[courses_list.curselection()[0]])
        emails_list = emails.get("1.0", END).split("\n")[:-1]

        for email in emails_list:
            email = email.strip()

            with open(profiles_file, encoding='utf8') as csvfile:
                print("Working with: ", email)
                reader = csv.reader(csvfile, delimiter=',')
                for row in reader:
                    if email == row[3] and row[1] != "verified":
                        verify_text.insert(END, row[1] + ";" + row[3] + ";" + row[2] + ";" + row[1] + "\n")
                    elif email == row[3] and row[1] == "verified":
                        errors.insert(END, email + " IN VERIFIED COHORT!\n")
                if email not in profiles_file:
                        errors.insert(END, email + "\n")

    except:
        emails.delete('1.0', END)
        errors.insert(END, "Couldn't open file\n")


run_button = Button(frame, text="Run", width=15, height=2, font='Consolas 10', command=run)


for i in courses:
    courses_list.insert(END, i)


courses_list.pack(side='left')
run_button.pack(side="right")
emails.pack(fill="both")
verify_text.pack(fill="both")
errors.pack(fill="both")
frame.pack(fill="both")
frame_text.pack(fill="both")

root.mainloop()