import config
import sys
import shelve

def shelve_write(id, state):
    with shelve.open(config.shelve_name) as storage:
        storage[str(id)] = state
    
def shelve_read(id):
    with shelve.open(config.shelve_name) as storage:
        try:
            data = storage[str(id)]
        except:
            data = sys.exc_info()
        return data