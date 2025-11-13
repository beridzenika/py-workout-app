import json

class Manager:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_json()

    def load_json(self):
        # return json file
        with open(self.filename, "r") as f:
            return json.load(f)
    
    def next_day(self):
        self.data["current_day"] += 1
        if self.data["current_day"] > len(self.data["days"]):
            self.data["current_day"] = 1


    def update_json(self):
        # update json file
        with open(self.filename, "w") as f:
            json.dump(self.data, f, indent=4)
        print("data updated")
