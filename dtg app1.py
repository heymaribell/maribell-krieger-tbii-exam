import tkinter as tk
from tkinter import messagebox, ttk
import random


class DailyTaskGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Task Generator")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.config(bg="darkseagreen")

        self.label_font = ("Britannic", 15, "bold")
        self.button_font = ("Britannic", 12, "bold")
        self.entry_font = ("Britannic", 12, "normal")
        self.reward = None

        # Configure the grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Initial UI setup
        self.setup_initial_frame()

    def setup_initial_frame(self):
        self.clear_frame()

        # Top frame for the main title
        top_frame = tk.Frame(self.root, width=600, height=40, bg="cornsilk")
        top_frame.grid(row=0, column=0, padx=0, pady=5)
        lbl = tk.Label(top_frame, text="Daily Task Generator", font=("Britannic", 30, "bold"),
                       fg="seagreen", bg="cornsilk", bd=0, padx=160, pady=20)
        lbl.pack()

        # Middle frame for the descriptive labels
        middle_frame = tk.Frame(self.root, width=600, height=200, bg="darkseagreen")
        middle_frame.grid(row=1, column=0, padx=0, pady=10)
        lbl1 = tk.Label(middle_frame, text="Organize your daily tasks in a fun way!\n\n"
                                           "No endless lists and getting overwhelmed; it's only 10 tasks. \n\n"
                                           "Daily Task Generator will randomly pick one out of ten.",
                        font=("Britannic", 20, "bold"), fg="cornsilk", bg="darkseagreen", bd=0, pady=10)
        lbl1.pack()

        # Bottom frame for the button
        bottom_frame = tk.Frame(self.root, width=600, height=300, bg="darkseagreen")
        bottom_frame.grid(row=2, column=0, padx=0, pady=10)
        start_button = tk.Button(bottom_frame, text="Get Started", font=("Britannic", 20, "bold"),
                                 fg="seagreen", bg="darkseagreen", width=20, height=2, command=self.show_reward_option)
        start_button.pack(pady=20)

    def show_reward_option(self):
        self.clear_frame()

        initial_frame = tk.Frame(self.root, bg="cornsilk", bd=5)
        initial_frame.place(relx=0.5, rely=0.5, anchor="center")

        initial_label = tk.Label(initial_frame, text="Do you want to enter a reward?", bg="cornsilk",
                                 font=self.label_font, fg="seagreen")
        initial_label.pack(pady=10, padx=20)

        enter_reward_button = tk.Button(initial_frame, text="Enter Reward", command=self.show_reward_frame,
                                        bg="darkseagreen", font=self.button_font, fg="seagreen", bd=3)
        enter_reward_button.pack(pady=10)

        skip_reward_button = tk.Button(initial_frame, text="Skip Reward", command=self.start_progress_bar,
                                       bg="darkseagreen", font=self.button_font, fg="seagreen", bd=3)
        skip_reward_button.pack(pady=10)

    def show_reward_frame(self):
        self.clear_frame()

        reward_frame = tk.Frame(self.root, bg="cornsilk", bd=5)
        reward_frame.place(relx=0.5, rely=0.5, anchor="center")

        reward_label = tk.Label(reward_frame, text="Enter your reward:", bg="cornsilk",
                                font=self.label_font, fg="seagreen")
        reward_label.pack(pady=10, padx=20)

        self.reward_entry = tk.Entry(reward_frame, width=30, font=self.entry_font, fg="seagreen", bd=3)
        self.reward_entry.pack(pady=5)

        submit_button = tk.Button(reward_frame, text="Submit", command=self.submit_reward,
                                  bg="darkseagreen", font=self.button_font, fg="seagreen", bd=3)
        submit_button.pack(pady=10)

    def submit_reward(self):
        self.reward = self.reward_entry.get()
        self.start_progress_bar()

    def start_progress_bar(self):
        self.clear_frame()

        progress_frame = tk.Frame(self.root, bg="darkseagreen")
        progress_frame.place(relx=0.5, rely=0.5, anchor="center")

        lbl = tk.Label(progress_frame, text="Take a deep breath and let's go!", font=("Britannic", 30, "bold"),
                       fg="seagreen", bg="cornsilk", bd=0, padx=160, pady=20)
        lbl.pack(side=tk.TOP, pady=20)

        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100, style="TProgressbar")
        progress_bar.pack(expand=True, fill="both", padx=100, pady=20)

        style = ttk.Style()
        style.theme_use('default')
        style.configure("TProgressbar", troughcolor='seagreen', background='cornsilk')

        def update_progress():
            for i in range(101):
                progress_var.set(i)
                self.root.update_idletasks()
                self.root.after(100)  # 100 ms per step for a total of 10 seconds
            self.start_task_manager()

        self.root.after(0, update_progress)

    def start_task_manager(self):
        self.clear_frame()
        self.list_tasks = []
        list_task_entries_frame = tk.Frame(self.root, bg="darkseagreen")
        list_task_entries_frame.pack(pady=40)

        def add_task_entries():
            for _ in range(10):
                entry = tk.Entry(list_task_entries_frame, width=30)
                entry.pack(pady=7)
                entry.bind("<Return>", focus_next_entry)
                self.list_tasks.append(entry)

        def focus_next_entry(event):
            current_entry = event.widget
            current_index = self.list_tasks.index(current_entry)
            next_index = (current_index + 1) % len(self.list_tasks)
            self.list_tasks[next_index].focus_set()

        add_task_entries()

        pick_random_task_button = tk.Button(self.root, text="Pick Random Task", font=("Britannic", 15, "bold"),
                                            fg="seagreen", bg="cornsilk", command=self.pick_random_task)
        pick_random_task_button.pack(pady=5)

    def pick_random_task(self):
        available_tasks = [entry.get() for entry in self.list_tasks if entry.get().strip()]
        if available_tasks:
            selected_task = random.choice(available_tasks)
            for entry in self.list_tasks:
                if entry.get() == selected_task:
                    entry.delete(0, tk.END)
            messagebox.showinfo("Next Task", f"Next Task: {selected_task}")
        else:
            self.show_reward_message()

    def show_reward_message(self):
        if self.reward:
            messagebox.showinfo("Reward", f"Congratulations! You've completed all tasks.\nYour reward: {self.reward}")
        else:
            messagebox.showinfo("Reward", "Congratulations! You've completed all tasks.")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = DailyTaskGenerator(root)
    root.mainloop()
