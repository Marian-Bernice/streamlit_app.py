from copyreg import pickle
from pathlib import Path

import streamlit_authenticator as stauth

names = ['Marian-Bernice Haligah', 'Godlove Otoo']
usernames = ['mbhaligah', 'gdaniotoo']
passwords = ['logmein', 'ilovegod']

hashed_passwords = stauth.Hasher(passwords).generate()
file_path = Path(__file__).parent / 'hashed_pw.pkl'
with file_path.open('wb') as file:
    pickle.dump(hashed_passwords, file)


