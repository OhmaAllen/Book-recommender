from ApplicationInterface import ApplicationInterface
import pickle
import os

app = ApplicationInterface()
app.load_from_dataset()

if not os.path.exists("./application.pkl"):
    # serialize the object
    with open("./application.pkl", "wb") as f:
        pickle.dump(app, f)