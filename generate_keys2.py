import pickle
from pathlib import Path

import streamlit_authenticator as stauth

# creating the lists for the passwords of the teachers
passwords2 = ["123", "987"]

# hashing the passwords to prevent people from accessing these passwords
hashed_passwords2 = stauth.Hasher(passwords2).generate()

# storing the hashed passwords in a pickle file
file_path = Path(__file__).parent / "hashed_pw2.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords2, file)
