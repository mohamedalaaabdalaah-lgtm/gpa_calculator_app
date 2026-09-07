import customtkinter as ctk

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class GPACalculatorUIFrame(ctk.CTkFrame):

  def __init__(self, parent, scale_name):
    super().__init__(parent)

    self.grid_rowconfigure(1, weight=1)
    self.grid_columnconfigure(0, weight=1)

    # 1. قسم إدخال بيانات المادة (Input Panel)
    self.input_frame = ctk.CTkFrame(self, corner_radius=8)
    self.input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    # اسم المادة
    ctk.CTkLabel(
        self.input_frame, text="Course Name:", font=("Arial", 12, "bold")
    ).grid(row=0, column=0, padx=8, pady=8, sticky="w")
    self.entry_name = ctk.CTkEntry(
        self.input_frame, placeholder_text="e.g. Physics", width=140
    )
    self.entry_name.grid(row=0, column=1, padx=8, pady=8)

    # عدد الساعات
    ctk.CTkLabel(
        self.input_frame, text="Credit Hours:", font=("Arial", 12, "bold")
    ).grid(row=0, column=2, padx=8, pady=8, sticky="w")
    self.entry_hours = ctk.CTkEntry(
        self.input_frame, placeholder_text="e.g. 3", width=80
    )
    self.entry_hours.grid(row=0, column=3, padx=8, pady=8)

    # التقدير الحرفي
    ctk.CTkLabel(
        self.input_frame, text="Grade:", font=("Arial", 12, "bold")
    ).grid(row=0, column=4, padx=8, pady=8, sticky="w")
    self.combo_grade = ctk.CTkOptionMenu(
        self.input_frame,
        values=["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"],
        width=90,
    )
    self.combo_grade.grid(row=0, column=5, padx=8, pady=8)

    # زر إضافة المادة
    self.btn_add = ctk.CTkButton(
        self.input_frame, text="+ Add Course", font=("Arial", 12, "bold")
    )
    self.btn_add.grid(row=0, column=6, padx=12, pady=8)

    # 2. جدول عرض المواد (Dummy Table Layout)
    self.table_frame = ctk.CTkScrollableFrame(
        self, label_text=f"Added Courses ({scale_name})"
    )
    self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    self.table_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

    # عناوين الجدول
    headers = ["Course Name", "Credit Hours", "Grade", "Action"]
    for col, h in enumerate(headers):
      ctk.CTkLabel(
          self.table_frame,
          text=h,
          font=("Arial", 12, "bold"),
          text_color="#888888",
      ).grid(row=0, column=col, pady=5)

    # عناصر تجريبية لرؤية تصميم الشكل فقط (Dummy Rows)
    dummy_data = [("Physics", "3", "A"), ("Maths", "4", "B+")]
    for idx, (name, hrs, gr) in enumerate(dummy_data, start=1):
      ctk.CTkLabel(self.table_frame, text=name).grid(row=idx, column=0, pady=4)
      ctk.CTkLabel(self.table_frame, text=hrs).grid(row=idx, column=1, pady=4)
      ctk.CTkLabel(self.table_frame, text=gr).grid(row=idx, column=2, pady=4)
      ctk.CTkButton(
          self.table_frame,
          text="Delete",
          width=60,
          fg_color="#a83232",
          hover_color="#7a2323",
      ).grid(row=idx, column=3, pady=4)

    # 3. شريط عرض النتائج السفلي (Summary Bar UI)
    self.summary_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#1f538d")
    self.summary_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
    self.summary_frame.grid_columnconfigure((0, 1, 2), weight=1)

    ctk.CTkLabel(
        self.summary_frame,
        text="Total Hours: 7",
        font=("Arial", 14, "bold"),
        text_color="white",
    ).grid(row=0, column=0, pady=12)

    ctk.CTkLabel(
        self.summary_frame,
        text="Total Points: 25.2",
        font=("Arial", 14, "bold"),
        text_color="white",
    ).grid(row=0, column=1, pady=12)

    ctk.CTkLabel(
        self.summary_frame,
        text="GPA: 3.60",
        font=("Arial", 16, "bold"),
        text_color="#00FFC2",
    ).grid(row=0, column=2, pady=12)


class CustomScaleUIFrame(ctk.CTkFrame):

  def __init__(self, parent):
    super().__init__(parent)

    ctk.CTkLabel(
        self, text="Custom Scale Configurations", font=("Arial", 18, "bold")
    ).pack(pady=15)

    self.scroll_frame = ctk.CTkScrollableFrame(self, width=400, height=300)
    self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

    ctk.CTkLabel(
        self.scroll_frame, text="Grade", font=("Arial", 13, "bold")
    ).grid(row=0, column=0, padx=20, pady=5)
    ctk.CTkLabel(
        self.scroll_frame, text="Point Value", font=("Arial", 13, "bold")
    ).grid(row=0, column=1, padx=20, pady=5)

    grades = [
        ("A+", "4.0"),
        ("A", "3.75"),
        ("B+", "3.5"),
        ("B", "3.0"),
        ("C+", "2.5"),
        ("C", "2.0"),
        ("D", "1.0"),
        ("F", "0.0"),
    ]
    for idx, (grade, val) in enumerate(grades, start=1):
      ctk.CTkLabel(
          self.scroll_frame, text=grade, font=("Arial", 14, "bold")
      ).grid(row=idx, column=0, padx=20, pady=6)
      entry = ctk.CTkEntry(self.scroll_frame, width=100)
      entry.insert(0, val)
      entry.grid(row=idx, column=1, padx=20, pady=6)

    ctk.CTkButton(
        self,
        text="Save Custom Scale",
        font=("Arial", 13, "bold"),
        fg_color="#28a745",
        hover_color="#1e7e34",
    ).pack(pady=15)


class GPAMainWindow(ctk.CTk):

  def __init__(self):
    super().__init__()
    self.geometry("950x650")
    self.minsize(850, 550)
    self.title("GPA Calculator")

    self.grid_rowconfigure(1, weight=1)
    self.grid_columnconfigure(0, weight=1)

    # 1. شريط الزراير العلوي
    self.top_bar = ctk.CTkFrame(self, corner_radius=10)
    self.top_bar.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
    self.top_bar.grid_columnconfigure(3, weight=1)

    self.active_color = "#1f538d"
    self.inactive_color = "#3a3a3a"

    self.btn_standard = ctk.CTkButton(
        self.top_bar,
        text="Standard (3.3)",
        height=40,
        font=("Arial", 13, "bold"),
        fg_color=self.inactive_color,
        command=self.show_standard,
    )
    self.btn_standard.grid(row=0, column=0, padx=8, pady=8)

    self.btn_half = ctk.CTkButton(
        self.top_bar,
        text="Half-Point (3.5)",
        height=40,
        font=("Arial", 13, "bold"),
        fg_color=self.inactive_color,
        command=self.show_half,
    )
    self.btn_half.grid(row=0, column=1, padx=8, pady=8)

    self.btn_custom = ctk.CTkButton(
        self.top_bar,
        text="Custom Scale",
        height=40,
        font=("Arial", 13, "bold"),
        fg_color=self.inactive_color,
        command=self.show_custom,
    )
    self.btn_custom.grid(row=0, column=2, padx=8, pady=8)

    self.theme_optionmenu = ctk.CTkOptionMenu(
        self.top_bar,
        values=["Dark", "Light"],
        height=35,
        font=("Arial", 12, "bold"),
        command=ctk.set_appearance_mode,
    )
    self.theme_optionmenu.grid(row=0, column=4, padx=10, pady=8, sticky="e")

    # 2. Main Container
    self.container = ctk.CTkFrame(self, corner_radius=10)
    self.container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
    self.container.grid_rowconfigure(0, weight=1)
    self.container.grid_columnconfigure(0, weight=1)

    # إطارات الشاشات
    self.frame_standard = GPACalculatorUIFrame(
        self.container, "Standard 3.3 Scale"
    )
    self.frame_half = GPACalculatorUIFrame(
        self.container, "Half-Point 3.5 Scale"
    )
    self.frame_custom = CustomScaleUIFrame(self.container)

    self.show_standard()

  def hide_all_frames(self):
    self.frame_standard.grid_forget()
    self.frame_half.grid_forget()
    self.frame_custom.grid_forget()

  def update_button_styles(self, active_btn):
    self.btn_standard.configure(fg_color=self.inactive_color)
    self.btn_half.configure(fg_color=self.inactive_color)
    self.btn_custom.configure(fg_color=self.inactive_color)
    active_btn.configure(fg_color=self.active_color)

  def show_standard(self):
    self.hide_all_frames()
    self.frame_standard.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    self.update_button_styles(self.btn_standard)

  def show_half(self):
    self.hide_all_frames()
    self.frame_half.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    self.update_button_styles(self.btn_half)

  def show_custom(self):
    self.hide_all_frames()
    self.frame_custom.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    self.update_button_styles(self.btn_custom)


if __name__ == "__main__":
  app = GPAMainWindow()
  app.mainloop()