import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import numpy as np
import joblib

# Load your model
model = joblib.load("model.pkl")


# ============================================================
# MAIN WINDOW CLASS
# ============================================================
class PlacementPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Placement Prediction App")

        self.geometry("650x650")
        self.minsize(650, 650)
        self.resizable(True, True)

        # Load original background image
        try:
            self.original_bg = Image.open("bg.jpg")
            self.bg_img = self.original_bg.copy()
            self.bg_photo = ImageTk.PhotoImage(self.bg_img)
        except Exception as e:
            print("Error loading background image:", e)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.pack_propagate(False)

        self.frames = {}
        for Page in (HomePage, PredictPage):
            frame = Page(container, self)
            self.frames[Page] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame(HomePage)
        self.bind("<Configure>", self.resize_background)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def resize_background(self, event):
        try:
            new_w = event.width
            new_h = event.height

            resized = self.original_bg.resize((new_w, new_h), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized)

            for frame in self.frames.values():
                if hasattr(frame, "bg_label"):
                    frame.bg_label.config(image=self.bg_photo)

        except:
            pass


# ============================================================
# HOME PAGE
# ============================================================
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.bg_label = tk.Label(self, image=controller.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        title = tk.Label(self, text="🎓 Placement Prediction",
                         font=("Arial", 28, "bold"), bg="#ffffff")
        title.pack(pady=150)

        start_btn = tk.Button(self, text="Go to Prediction Page",
                              command=lambda: controller.show_frame(PredictPage),
                              font=("Arial", 16), bg="#4CAF50",
                              fg="white", padx=20, pady=10)
        start_btn.pack()


# ============================================================
# PREDICTION PAGE
# ============================================================
class PredictPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.bg_label = tk.Label(self, image=controller.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        title = tk.Label(self, text="Enter Student Details",
                         font=("Arial", 22, "bold"), bg="#ffffff")
        title.pack(pady=10)

        form = tk.Frame(self, bg="#ffffff")
        form.pack(pady=10)

        # EXACT FEATURE ORDER FOR MODEL INPUT
        labels = [
            "CGPA",
            "Internships",
            "Projects",
            "Workshops/Certifications",
            "Aptitude Test Score",
            "Soft Skills Rating",
            "Extracurricular Activities",
            "Placement Training",
            "SSC Marks",
            "HSC Marks",
        ]

        self.widgets = []

        for i, text in enumerate(labels):
            tk.Label(form, text=text, font=("Arial", 12),
                     bg="#ffffff").grid(row=i, column=0, pady=5, padx=5)

            if text in ["Extracurricular Activities", "Placement Training"]:
                combo = ttk.Combobox(form, values=["Yes", "No"], state="readonly", width=18)
                combo.grid(row=i, column=1, pady=5)
                combo.set("No")
                self.widgets.append(combo)

            else:
                entry = tk.Entry(form, font=("Arial", 12))
                entry.grid(row=i, column=1, pady=5)
                self.widgets.append(entry)

        predict_btn = tk.Button(self, text="Predict Placement",
                                command=self.predict_result,
                                font=("Arial", 16, "bold"), bg="#4CAF50",
                                fg="white", padx=20, pady=10)
        predict_btn.pack(pady=20)

        self.result_label = tk.Label(self, text="",
                                     font=("Arial", 18, "bold"), bg="#ffffff")
        self.result_label.pack(pady=10)

        back_btn = tk.Button(self, text="← Back to Home",
                             command=lambda: controller.show_frame(HomePage),
                             font=("Arial", 14), bg="#f44336", fg="white",
                             padx=15, pady=5)
        back_btn.pack(pady=10)

    def predict_result(self):
        try:
            vals = []

            for widget in self.widgets:

                if isinstance(widget, ttk.Combobox):
                    vals.append(1 if widget.get() == "Yes" else 0)

                else:
                    text_val = widget.get().strip()
                    if text_val == "":
                        raise ValueError("Some fields are empty!")
                    vals.append(float(text_val))

            final_input = [vals]   # Model expects 2D array

            print("Model Input:", vals)

            prediction = model.predict(final_input)[0]

            if prediction == 1:
                result_text = f"🎉 Student is Likely to be Placed"
            else:
                result_text = f"⚠ Student is Unlikely to be Placed"

            self.result_label.config(text=result_text)

        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            print("Prediction Error:", e)


# ============================================================
# RUN APP
# ============================================================
app = PlacementPage()
app.mainloop()