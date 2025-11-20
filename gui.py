import tkinter as tk
import time

class GUI:
    def __init__(self, data):
        self.completed=False # need this for main file
        self.data = data
        self.after_num = self.data["after_num"]
        self.steps = self.data["plan"]
        self.current_step = 0
        self.li_buttons = []

        self.root = tk.Tk() # initiate window entrance
        self.root.geometry("420x420")
        self.root.title("Workout app")

        self.title = tk.Label(self.root, 
                              text=f"Today is {self.data["muscles"]} day", 
                              font=('Arial', 18))
        self.step_frame = tk.Frame(self.root)
        self.finish_button = tk.Button(self.root, # button for finishing given exercises
                      text=f"Skip", 
                      bg= "#066896",
                      fg="white",
                      font=('Arial', 18),
                      command=self.next_step)
                
    
    def show_list(self, step):  
        # show the exercise list 
        step_name = step[0]
        exercises = step[1]
        tk.Label(self.step_frame, # title
                 text=step_name,
                 font=('Arial', 14)).pack() # show title
        for i, exercise in enumerate(exercises): # iterate exercises
            text = self.button_text(exercise) # get button text
            li=tk.Button(self.step_frame,   # create buttons presenting exercises
                        text=text,
                        bg= self.set_color(exercise["set"]),
                        fg="white",
                        font=('Arial', 12),
                        command=lambda i=i, exercise=exercise: self.set_button(i, exercise))
            li.pack(pady=5) # show buttons
            self.li_buttons.append(li) # add button to button array 
        self.finish_button.pack() # show finish button

    def set_button(self, i, exercise):
        #if has time duration
        if exercise["type"] == "time" and isinstance(exercise["duration"], int):
            self.li_buttons[i].config(state=tk.DISABLED,)  #freezing the button    

            remaining = exercise["duration"]
            self.timer(remaining, exercise, i) # turning timer for remaining amount time
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
            self.check_if_finished()  #check if all exercises are done


    def timer(self, remaining, exercise, i):
        if remaining > 0:
            #countdown with one sec and recurse while remaining
            self.root.after(1000, lambda: self.timer(remaining-1, exercise, i)) 
            time_left = f"{remaining} sec"
            # adding minutes if necessary
            if remaining >= 60:
                min=remaining//60
                sec=remaining%60
                time_left = f"{min}m  {sec}s"
            #updating button text
            self.li_buttons[i].config(text=f"{exercise["exercise"]} - {exercise["set"]} sets x {time_left}")
        else:
            self.complete_set(exercise, i) # decrease set/delete 
            if self.li_buttons[i] != False:
                self.li_buttons[i].config(state=tk.NORMAL) # unfreezing the button
            

    def button_text(self, exercise):
        #button text generator
        if exercise["type"] == "reps": # reps: 10
            return f"{exercise["exercise"]} - {exercise["set"]} sets x {exercise["rep"]} reps"
        elif isinstance(exercise["duration"], int): # 30 sec
            return f"{exercise["exercise"]} - {exercise["set"]} sets x {exercise["duration"]} sec"
        else: # max hold
            return f"{exercise["exercise"]} - {exercise["set"]} sets {exercise["duration"]}"


    def set_color(self, set):
        if set >=3: # 3 set
            return "#FF4027"
        elif set == 2: # 2 set
            return "#FFA916"
        else: # 1 set
            return "#6EEE3B"

        
    def complete_day(self):
        self.completed=True
        self.root.quit() # close window
    

    def check_if_finished(self):
        btn_num = self.li_buttons.count(False)
        step_len = len(self.steps) - 1
        if 0 <= self.current_step < step_len and btn_num == len(self.li_buttons): #if list finished
            self.finish_button.config(text=f"Do next step")
        else: #if exercises left
            self.finish_button.config(text=f"Skip")
        if self.current_step == step_len : #if last step (cooldown)
            self.finish_button.config(text=f"Finish", command=self.complete_day)
            if btn_num >= self.after_num: # if all exercises finished (min 5)
                self.finish_button.config(text=f"Finished")
                
    def next_step(self): 
        self.current_step += 1 # increase step
        self.li_buttons.clear() # clear button array
        for widget in self.step_frame.winfo_children():
            widget.destroy() # clear frame
        self.show_list(self.steps[self.current_step]) # show new list
        self.check_if_finished() # update finish button

    def get_done_workout(self): # //////////////////////////////////////////////////////////
        return self.steps[1][1] # done workouts to add to progress db

    def run(self):
        # show initial gui
        self.title.pack()
        self.step_frame.pack()
        self.show_list(self.steps[self.current_step])

        self.root.mainloop() # place window on screen