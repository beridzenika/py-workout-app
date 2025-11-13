import tkinter as tk
import time

class GUI:
    def __init__(self, data):
        self.completed=False
        self.data = data
        self.after_num = data["after_num"]
        self.current_day = str(data["current_day"])
        self.day = data["days"][self.current_day]
        self.steps = [
            ("warmup", lambda: self.data["before"]),
            ("conditioning", lambda: self.day["exercises"]),
            ("cooldown (min 5)", lambda: self.data["after"])
        ]
        self.current_step = 0
        self.li_buttons = []

        self.root = tk.Tk() # initiate window entrance
        self.root.geometry("420x420")
        self.root.title("Workout app")

        self.title = tk.Label(self.root, 
                              text=f"Today is {self.day["muscles"]} day", 
                              font=('Arial', 18))
        self.step_frame = tk.Frame(self.root)
        

    def show_list(self, stage):
        stage_name = stage[0]
        exercises = stage[1]()
        tk.Label(self.step_frame, 
                 text=stage_name, 
                 font=('Arial', 14)).pack()
        for i, exercise in enumerate(exercises): # iterate exercises
            text = self.button_text(exercise) #get button text

            li=tk.Button(self.step_frame, 
                        text=text,
                        bg= self.set_color(exercise["set"]),
                        fg="white",
                        font=('Arial', 12),
                        command=lambda i=i, exercise=exercise: self.set_button(i, exercise))
            li.pack(pady=5)
            self.li_buttons.append(li)


    def set_button(self, i, exercise):

        #if has time duration
        if exercise["type"] == "time" and isinstance(exercise["duration"], int):
            self.li_buttons[i].config(state=tk.DISABLED,)  #freezing the button    

            remaining = exercise["duration"]
            self.timer(remaining, exercise, i)
        else:
            self.complete_set(exercise, i) #decrease set/delete


    def complete_set(self, exercise, i):
        exercise["set"] -= 1 #decrease set
        
        self.li_buttons[i].config(
            text=self.button_text(exercise), #change text
            bg= self.set_color(exercise["set"]) #change color
        )
        if exercise["set"] <= 0: 
            self.li_buttons[i].destroy() #delete button on window
            self.li_buttons[i] = False
            #check if all exercises are done
            self.check_if_finished()


    def timer(self, remaining, exercise, i):
        if remaining > 0:
            self.root.after(1000, lambda: self.timer(remaining-1, exercise, i)) #countdown with one sec and recurse
            time_left = f"{remaining} sec"
            if remaining >= 60:
                min=remaining//60
                sec=remaining%60
                time_left = f"{min}m  {sec}s"
            self.li_buttons[i].config(text=f"{exercise["exercise"]} - {exercise["set"]} sets x {time_left}")
        else:
            self.complete_set(exercise, i)
            if self.li_buttons[i] != False:
                self.li_buttons[i].config(state=tk.NORMAL)
            

    def button_text(self, exercise):
        if exercise["type"] == "reps":
            return f"{exercise["exercise"]} - {exercise["set"]} sets x {exercise["rep"]} reps"
        elif isinstance(exercise["duration"], int):
            return f"{exercise["exercise"]} - {exercise["set"]} sets x {exercise["duration"]} sec"
        else:
            return f"{exercise["exercise"]} - {exercise["set"]} sets {exercise["duration"]}"


    def set_color(self, set):
        if set >=3:
            return "#FF4027"
        elif set == 2:
            return "#FFA916"
        else:
            return "#6EEE3B"

        
    def complete_day(self):
        self.completed=True
        self.root.quit()
    

    def check_if_finished(self):
        btn_num = self.li_buttons.count(False)
        step_len = len(self.steps) - 1
        if 0 <= self.current_step < step_len and btn_num == len(self.li_buttons):
            tk.Button(self.step_frame, 
                      text=f"Do next step", 
                      bg= "#066896",
                      fg="white",
                      font=('Arial', 18),
                      command=self.next_step).pack()
        elif self.current_step == step_len and btn_num >= self.after_num:
            tk.Button(self.step_frame, 
                      text=f"Finish workout?", 
                      bg= "#066896",
                      fg="white",
                      font=('Arial', 18),
                      command=self.complete_day).pack()
                
    def next_step(self):
        self.current_step += 1
        self.li_buttons.clear()
        for widget in self.step_frame.winfo_children():
            widget.destroy()
        self.show_list(self.steps[self.current_step])

    def run(self):
        self.title.pack()
        self.step_frame.pack()
        self.show_list(self.steps[self.current_step])

        self.root.mainloop() # place window on screen