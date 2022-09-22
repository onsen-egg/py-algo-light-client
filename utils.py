import pickle

def load(obj_file):
  with open(obj_file, "rb") as f:
    return pickle.load(f)
