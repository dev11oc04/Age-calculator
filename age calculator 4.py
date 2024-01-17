#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      hp
#
# Created:     19/06/2023
# Copyright:   (c) hp 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import datetime
import tkinter as tk
from tkinter import ttk
import ephem
import random
import requests
from tkcalendar import DateEntry

# Define colors
app_background = "#F0F0F0"
heading_background = "#FF9F00"
heading_fg = "white"

# Create the main window
window = tk.Tk()
window.geometry("620x780")
window.title("Age Calculator App")
window.configure(bg=app_background)

# Create a new window for displaying astrological information
astro_window = None
future_window = None

# Create the heading label
heading_label = tk.Label(window, text="Age Calculator App", font=("Arial", 20, "bold"), bg=heading_background, fg=heading_fg)
heading_label.pack(pady=20)

# Create the personal information section
personal_info_frame = tk.Frame(window, bg=app_background)
personal_info_frame.pack(pady=20)

personal_info_label = tk.Label(personal_info_frame, text="Personal Information", font=("Arial", 16, "bold"), bg=app_background)
personal_info_label.grid(column=0, row=0, columnspan=2, pady=10)

name_label = tk.Label(personal_info_frame, text="Enter a name", font=("Arial", 12), bg=app_background)
name_label.grid(column=0, row=1, pady=5)
birthdate_label = tk.Label(personal_info_frame, text="Enter your birthdate", font=("Arial", 12), bg=app_background)
birthdate_label.grid(column=0, row=2, pady=5)
time_of_birth_label = tk.Label(personal_info_frame, text="Enter your time of birth", font=("Arial", 12), bg=app_background)
time_of_birth_label.grid(column=0, row=3, pady=5)
gender_label = tk.Label(personal_info_frame, text="Gender", font=("Arial", 12), bg=app_background)
gender_label.grid(column=0, row=4, pady=5)
current_date_label = tk.Label(personal_info_frame, text="Current Date (YYYY-MM-DD)", font=("Arial", 12), bg=app_background)
current_date_label.grid(column=0, row=5, pady=5)

name_entry = tk.Entry(personal_info_frame, font=("Arial", 12))
name_entry.grid(column=1, row=1, pady=5)
birthdate_entry = DateEntry(personal_info_frame, width=12, background="darkblue", foreground="white", font=("Arial", 12), date_pattern="yyyy-mm-dd")
birthdate_entry.grid(column=1, row=2, pady=5)
time_of_birth_entry = tk.Entry(personal_info_frame, font=("Arial", 12))
time_of_birth_entry.grid(column=1, row=3, pady=5)

gender_var = tk.StringVar(value="Male")
male_radio = tk.Radiobutton(personal_info_frame, text="Male", variable=gender_var, value="Male", font=("Arial", 12), bg=app_background)
male_radio.grid(column=1, row=4, sticky="W", pady=5)
female_radio = tk.Radiobutton(personal_info_frame, text="Female", variable=gender_var, value="Female", font=("Arial", 12), bg=app_background)
female_radio.grid(column=1, row=4, sticky="E", pady=5)
others_radio = tk.Radiobutton(personal_info_frame, text="Others", variable=gender_var, value="Others", font=("Arial", 12), bg=app_background)
others_radio.grid(column=1, row=5, pady=5)

current_date_entry = tk.Entry(personal_info_frame, font=("Arial", 12))
current_date_entry.insert(tk.END, datetime.date.today().strftime("%Y-%m-%d"))
current_date_entry.grid(column=1, row=6, pady=5)

# Create the function to calculate age and display information
class Person:
    def __init__(self, name, birthdate, time_of_birth, gender):
        self.name = name
        self.birthdate = birthdate
        self.time_of_birth = time_of_birth
        self.gender = gender

    def age(self, current_date):
        birthdate = self.birthdate
        age = current_date - birthdate
        years = age.days // 365
        months = (age.days % 365) // 30
        days = (age.days % 365) % 30
        return years, months, days

    def zodiac_sign(self):
        birthdate = ephem.Date(self.birthdate)
        sun = ephem.Sun()
        sun.compute(birthdate)
        zodiac_sign = ephem.constellation(sun)[1]
        return zodiac_sign

    def is_birthday(self, current_date):
        return (self.birthdate.month, self.birthdate.day) == (current_date.month, current_date.day)

    def get_astrological_info(self):
        birthdate = self.birthdate
        day_of_week = birthdate.strftime("%A")
        astrological_info = f"On your birthdate, {day_of_week}, you possess the following qualities: ...\n"
        # Add more astrological information based on the birthdate and zodiac sign
        planet_positions = self.get_planet_positions()
        astrological_info += "Planet Positions:\n"
        for planet, position in planet_positions.items():
            astrological_info += f"{planet}: {position}\n"
        return astrological_info

    def get_planet_positions(self):
        birth_datetime = datetime.datetime(
            int(self.birthdate.year), int(self.birthdate.month), int(self.birthdate.day), 12, 0, 0
        )
        planet_positions = {}
        planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
        for planet_name in planets:
            planet = getattr(ephem, planet_name)()
            planet.compute(birth_datetime)
            const = ephem.constellation(planet)
            planet_positions[planet_name] = const[1]
        return planet_positions

    def get_ancient_incident(self):
        birthdate = self.birthdate.strftime("%B %d")
        url = f"https://en.wikipedia.org/api/rest_v1/page/random/summary?births={birthdate}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            title = data.get("title")
            description = data.get("extract")
            if title and description:
                return f"{title}\n\n{description}"
        return "No ancient incident found for this birthdate."

    def get_future_prediction(self):
        random.seed(self.name)  # Set the seed based on the name for consistent predictions
        predictions = [
            "You will travel to an exotic location within the next year.",
            "You will meet someone famous in the near future.",
            "A great opportunity will come your way in the coming months.",
            "You will achieve a personal milestone in the next few weeks.",
            "You will receive unexpected good news in the next month."
        ]
        return random.choice(predictions)


def calculate_age():
    name = name_entry.get()
    gender = gender_var.get()
    birthdate = datetime.datetime.strptime(birthdate_entry.get(), "%Y-%m-%d").date()
    current_date = datetime.datetime.strptime(current_date_entry.get(), "%Y-%m-%d").date()

    person = Person(name, birthdate, "", gender)
    years, months, days = person.age(current_date)

    age_result_label.config(text=f"{name} is {years} years, {months} months, and {days} days old.")

    zodiac_sign_label.config(text=f"Zodiac Sign: {person.zodiac_sign()}")

    if person.is_birthday(current_date):
        birthday_label.config(text="Happy birthday!")
    else:
        birthday_label.config(text="")

    if astro_window is not None:
        astro_window.destroy()

    if future_window is not None:
        future_window.destroy()

    astro_button.config(state="normal")
    future_button.config(state="normal")


def show_astro_info():
    name = name_entry.get()
    gender = gender_var.get()
    birthdate = datetime.datetime.strptime(birthdate_entry.get(), "%Y-%m-%d").date()

    person = Person(name, birthdate, "", gender)
    astro_info = person.get_astrological_info()

    global astro_window
    astro_window = tk.Toplevel(window)
    astro_window.geometry("500x400")
    astro_window.title("Astrological Information")

    astro_info_label = tk.Label(astro_window, text=astro_info, font=("Arial", 12), bg=app_background)
    astro_info_label.pack(pady=20)

    astro_button.config(state="disabled")


def show_future_prediction():
    name = name_entry.get()
    gender = gender_var.get()
    birthdate = datetime.datetime.strptime(birthdate_entry.get(), "%Y-%m-%d").date()

    person = Person(name, birthdate, "", gender)
    prediction = person.get_future_prediction()

    global future_window
    future_window = tk.Toplevel(window)
    future_window.geometry("500x300")
    future_window.title("Future Prediction")

    prediction_label = tk.Label(future_window, text=prediction, font=("Arial", 16, "bold"), bg=app_background)
    prediction_label.pack(pady=20)

    future_button.config(state="disabled")


# Create the age calculation section
age_calc_frame = tk.Frame(window, bg=app_background)
age_calc_frame.pack(pady=20)

age_calc_label = tk.Label(age_calc_frame, text="Age Calculation", font=("Arial", 16, "bold"), bg=app_background)
age_calc_label.grid(column=0, row=0, columnspan=2, pady=10)

calculate_button = ttk.Button(age_calc_frame, text="Calculate Age", command=calculate_age)
calculate_button.grid(column=0, row=1, columnspan=2, pady=10)

age_result_label = tk.Label(age_calc_frame, text="", font=("Arial", 14), bg=app_background)
age_result_label.grid(column=0, row=2, columnspan=2, pady=5)

zodiac_sign_label = tk.Label(age_calc_frame, text="", font=("Arial", 14), bg=app_background)
zodiac_sign_label.grid(column=0, row=3, columnspan=2, pady=5)

birthday_label = tk.Label(age_calc_frame, text="", font=("Arial", 14), bg=app_background)
birthday_label.grid(column=0, row=4, columnspan=2, pady=5)

# Create the buttons for displaying astrological information and future prediction
astro_button = ttk.Button(age_calc_frame, text="Show Astrological Info", command=show_astro_info)
astro_button.grid(column=0, row=5, pady=10)

future_button = ttk.Button(age_calc_frame, text="Get Future Prediction", command=show_future_prediction)
future_button.grid(column=1, row=5, pady=10)

# Run the main window loop
window.mainloop()