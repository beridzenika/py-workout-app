from base_managers import PlanManager, ProgressManager
from datetime import datetime

class Manager:
    def __init__(self, plan_file, progress_file):
        #plan and progress classes
        self.plan = PlanManager(plan_file)
        self.progress = ProgressManager(progress_file)

    def next_day(self):
        # move to next day and save progress
        self.progress.next_day(self.plan.get_days_len())

    def update_json(self):
        #update manually
        self.progress.update_json() # gives error here

    def get_day_data(self):
        # get data gui needs for the current day plan
        current_day = self.progress.get_current_day()
        # days workouts data needed for gui
        data = {
            "after_num": self.progress.get_after_num(),
            "muscles": self.plan.get_day(current_day)["muscles"],
            "plan": [
                ("warmup", self.plan.get_before()),
                ("conditioning", self.plan.get_day(current_day)["exercises"]),
                (f"cooldown (min {self.progress.get_after_num()})", self.plan.get_after())
            ]
        }
        return data
    
    def add_to_progress(self, done_workout):
        # add done workouts to progress db
        entry = {
            "date" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "day" : datetime.now().strftime("%A"),
            # also get the muscle day                    //////////////////////////////////////////
            "exercises" : done_workout
        }
        self.progress.add_to_progress(entry)