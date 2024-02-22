import pickle
from pathlib import Path

import streamlit_authenticator as stauth

# creating the lists for the passwords of the students
passwords = ["456", "789", "1098"]

# hashing the passwords to prevent people from accessing these passwords
hashed_passwords = stauth.Hasher(passwords).generate()

# storing the hashed passwords in a pickle file
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)

