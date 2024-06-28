import tkinter as tk
from tkinter import messagebox, ttk
import random


# When a new page is launched, the previous page's contents is being cleared.
def clear_widgets(root):
    for i in root.winfo_children():
        i.destroy()


# Initial frame is being set up, with several frames for different purposes.
def setup_initial_frame(root):
    clear_widgets(root)

    top_frame = tk.Frame(root, width=600, height=40, bg="cornsilk")
    top_frame.grid(row=0, column=0, padx=0, pady=5)
    lbl = tk.Label(top_frame, text="Daily Task Generator", font=("Britannic", 30, "bold"),
                   fg="seagreen", bg="cornsilk", bd=0, padx=160, pady=20)
    lbl.pack()

    middle_frame = tk.Frame(root, width=600, height=200, bg="darkseagreen")
    middle_frame.grid(row=1, column=0, padx=0, pady=10)
    lbl1 = tk.Label(middle_frame, text="Organize your daily tasks in a fun way!\n\n"
                                       "No endless lists and getting overwhelmed; it's only 10 tasks. \n\n"
                                       "Daily Task Generator will randomly pick one out of ten.",
                    font=("Britannic", 20, "bold"), fg="cornsilk", bg="darkseagreen", bd=0, pady=10)
    lbl1.pack()

    bottom_frame = tk.Frame(root, width=600, height=300, bg="darkseagreen")
    bottom_frame.grid(row=2, column=0, padx=0, pady=10)
    start_button = tk.Button(bottom_frame, text="Get Started", font=("Britannic", 20, "bold"),
                             fg="seagreen", bg="darkseagreen", width=20, height=2,
                             command=lambda: show_reward_option(root))
    start_button.pack(pady=20)


# A reward option is set up for users to either skip or input a reward.
def show_reward_option(root):
    clear_widgets(root)

    initial_frame = tk.Frame(root, bg="cornsilk", bd=5)
    initial_frame.place(relx=0.5, rely=0.5, anchor="center")

    initial_label = tk.Label(initial_frame, text="Do you want to enter a reward?", bg="cornsilk",
                             font=("Britannic", 15, "bold"), fg="seagreen")
    initial_label.pack(pady=10, padx=20)

    enter_reward_button = tk.Button(initial_frame, text="Enter Reward",
                                    command=lambda: show_reward_frame(root),
                                    bg="darkseagreen", font=("Britannic", 12, "bold"), fg="seagreen", bd=3)
    enter_reward_button.pack(pady=10)

    skip_reward_button = tk.Button(initial_frame, text="Skip Reward",
                                   command=lambda: update_progress(root, None),
                                   bg="darkseagreen", font=("Britannic", 12, "bold"), fg="seagreen", bd=3)
    skip_reward_button.pack(pady=10)


# If the user chooses to set up a reward, the reward entry shows up.
def show_reward_frame(root):
    clear_widgets(root)

    reward_frame = tk.Frame(root, bg="cornsilk", bd=5)
    reward_frame.place(relx=0.5, rely=0.5, anchor="center")

    reward_label = tk.Label(reward_frame, text="Enter your reward:", bg="cornsilk",
                            font=("Britannic", 15, "bold"), fg="seagreen")
    reward_label.pack(pady=10, padx=20)

    reward_entry = tk.Entry(reward_frame, width=30, font=("Britannic", 12, "normal"), fg="seagreen", bd=3)
    reward_entry.pack(pady=5)

    submit_button = tk.Button(reward_frame, text="Submit", command=lambda: submit_reward(root, reward_entry),
                              bg="darkseagreen", font=("Britannic", 12, "bold"), fg="seagreen", bd=3)
    submit_button.pack(pady=10)


# The entered reward is being submitted.
def submit_reward(root, entry):
    reward = entry.get()
    update_progress(root, reward)


# Progress bar function is used as a time tracker (duration: 10 seconds).
def update_progress(root, reward):
    clear_widgets(root)
    progress_frame = tk.Frame(root, bg="darkseagreen")
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

    def progress():
        for i in range(101):
            progress_var.set(i)
            root.update_idletasks()
            root.after(100)
        start_task_manager(root, reward)

    root.after(0, progress)


# The task manager allows the user to enter up to ten tasks with a list.
def start_task_manager(root, reward):
    clear_widgets(root)
    list_tasks = []
    list_task_entries_frame = tk.Frame(root, bg="darkseagreen")
    list_task_entries_frame.pack(pady=40)

    def add_task_entries():
        for _ in range(10):
            entry = tk.Entry(list_task_entries_frame, width=30)
            entry.pack(pady=7)
            entry.bind("<Return>", focus_next_entry)
            list_tasks.append(entry)

    def focus_next_entry(event):
        current_entry = event.widget
        current_index = list_tasks.index(current_entry)
        next_index = (current_index + 1) % len(list_tasks)
        list_tasks[next_index].focus_set()

    add_task_entries()

    pick_random_task_button = tk.Button(root, text="Pick Random Task", font=("Britannic", 15, "bold"),
                                        fg="seagreen", bg="cornsilk",
                                        command=lambda: pick_random_task(list_tasks, reward))
    pick_random_task_button.pack(pady=5)


# The Daily Task Generator randomly picks one task after the other until all ten are completed.
def pick_random_task(list_tasks, reward):
    available_tasks = [entry.get() for entry in list_tasks if entry.get().strip()]
    if available_tasks:
        selected_task = random.choice(available_tasks)
        for entry in list_tasks:
            if entry.get() == selected_task:
                entry.delete(0, tk.END)
        messagebox.showinfo("Next Task", f"Next Task: {selected_task}")
    else:
        show_reward_message(reward)


# If a reward was previously entered, it shows up at the end.
def show_reward_message(reward):
    if reward:
        messagebox.showinfo("Reward", f"Congratulations! You've completed all tasks.\nYour reward: {reward}")
    else:
        messagebox.showinfo("Reward", "Congratulations! You've completed all tasks.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Daily Task Generator")
    root.geometry("600x600")
    root.resizable(False, False)
    root.config(bg="darkseagreen")

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)

    setup_initial_frame(root)

    root.mainloop()
