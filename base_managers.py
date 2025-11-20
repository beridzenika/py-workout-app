import json
class BaseManager: # parent class for db managers
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_json() # load data

    def load_json(self):
        # return json file
        with open(self.filename, "r") as f:
            return json.load(f)

    def update_json(self):
        # update json file
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)

class ProgressManager(BaseManager):
    def __init__(self, filename):
        super().__init__(filename)
    
    def get_current_day(self): #due day
        return self.data["current_day"]
    
    def get_after_num(self): # min num of compulsory cooldown exercises
        return self.data["after_num"]

    def next_day(self, days_len):
        # update current day
        self.data["current_day"] += 1
        if self.data["current_day"] > days_len:
            self.data["current_day"] = 1
    
    def add_to_progress(self, done_workout):
        # add done workout to progress db
        self.data["history"].append(done_workout)

class PlanManager(BaseManager):
    def __init__(self, filename):
        super().__init__(filename)
    
    def get_days_len(self):
        # conditioning (main) exercises
        return len(self.data["days"])

    def get_before(self):
        # wormup exercises
        return self.data["before"]
    
    def get_after(self):
        # cooldown exercises
        return self.data["after"]
    
    def get_day(self, current_day):
        # current day data
        return self.data["days"][str(current_day)]