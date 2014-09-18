def make_database():
    """ 
    Creates a database
    """
    return []

def add_value(database, key, value):
    """
    Creates a mapping between that key and value inside of the database. If the
    key already exists in the database, then we replace the previous key-value pair
    with the new one.
    """
    if type(key) != int and type(key) != str:
        raise TypeError("databases only accept strings or numbers as keys")
    for i in range(len(database)):
        k, v = database[i]
        if k == key:
            return database[:i] + database[i+1:] + [[key, value]]
    return database + [[key, value]]

def get_keys(database):
    """
    Returns a list that contains all the keys found in that database, in
    arbitrary order
    """
    return [key for key, val in database]

def get_values(database):
    """
    Returns a list that contains all the values found in that database, in
    arbitrary order
    """
    return [val for key, val in database]

def get_value_from_key(database, key):
    """
    Returns the value associated with that key. It will raise error if the key
    is not found in the database.
    """
    for k, v in database:
        if k == key:
            return v
    raise KeyError("key", key, "not found in database")

def get_len(database):
    """
    Returns how many key-value pairs are in the database
    """
    return len(database)

def get_items(database):
    """
    Returns a list of the key-value pairs, in arbitrary order
    """
    return database
