import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import pickle
from pathlib import Path
import time
from variables import teachers_students, nom, best_breath, result_o2, result_co2

import streamlit_authenticator as stauth

check2 = True
check3 = False
timer1 = 0

alt.data_transformers.disable_max_rows()

if 'key' not in st.session_state:
    st.session_state['count_o2'] = 0

if 'key' not in st.session_state:
    st.session_state['count_co2'] = 0

if 'key' not in st.session_state:
    st.session_state['key'] = pd.DataFrame()

if 'key_o2' not in st.session_state:
    st.session_state['key_o2'] = pd.DataFrame()

if 'key_co2' not in st.session_state:
    st.session_state['key_co2'] = pd.DataFrame()

if 'check' not in st.session_state:
    st.session_state['check'] = 0

if 'check2' not in st.session_state:
    st.session_state['check2'] = 0

if 'check3' not in st.session_state:
    st.session_state['check3'] = 0

if 'o2_breath_prepare' not in st.session_state:
    st.session_state['o2_breath_prepare'] = 2

if 'o2_breath_hold' not in st.session_state:
    st.session_state['o2_breath_hold'] = 1

if 'o2_breath_increase' not in st.session_state:
    st.session_state['o2_breath_increase'] = 2

if 'number_sets_o2' not in st.session_state:
    st.session_state['number_sets_o2'] = 2

if 'co2_breath_prepare' not in st.session_state:
    st.session_state['co2_breath_prepare'] = 6

if 'co2_breath_hold' not in st.session_state:
    st.session_state['co2_breath_hold'] = 2

if 'co2_breath_decrease' not in st.session_state:
    st.session_state['co2_breath_decrease'] = 1

if 'number_sets_co2' not in st.session_state:
    st.session_state['number_sets_co2'] = 2

# storing the list containing the results of the best breath hold exercise of every students in a pickle file
def save_bestbreath(save_best_breath):
    with open('data.pkl', 'wb') as file1:
        pickle.dump(save_best_breath, file1)

# loading the list containing the results of the best breath hold exercise of every students from the pickle file
def load_data():
    try:
        with open('data.pkl', 'rb') as file1:
            save_best_breath = pickle.load(file1)
    except FileNotFoundError:
        save_best_breath = []
    return save_best_breath

# storing the list containing the results of the table of co2 exercise of every students in a pickle file
def save_resultco2(save_result_co2):
    with open('data.pkl2', 'wb') as file3:
        pickle.dump(save_result_co2, file3)

# loading the list containing the results of the table of co2 exercise of every students from the pickle file
def load_dataco2():
    try:
        with open('data.pkl2', 'rb') as file3:
            save_result_co2 = pickle.load(file3)
    except FileNotFoundError:
        save_result_co2 = []
    return save_result_co2

# storing the list containing the results of the table of o2 exercise of every students in a pickle file
def save_resulto2(save_result_o2):
    with open('data.pkl3', 'wb') as file4:
        pickle.dump(save_result_o2, file4)

# loading the list containing the results of the table of o2 exercise of every students from the pickle file
def load_data_o2():
    try:
        with open('data.pkl3', 'rb') as file4:
            save_result_o2 = pickle.load(file4)
    except FileNotFoundError:
        save_result_o2 = []
    return save_result_o2

# storing the list containing the students of every teacher
def save_teacher_student(save_teacherstudents):
    with open('data.pkl4', 'wb') as file5:
        pickle.dump(save_teacherstudents, file5)

# loading the list containing the the students of every teacher
def load_data_teacher_student():
    try:
        with open('data.pkl4', 'rb') as file5:
            save_teacherstudents = pickle.load(file5)
    except FileNotFoundError:
        save_teacherstudents = []
    return save_teacherstudents



# this is the function for the best breath hold exercise
def start():
    global timer1
    clock = int(user_time)
    time_box.empty()
    for secs in range(clock, 0, -1):
        mm, ss = secs // 60, secs % 60
        timer.metric("Countdown", f"{mm:02d}:{ss:02d}")
        time.sleep(1)
    clock = 0
    st.button("Stop", on_click=time1, key=f"button-{clock}")

    mm, ss = 0, 0
    while True:
        timer.metric("time you have been holding your breath for", f"{mm:02d}:{ss:02d}")
        time.sleep(1)
        ss += 1
        timer1 += 1
        if (ss % 60) == 0:
            mm += 1
            ss = 0

# function to save the results from the best breath hold exercise
def time1():
    st.session_state['check'] = 0
    if len(best_breath) == 0:
        best_breath.append([name, timer1])
        st.session_state['check'] = 2
    for z in range(len(best_breath)):
        if st.session_state['check'] == 2:
            break
        if best_breath[z][0] == name:
            best_breath[z].append(timer1)
            st.session_state['check'] = 1
    if st.session_state['check'] == 0:
        best_breath.append([name, timer1])
    save_bestbreath(best_breath)


# function to save the results from the table of o2 exercise
def time2():
    st.session_state['check2'] = 0
    if len(result_o2) == 0:
        result_o2.append([name, [st.session_state['o2_breath_prepare']], [st.session_state['o2_breath_hold']],
                          [st.session_state['o2_breath_increase']], [st.session_state['number_sets_o2']],
                          ["trial 1" + " incompleted"]])
        st.session_state['check2'] = 2
    for p in range(len(result_o2)):
        if st.session_state['check2'] == 2:
            break
        if result_o2[p][0] == name:
            result_o2[p][1].append(st.session_state['o2_breath_prepare'])
            result_o2[p][2].append(st.session_state['o2_breath_hold'])
            result_o2[p][3].append(st.session_state['o2_breath_increase'])
            result_o2[p][4].append(st.session_state['number_sets_o2'])
            st.session_state['count_o2'] = len(result_o2[p][5])
            result_o2[p][5].append("trial " + str(st.session_state['count_o2']) + " incompleted")
            st.session_state['check2'] = 1
    if st.session_state['check2'] == 0:
        result_o2.append([name, [st.session_state['o2_breath_prepare']],
                          [st.session_state['o2_breath_hold']], [st.session_state['o2_breath_increase']],
                          [st.session_state['number_sets_o2']], ["trial 1" + " incompleted"]])
    save_resulto2(result_o2)

def time3():
    st.session_state['check3'] = 0
    if len(result_co2) == 0:
        result_co2.append([name, [st.session_state['co2_breath_prepare']], [st.session_state['co2_breath_hold']], [st.session_state['co2_breath_decrease']], [st.session_state['number_sets_co2']], ["trial 1" + " incompleted"]])
        st.session_state['check3'] = 2
    for q in range(len(result_co2)):
        if st.session_state['check3'] == 2:
            break
        if result_co2[q][0] == name:
            result_co2[q][1].append(st.session_state['co2_breath_prepare'])
            result_co2[q][2].append(st.session_state['co2_breath_hold'])
            result_co2[q][3].append(st.session_state['co2_breath_decrease'])
            result_co2[q][4].append(st.session_state['number_sets_co2'])
            st.session_state['count_co2'] = len(result_co2[q][5])
            result_co2[q][5].append("trial " + str(st.session_state['count_co2']) + " incompleted")
            st.session_state['check3'] = 1
    if st.session_state['check3'] == 0:
        result_co2.append([name, [st.session_state['co2_breath_prepare']], [st.session_state['co2_breath_hold']], [st.session_state['co2_breath_decrease']], [st.session_state['number_sets_co2']], ["trial 1" + " incompleted"]])
    save_resultco2(result_co2)

    pass

# function for the table of o2 exercise
def table_o2():
    st.session_state['count_o2'] += 1
    buttonPlaceholder.empty()
    buttonPlaceholder2.empty()
    placeholder9 = st.empty()
    for i in range(st.session_state['number_sets_o2']):
        breathHoldTime = st.session_state['o2_breath_hold'] + (i * st.session_state['o2_breath_increase'])
        buttonPlaceholder.button("click here to quit", on_click=time2, key=f"button-{i}")
        breathPrepareTime = st.session_state['o2_breath_prepare']
        for secs in range(breathPrepareTime, 0, -1):
            mm, ss = secs // 60, secs % 60
            placeholder9.metric("time to prepare for breath hold", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        for secs in range(breathHoldTime, 0, -1):
            mm, ss = secs // 60, secs % 60
            placeholder9.metric("time to hold your breath for", f"{mm:02d}:{ss:02d}")
            time.sleep(1)


def save_o2():

    st.session_state['check2'] = 0
    if len(result_o2) == 0:
        result_o2.append([name, [st.session_state['o2_breath_prepare']], [st.session_state['o2_breath_hold']], [st.session_state['o2_breath_increase']], [st.session_state['number_sets_o2']], ["trial 1" + " completed"]])
        save_resulto2(result_o2)
        st.session_state['check2'] = 2
    for p in range(len(result_o2)):
        if st.session_state['check2'] == 2:
            break
        if result_o2[p][0] == name:
            result_o2[p][1].append(st.session_state['o2_breath_prepare'])
            result_o2[p][2].append(st.session_state['o2_breath_hold'])
            result_o2[p][3].append(st.session_state['o2_breath_increase'])
            result_o2[p][4].append(st.session_state['number_sets_o2'])
            st.session_state['count_o2'] = len(result_co2[p][5])
            result_o2[p][5].append("trial " + str(st.session_state['count_o2']) + " completed")
            st.session_state['check2'] = 1
    if st.session_state['check2'] == 0:
        result_o2.append([name, [st.session_state['o2_breath_prepare']], [st.session_state['o2_breath_hold']], [st.session_state['o2_breath_increase']], [st.session_state['number_sets_o2']], ["trial 1" + " completed"]])
    save_resulto2(result_o2)


# function for the table of co2 exercise
def table_co2():
    st.session_state['count_co2'] += 1
    buttonPlaceholder.empty()
    buttonPlaceholder2.empty()
    placeholder9 = st.empty()
    for d in range(st.session_state['number_sets_co2']):
        breathHoldTime = st.session_state['co2_breath_hold']
        buttonPlaceholder.button("click here to quit", on_click=time3, key=f"button-{d}")
        breathPrepareTime = st.session_state['co2_breath_prepare'] - (d * st.session_state['co2_breath_decrease'])
        for secs in range(breathPrepareTime, 0, -1):
            mm, ss = secs // 60, secs % 60
            placeholder9.metric("time to prepare for breath hold", f"{mm:02d}:{ss:02d}")
            time.sleep(1)
        for secs in range(breathHoldTime, 0, -1):
            mm, ss = secs // 60, secs % 60
            placeholder9.metric("time to hold your breath for", f"{mm:02d}:{ss:02d}")
            time.sleep(1)


def save_co2():
    st.session_state['check3'] = 0
    if len(result_co2) == 0:
        result_co2.append([name, [st.session_state['co2_breath_prepare']], [st.session_state['co2_breath_hold']], [st.session_state['co2_breath_decrease']], [st.session_state['number_sets_co2']], ["trial 1" + " completed"]])
        save_resultco2(result_co2)
        st.session_state['check3'] = 2
    for q in range(len(result_co2)):
        if st.session_state['check3'] == 2:
            break
        if result_co2[q][0] == name:
            result_co2[q][1].append(st.session_state['co2_breath_prepare'])
            result_co2[q][2].append(st.session_state['co2_breath_hold'])
            result_co2[q][3].append(st.session_state['co2_breath_decrease'])
            result_co2[q][4].append(st.session_state['number_sets_co2'])
            st.session_state['count_co2'] = len(result_co2[q][5])
            result_co2[q][5].append("trial " + str(st.session_state['count_co2']) + " completed")
            st.session_state['check3'] = 1
    if st.session_state['check3'] == 0:
        result_co2.append([name, [st.session_state['co2_breath_prepare']], [st.session_state['co2_breath_hold']], [st.session_state['co2_breath_decrease']], [st.session_state['number_sets_co2']], ["trial 1" + " completed"]])
    save_resultco2(result_co2)


# function to edit the table of co2
def edit_o2():
    st.session_state['o2_breath_prepare'] = (prepare_o2 * 60) + prepare_o22
    st.session_state['o2_breath_hold'] = (hold_o2 * 60) + hold_o22
    st.session_state['o2_breath_increase'] = difference_o2
    st.session_state['number_sets_o2'] = number_sets


# function to edit the table of o2
def edit_co2():
    st.session_state['co2_breath_prepare'] = (prepare_co2 * 60) + prepare_co22
    st.session_state['co2_breath_hold'] = (hold_co2 * 60) + hold_co22
    st.session_state['co2_breath_decrease'] = difference_co2
    st.session_state['number_sets_co2'] = number_sets_co2


# login page for students
placeholder = st.empty()
check = placeholder.radio("choose which one you are 👇", ('choose', 'teacher', 'student'), disabled=False)

if check == 'student':
    names = ["Romain Cherdel", "Aidan hankins"]
    usernames = ["romain_chrd", "aidan_hks"]
    file_path = Path(__file__).parent / "hashed_pw.pkl"
    with file_path.open("rb") as file:
        passwords = pickle.load(file)

    credentials = {
        "usernames": {
            usernames[0]: {
                "name": names[0],
                "password": passwords[0]
            },
            usernames[1]: {
                "name": names[1],
                "password": passwords[1]
            }
        }
    }

    for uname, name, pwd in zip(usernames, names, passwords):
        user_dict = {"name": name, "password": pwd}
        credentials["usernames"].update({uname: user_dict})
    authenticator = stauth.Authenticate(credentials, "sales_dashboard", "auth", cookie_expiry_days=0)

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status == False:
        st.error("username/password is incorrect")

    if authentication_status == None:
        st.warning("please enter username/password")

    if authentication_status:
        length = len(teachers_students)
        placeholder.empty()
        save_placeholder = st.empty()
        option = save_placeholder.radio('who is your teacher', ('select', 'Géraud', 'Turland'),
                                        disabled=False)
        if option == 'select':
            pass
            for i in range(len(teachers_students)):
                if teachers_students[i][0] == name:
                    nom = True
        else:
            teachers_students.append([name, option])
            save_teacher_student(teachers_students)

        if len(teachers_students) > length:
            nom = True
        if nom:
            with st.sidebar:
                save_placeholder.empty()
                selected = option_menu(menu_title="Main menu",
                                       options=["Home", "Best breath hold time", "Table of O2", "Table of co2", "edit your table of o2", "edit your table of co2", "results"])
            if selected == "Home":
                st.title(f"welcome {name}")
                st.title(f"You have selected {selected}")
                authenticator.logout("Logout", "main")

            # section to start the best breath hold exercise
            if selected == "Best breath hold time":
                st.title(f"You have selected {selected}")
                timer = st.empty()
                bt = st.empty()
                time_box = st.empty()
                user_time = time_box.text_input("Enter your time: ")
                st.button("Start", on_click=start)

            # section to start the table of o2 exercise
            if selected == "Table of O2":
                st.title(f"You have selected {selected}")
                st.subheader("Hi, I am Romain")
                buttonPlaceholder = st.empty()
                buttonPlaceholder2 = st.empty()
                buttonPlaceholder.button("click here to start", on_click=table_o2)
                buttonPlaceholder2.button("click here to save result", on_click=save_o2)

            # section to start the table of co2 exercise
            if selected == "Table of co2":
                st.title(f"You have selected {selected}")
                st.subheader("Hi, I am Romain")
                buttonPlaceholder = st.empty()
                buttonPlaceholder2 = st.empty()
                buttonPlaceholder.button("click here to start", on_click=table_co2)
                buttonPlaceholder2.button("click here to save result", on_click=save_co2)

            # section to edit the table of co2 exercise
            if selected == "edit your table of o2":
                prepare_o2 = st.slider('how long do you want to prepare you breath hold for in min', 0, 10, 5)
                prepare_o22 = st.slider('how long do you want to prepare you breath hold for in seconds', 0, 60, 30)
                hold_o2 = st.slider('how long do you want your first breath hold to be in min', 0, 10, 5)
                hold_o22 = st.slider('how long do you want your first breath hold to be in seconds', 0, 60, 30)
                difference_o2 = st.slider('how many seconds of breath hold do you want to add between each set', 0, 60, 30)
                number_sets = st.slider('how many sets do you want to do', 0, 10, 5)
                st.button("click here to edit your table of o2", on_click=edit_o2)

            # section to edit the table of co2 exercise
            if selected == "edit your table of co2":
                prepare_co2 = st.slider('how long do you want to prepare your first breath hold time for in min', 0, 10, 5)
                prepare_co22 = st.slider('how long do you want to prepare your first breath hold time for in seconds', 0, 60, 30)
                hold_co2 = st.slider('how long do you want your breath hold to be in min', 0, 10, 5)
                hold_co22 = st.slider('how long do you want your first breath hold to be in seconds', 0, 60, 30)
                difference_co2 = st.slider('how many seconds of breath prepare time do you want to remove between each set', 0, 60, 30)
                number_sets_co2 = st.slider('how many sets do you want to do', 0, 10, 5)
                st.button("click here to edit your table of o2", on_click=edit_co2)

            if selected == "results":
                result_o2 = load_data_o2()
                result_co2 = load_dataco2()
                best_breath = load_data()
                teachers_students = load_data_teacher_student()
                print(result_o2)
                st.session_state['check3'] = 1
                st.session_state['check2'] = 1
                st.session_state['check'] = 1
                if len(best_breath) == 0:
                    st.write("No student has done the best breath hold exercise yet ")
                else:
                    for t in range(len(best_breath)):
                        if best_breath[t][0] == name:
                            store_name = best_breath[t][0]
                            best_breath[t].remove(best_breath[t][0])
                            st.session_state['key'] = pd.DataFrame(best_breath[t])
                            print(name)
                            best_breath[t].insert(0, store_name)
                            st.session_state['check'] = 0

                if len(result_o2) == 0:
                    st.write("No student has done the table of o2 exercise yet ")
                else:
                    for h in range(len(result_o2)):
                        if result_o2[h][0] == name:
                            store_name1 = result_o2[h][0]
                            result_o2[h].remove(result_o2[h][0])
                            st.session_state['key_o2'] = pd.DataFrame(
                               {
                                   "breathprepare time": result_o2[h][0],
                                   "initial breath hold time": result_o2[h][1],
                                   "increase in breath hold time between each set in seconds": result_o2[h][2],
                                   "number of sets": result_o2[h][3],
                                   "failure": result_o2[h][4],

                               }
                            )
                            result_o2[h].insert(0, store_name1)
                            st.session_state['check2'] = 0

                if len(result_co2) == 0:
                    st.write("No student has done the table of co2 exercise yet ")
                else:
                    for b in range(len(result_co2)):
                        if result_co2[b][0] == name:
                            store_name2 = result_co2[b][0]
                            result_co2[b].remove(result_co2[b][0])
                            st.session_state['key_co2'] = pd.DataFrame(
                               {
                                   "initial breathprepare time": result_co2[b][0],
                                   "breath hold time": result_co2[b][1],
                                   "decrease in breath prepare time between each set": result_co2[b][2],
                                   "number of sets2": result_co2[b][3],
                                   "failure2": result_co2[b][4],

                               }
                            )
                            result_co2[b].insert(0, store_name2)
                            st.session_state['check3'] = 0

                print(result_o2)
                if st.session_state['check'] == 0:
                    st.area_chart(st.session_state['key'])
                else:
                    st.write("This student hasn't done the best breath hold exercise yet ")
                if st.session_state['check2'] == 0:
                    melted_data = st.session_state['key_o2'].melt(id_vars='failure', var_name='C', value_name='Value')

                    chart = alt.Chart(melted_data).mark_bar().encode(
                        x=alt.X('C:N', title=''),
                        y=alt.Y('Value:Q', title='seconds'),
                        column=alt.Column('failure:N', title='check for completion')
                    ).properties(
                        width=100,
                        title='Grouped Bar Chart for table of o2'
                    )

                    st.altair_chart(chart)
                else:
                    st.write("This student hasn't done the table of o2 exercise yet ")
                if st.session_state['check3'] == 0:
                    melted_data2 = st.session_state['key_co2'].melt(id_vars='failure2', var_name='D', value_name='Value')

                    chart_2 = alt.Chart(melted_data2).mark_bar().encode(
                        x=alt.X('D:N', title=''),
                        y=alt.Y('Value:Q', title='seconds'),
                        column=alt.Column('failure2:N', title='check for completion')
                    ).properties(
                        width=100,
                        title='Grouped Bar Chart for table of co2'
                    )

                    st.altair_chart(chart_2)

                else:
                    st.write("This student hasn't done the table of co2 exercise yet ")

# login page for teachers
elif check == 'teacher':

    names2 = ["Géraud", "Turland"]
    usernames2 = ["grd", "mrt"]

    file_path = Path(__file__).parent / "hashed_pw2.pkl"
    with file_path.open("rb") as file:
        passwords2 = pickle.load(file)

    credentials2 = {
        "usernames": {
            usernames2[0]: {
                "name": names2[0],
                "password": passwords2[0]
            },
            usernames2[1]: {
                "name": names2[1],
                "password": passwords2[1]
            }
        }
    }

    authenticator2 = stauth.Authenticate(credentials2, "sales_dashboard2", "auth2", cookie_expiry_days=0)
    name2, authentication_status2, username2 = authenticator2.login("Login", "main")

    if authentication_status2 == False:
        st.error("username/password is incorrect")

    if authentication_status2 == None:
        st.warning("please enter username/password")

    if authentication_status2:
        result_o2 = load_data_o2()
        result_co2 = load_dataco2()
        best_breath = load_data()
        teachers_students = load_data_teacher_student()
        st.title(f"welcome {name2}")
        authenticator2.logout("Logout", "main")
        placeholder.empty()
        with st.sidebar:
            selected = option_menu(menu_title="Main menu", options=["Home", "Projects"], )
        if selected == "Home":
            students = []
            st.title(f"You have selected {selected}")
            for i in range(len(teachers_students)):
                if teachers_students[i][1] == name2:
                    students.append(teachers_students[i][0])
            students.append("selected")
            x = 1
            myset = set(students)
            check4 = placeholder.radio('choose a student', myset, disabled=False)
            if check4 == "selected":
                print("ya")
            else:
                st.session_state['check3'] = 1
                st.session_state['check2'] = 1
                st.session_state['check'] = 1
                if len(best_breath) == 0:
                    st.write("No student has done the best breath hold exercise yet ")

                # creates the dataframe holding the best breath hold time of the student if they have done the exercise
                else:
                    for t in range(len(best_breath)):
                        if best_breath[t][0] == check4:
                            store_name = best_breath[t][0]
                            best_breath[t].remove(best_breath[t][0])
                            st.session_state['key'] = pd.DataFrame(best_breath[t])
                            best_breath[t].insert(0, store_name)
                            st.session_state['check'] = 0

                if len(result_o2) == 0:
                    st.write("No student has done the table of o2 exercise yet ")
                # creates the dataframe holding the results of the student from the table of o2 exercise if they have done the exercise
                else:
                    for h in range(len(result_o2)):
                        if result_o2[h][0] == check4:
                            st.session_state['key_o2'] = pd.DataFrame(
                               {
                                   "breathprepare time": result_o2[h][1],
                                   "initial breath hold time": result_o2[h][2],
                                   "increase in breath hold time between each set in seconds": result_o2[h][3],
                                   "number of sets": result_o2[h][4],
                                   "failure": result_o2[h][5],

                               }
                            )
                            st.session_state['check2'] = 0

                if len(result_co2) == 0:
                    st.write("No student has done the table of co2 exercise yet ")

                # creates the dataframe holding the results of the student from the table of co2 exercise if they have done the exercise
                else:
                    for b in range(len(result_co2)):
                        if result_co2[b][0] == check4:
                            store_name2 = result_co2[b][0]
                            result_co2[b].remove(result_co2[b][0])
                            st.session_state['key_co2'] = pd.DataFrame(
                               {
                                   "initial breathprepare time": result_co2[b][0],
                                   "breath hold time": result_co2[b][1],
                                   "decrease in breath prepare time between each set": result_co2[b][2],
                                   "number of sets2": result_co2[b][3],
                                   "failure2": result_co2[b][4],

                               }
                            )
                            result_co2[b].insert(0, store_name2)
                            st.session_state['check3'] = 0

                print(st.session_state['key'])
                print(st.session_state['key_o2'])

                # creates the graph showing the breath hold times of the student
                if st.session_state['check'] == 0:
                    st.area_chart(st.session_state['key'])
                else:
                    st.write("This student hasn't done the best breath hold exercise yet ")

                # creates the graph showing the results of the student from the table of o2 exercise
                if st.session_state['check2'] == 0:
                    melted_data = st.session_state['key_o2'].melt(id_vars='failure', var_name='C', value_name='Value')

                    chart = alt.Chart(melted_data).mark_bar().encode(
                        x=alt.X('C:N', title=''),
                        y=alt.Y('Value:Q', title='seconds'),
                        column=alt.Column('failure:N', title='check for completion')
                    ).properties(
                        width=100,
                        title='Grouped Bar Chart for table of o2'
                    )

                    st.altair_chart(chart)
                else:
                    st.write("This student hasn't done the table of o2 exercise yet ")

                # creates the graph showing the results of the student from the table of co2 exercise
                if st.session_state['check3'] == 0:
                    melted_data2 = st.session_state['key_co2'].melt(id_vars='failure2', var_name='D', value_name='Value')

                    chart_2 = alt.Chart(melted_data2).mark_bar().encode(
                        x=alt.X('D:N', title=''),
                        y=alt.Y('Value:Q', title='seconds'),
                        column=alt.Column('failure2:N', title='check for completion')
                    ).properties(
                        width=100,
                        title='Grouped Bar Chart for table of co2'
                    )

                    st.altair_chart(chart_2)

                else:
                    st.write("This student hasn't done the table of co2 exercise yet ")

        if selected == "Projects":
            st.title(f"You have selected {selected}")
            print(result_o2)
            print(result_co2)
            print(best_breath)
