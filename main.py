from manager import Manager
from gui import GUI
import time

# running code
def main():    
    manager = Manager("plan.json", "progress.json")
    data = manager.get_day_data() # get data

    gui = GUI(data)
    gui.run() # run gui

    if gui.completed: # if day done
        manager.next_day() # edit next day workout
        done_workout = gui.get_done_workout()
        manager.add_to_progress(done_workout) # add node workout to progress db
        manager.update_json() # update progress db

main()