import pickle

def verify_pkl_data_structure(pkl_path):
    """
    Loads data from a pkl file and verifies if it's a list of lists.

    Args:
        pkl_path (str): The path to the .pkl file.

    Returns:
        bool: True if the data is a list of lists, False otherwise.
    """
    try:
        with open(pkl_path, 'rb') as f:
            data = pickle.load(f)

        if isinstance(data, list):
            all_are_lists = all(isinstance(item, list) for item in data)
            if all_are_lists:
               print("The data in the pkl file is a list of lists.")
               # Show the full list of lists structure
               print(data)
               # Show the type of the first element if any
               if len(data)> 0:
                    print(f"The type of the first element of the list is: {type(data[0])}")
               return True
            else:
                print("The data in the pkl file is a list but not all the elements are lists")
                return False
        else:
            print("The data in the pkl file is not a list.")
            return False

    except FileNotFoundError:
        print(f"Error: File not found at '{pkl_path}'")
        return False
    except pickle.PickleError as e:
        print(f"Error loading the file: {e}")
        return False
    except Exception as e:
       print(f"Error loading data from {pkl_path}: {e}")
       return False

# Replace with the actual path to your .pkl file
pkl_file = "testetower.pkl"

if verify_pkl_data_structure(pkl_file):
    print("The data structure is correct.")
else:
    print("The data structure is incorrect.")
