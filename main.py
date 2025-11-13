from manager import Manager
from gui import GUI
import time



# running code
def main():    
    manager = Manager("workouts.json")
    data = manager.load_json()
    
    gui = GUI(data)
    gui.run()

    if gui.completed:
        manager.next_day()
        manager.update_json()


main()