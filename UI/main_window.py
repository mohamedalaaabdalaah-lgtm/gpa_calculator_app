import customtkinter as ctk

# link all backend files
from gpa_calculator_app.logic.gpa_engine import (
    calculate_required_gpa,
    calculate_cumulative_gpa,
    calculate_semester_gpa
)
from gpa_calculator_app.logic.scale_manager import (
    check_scale,
    get_grade_points
)
from gpa_calculator_app.logic.data_manager import (
    load_user_data,
    save_user_data
)

# APP SETTINGS
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


# 1. GPA CALCULATOR UI
class GPACalculatorUIFrame(ctk.CTkFrame):

    def __init__(self, parent, scale_name, scale_type="standard", custom_scale_dict=None, on_edit_custom=None):
        super().__init__(parent)

        self.scale_type = scale_type
        self.custom_scale_dict = custom_scale_dict or {}
        self.on_edit_custom = on_edit_custom  # Callback لتعديل الـ Custom Scale

        # قراءة الداتا المحفوظة من الفايل 
        all_data = load_user_data()
        self.courses_list = all_data.get(self.scale_type, [])

        # window size / grid setup
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # INPUT PANEL
        self.input_frame = ctk.CTkFrame(self, corner_radius=8)
        self.input_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

        # Course Name Label
        ctk.CTkLabel(
            self.input_frame,
            text="Course Name:",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=8, pady=8, sticky="w")

        # Input Course Name
        self.entry_name = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="e.g. Physics",
            width=140
        )
        self.entry_name.grid(row=0, column=1, padx=8, pady=8)

        # Credit Hours Label
        ctk.CTkLabel(
            self.input_frame,
            text="Credit Hours:",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=2, padx=8, pady=8, sticky="w")

        # Input Credit Hours
        self.entry_hours = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="e.g. 3",
            width=80
        )
        self.entry_hours.grid(row=0, column=3, padx=8, pady=8)

        # Grade Label
        ctk.CTkLabel(
            self.input_frame,
            text="Grade:",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=4, padx=8, pady=8, sticky="w")

        # Input Grade
        self.combo_grade = ctk.CTkOptionMenu(
            self.input_frame,
            values=["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"],
            width=90
        )
        self.combo_grade.grid(row=0, column=5, padx=8, pady=8)

        # Add Course Button 
        self.btn_add = ctk.CTkButton(
            self.input_frame,
            text="+ Add Course",
            font=("Arial", 12, "bold"),
            command=self.add_course
        )
        self.btn_add.grid(row=0, column=6, padx=8, pady=8)

        # Edit Scale Button (يظهر فقط في الـ Custom Scale)
        if self.scale_type == "custom" and self.on_edit_custom:
            self.btn_edit_scale = ctk.CTkButton(
                self.input_frame,
                text="Edit Scale",
                font=("Arial", 12, "bold"),
                fg_color="#6c757d",
                hover_color="#5a6268",
                width=80,
                command=self.on_edit_custom
            )
            self.btn_edit_scale.grid(row=0, column=7, padx=8, pady=8)

        # ERROR LABEL (تمت إضافته لمنع الخطأ عند الاستدعاء)
        self.lbl_error = ctk.CTkLabel(
            self.input_frame,
            text="",
            text_color="#FF4D4D",
            font=("Arial", 11, "bold")
        )
        self.lbl_error.grid(row=1, column=0, columnspan=8, padx=8, pady=(0, 5), sticky="w")

        # COURSES TABLE
        self.table_frame = ctk.CTkScrollableFrame(
            self,
            label_text=f"Added Courses ({scale_name})"
        )
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.table_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Table Headers
        headers = ["Course Name", "Credit Hours", "Grade", "Action"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                text_color="#888888"
            ).grid(row=0, column=col, pady=5)

        # SUMMARY BAR
        self.summary_frame = ctk.CTkFrame(self, corner_radius=8, fg_color="#1f538d")
        self.summary_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        self.summary_frame.grid_columnconfigure((0, 1), weight=1)

        self.lbl_total_hours = ctk.CTkLabel(
            self.summary_frame,
            text="Total Hours: 0",
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        self.lbl_total_hours.grid(row=0, column=0, pady=12)

        self.lbl_gpa = ctk.CTkLabel(
            self.summary_frame,
            text="GPA: 0.00",
            font=("Arial", 16, "bold"),
            text_color="white"
        )
        self.lbl_gpa.grid(row=0, column=1, pady=12)

        # Refresh
        self.refresh_table_and_summary()

    def add_course(self):
        # مسح أي خطأ سابق
        self.lbl_error.configure(text="")

        name = self.entry_name.get().strip()
        hours_raw = self.entry_hours.get().strip()
        grade = self.combo_grade.get()

        # empty input 
        if not name or not hours_raw:
            self.lbl_error.configure(text="Please enter both course name and credit hours.")
            return

        try:
            hours = float(hours_raw)
            if hours <= 0:
                self.lbl_error.configure(text="Credit hours must be greater than 0.")
                return
            elif hours > 6:
                self.lbl_error.configure(text="Maximum credit hours per course is 6 hours.")
                return
        except ValueError:
            self.lbl_error.configure(text="Credit hours must be a valid number.")
            return

        # add to list
        self.courses_list.append({"name": name, "hours": hours, "grade": grade})

        # save after addition
        self.save_to_json()

        # clear entries
        self.entry_name.delete(0, 'end')
        self.entry_hours.delete(0, 'end')
        self.refresh_table_and_summary()

    def delete_course(self, index):
        self.courses_list.pop(index)
        self.save_to_json()
        self.refresh_table_and_summary()

    def save_to_json(self):
        all_data = load_user_data()
        all_data[self.scale_type] = self.courses_list
        save_user_data(all_data)

    def refresh_table_and_summary(self):
        # delete old rows
        for widget in self.table_frame.winfo_children():
            grid_info = widget.grid_info()
            if "row" in grid_info and int(grid_info["row"]) > 0:
                widget.destroy()

        # render new rows
        for idx, course in enumerate(self.courses_list, start=1):
            ctk.CTkLabel(self.table_frame, text=course["name"]).grid(row=idx, column=0, pady=4)
            ctk.CTkLabel(self.table_frame, text=str(course["hours"])).grid(row=idx, column=1, pady=4)
            ctk.CTkLabel(self.table_frame, text=course["grade"]).grid(row=idx, column=2, pady=4)
            
            ctk.CTkButton(
                self.table_frame,
                text="Delete",
                width=60,
                fg_color="#a83232",
                hover_color="#7a2323",
                command=lambda i=idx-1: self.delete_course(i)
            ).grid(row=idx, column=3, pady=4)

        # update total hours
        total_hours = sum(float(course["hours"]) for course in self.courses_list)
        hours_display = int(total_hours) if total_hours.is_integer() else total_hours
        self.lbl_total_hours.configure(text=f"Total Hours: {hours_display}")

        # update GPA
        gpa = calculate_semester_gpa(self.courses_list, self.scale_type, self.custom_scale_dict)
        self.lbl_gpa.configure(text=f"GPA: {gpa:.2f}")


# 2. CUSTOM SCALE CONFIGURATION
class CustomScaleUIFrame(ctk.CTkFrame):

    def __init__(self, parent, on_save):
        super().__init__(parent)

        self.on_save = on_save
        self.entries = []

        # TITLE
        ctk.CTkLabel(
            self, text="Custom Scale Configurations", font=("Arial", 18, "bold")
        ).pack(pady=15)

        # SCROLL FRAME
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=400, height=300)
        self.scroll_frame.pack(
            fill="both", expand=True, padx=20, pady=10
        )

        # HEADERS
        ctk.CTkLabel(
            self.scroll_frame, text="Grade", font=("Arial", 13, "bold")
        ).grid(row=0, column=0, padx=20, pady=5)

        ctk.CTkLabel(
            self.scroll_frame, text="Point Value", font=("Arial", 13, "bold")
        ).grid(row=0, column=1, padx=20, pady=5)

        # DEFAULT GRADES
        grades = [
            ("A+", "4.0"),
            ("A", "3.75"),
            ("A-", "3.5"),
            ("B+", "3.25"),
            ("B", "3.0"),
            ("B-", "2.75"),
            ("C+", "2.5"),
            ("C", "2.0"),
            ("D", "1.0"),
            ("F", "0.0"),
        ]

        # CREATE GRADE ROWS
        for idx, (grade, value) in enumerate(grades, start=1):
            ctk.CTkLabel(
                self.scroll_frame, text=grade, font=("Arial", 14, "bold")
            ).grid(row=idx, column=0, padx=20, pady=6)

            entry = ctk.CTkEntry(self.scroll_frame, width=100)
            entry.insert(0, value)
            entry.grid(row=idx, column=1, padx=20, pady=6)

            self.entries.append(entry)

        # ERROR LABEL
        self.lbl_error = ctk.CTkLabel(
            self, text="", text_color="#FF4D4D", font=("Arial", 12, "bold")
        )
        self.lbl_error.pack(pady=(0, 5))

        # SAVE BUTTON
        ctk.CTkButton(
            self,
            text="Save Custom Scale",
            font=("Arial", 13, "bold"),
            fg_color="#28a745",
            hover_color="#1e7e34",
            command=self.save_scale,
        ).pack(pady=(0, 15))

    def save_scale(self):
        self.lbl_error.configure(text="")

        try:
            custom_scale = {}
            grades = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "D", "F"]

            for grade, entry in zip(grades, self.entries):
                raw_val = entry.get().strip()

                if not raw_val:
                    self.lbl_error.configure(text="Please fill in all grade point values.")
                    return

                value = float(raw_val)

                if value < 0 or value > 10:
                    self.lbl_error.configure(text="Point values must be between 0.0 and 10.0.")
                    return

                custom_scale[grade] = value

            self.lbl_error.configure(text="")
            self.on_save(custom_scale)

        except ValueError:
            self.lbl_error.configure(text="Please enter valid numerical values for points.")


# 3. TARGET GPA PAGE
class TargetGPAUIFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        # TITLE
        ctk.CTkLabel(
            self, text="Target GPA", font=("Arial", 22, "bold")
        ).grid(row=0, column=0, pady=(25, 5))

        ctk.CTkLabel(
            self, text="Calculate the GPA you need to reach your target.", font=("Arial", 13)
        ).grid(row=1, column=0, pady=(0, 20))

        # INPUT FRAME
        self.input_frame = ctk.CTkFrame(self, corner_radius=10)
        self.input_frame.grid(row=2, column=0, padx=80, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        # CURRENT GPA
        ctk.CTkLabel(
            self.input_frame, text="Current GPA:", font=("Arial", 13, "bold")
        ).grid(row=0, column=0, padx=15, pady=12, sticky="w")

        self.entry_current_gpa = ctk.CTkEntry(self.input_frame, placeholder_text="e.g. 3.20")
        self.entry_current_gpa.grid(row=0, column=1, padx=15, pady=12, sticky="ew")

        # COMPLETED HOURS
        ctk.CTkLabel(
            self.input_frame, text="Completed Credit Hours:", font=("Arial", 13, "bold")
        ).grid(row=1, column=0, padx=15, pady=12, sticky="w")

        self.entry_completed_hours = ctk.CTkEntry(self.input_frame, placeholder_text="e.g. 60")
        self.entry_completed_hours.grid(row=1, column=1, padx=15, pady=12, sticky="ew")

        # TARGET GPA
        ctk.CTkLabel(
            self.input_frame, text="Target GPA:", font=("Arial", 13, "bold")
        ).grid(row=2, column=0, padx=15, pady=12, sticky="w")

        self.entry_target_gpa = ctk.CTkEntry(self.input_frame, placeholder_text="e.g. 3.50")
        self.entry_target_gpa.grid(row=2, column=1, padx=15, pady=12, sticky="ew")

        # FUTURE HOURS
        ctk.CTkLabel(
            self.input_frame, text="Target Credit Hour (completed + future):", font=("Arial", 13, "bold")
        ).grid(row=3, column=0, padx=15, pady=12, sticky="w")

        self.entry_future_hours = ctk.CTkEntry(self.input_frame, placeholder_text="e.g. 15")
        self.entry_future_hours.grid(row=3, column=1, padx=15, pady=12, sticky="ew")

        # CALCULATE BUTTON
        ctk.CTkButton(
            self.input_frame,
            text="Calculate Required GPA",
            font=("Arial", 13, "bold"),
            fg_color="#28a745",
            hover_color="#1e7e34",
            command=self.calculate_target
        ).grid(row=4, column=0, columnspan=2, padx=15, pady=20)

        # RESULT
        self.result_label = ctk.CTkLabel(
            self,
            text="Required GPA: --",
            font=("Arial", 20, "bold"),
            text_color="#28a745"
        )
        self.result_label.grid(row=3, column=0, pady=25)

    def calculate_target(self):
        try:
            current_gpa = float(self.entry_current_gpa.get())
            completed_hours = float(self.entry_completed_hours.get())
            target_gpa = float(self.entry_target_gpa.get())
            future_hours = float(self.entry_future_hours.get())

            if completed_hours < 0 or future_hours <= 0:
                raise ValueError
            if current_gpa < 0 or current_gpa > 4.0 or target_gpa < 0 or target_gpa > 4.0:
                raise ValueError

            req_gpa = calculate_required_gpa(current_gpa, completed_hours, target_gpa, future_hours)

            if req_gpa > 4.0:
                self.result_label.configure(
                    text=f"Required GPA: {req_gpa:.2f} (Impossible: Exceeds 4.0)",
                    text_color="#ff5555"
                )
            elif req_gpa <= 0:
                self.result_label.configure(
                    text="Target already achieved!",
                    text_color="#28a745",
                )
            else:
                self.result_label.configure(
                    text=f"Required GPA: {req_gpa:.2f}",
                    text_color="#28a745"
                )

        except ValueError:
            self.result_label.configure(
                text="Please enter valid numbers.",
                text_color="#ff5555"
            )


# 4. CUMULATIVE GPA PAGE
class CumulativeGPAUIFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.semesters = []

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # TITLE
        ctk.CTkLabel(
            self, text="Cumulative GPA", font=("Arial", 22, "bold")
        ).grid(row=0, column=0, pady=(20, 5))

        ctk.CTkLabel(
            self, text="Add your semesters and calculate your cumulative GPA.", font=("Arial", 13)
        ).grid(row=1, column=0, pady=(0, 15))

        # MAIN FRAME
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=2, column=0, sticky="nsew", padx=50, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # HEADERS 
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(header_frame, text="Semester", font=("Arial", 13, "bold")).grid(row=0, column=0)
        ctk.CTkLabel(header_frame, text="GPA", font=("Arial", 13, "bold")).grid(row=0, column=1)
        ctk.CTkLabel(header_frame, text="Credit Hours", font=("Arial", 13, "bold")).grid(row=0, column=2)
        ctk.CTkLabel(header_frame, text="Action", font=("Arial", 13, "bold")).grid(row=0, column=3)

        # SEMESTERS FRAME
        self.semesters_frame = ctk.CTkScrollableFrame(self.main_frame, height=180)
        self.semesters_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.semesters_frame.grid_columnconfigure(0, weight=1)

        # BUTTONS CONTAINER
        buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, pady=10)

        ctk.CTkButton(
            buttons_frame,
            text="+ Add Semester",
            font=("Arial", 13, "bold"),
            fg_color="#28a745",
            command=self.add_semester
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            buttons_frame,
            text="Calculate Cumulative GPA",
            font=("Arial", 13, "bold"),
            fg_color="#28a745",
            command=self.calculate_cumulative
        ).pack(side="left", padx=10)

        # RESULT LABEL 
        self.result_label = ctk.CTkLabel(
            self,
            text="Cumulative GPA: --",
            font=("Arial", 20, "bold"),
            text_color="#28a745"
        )
        self.result_label.grid(row=3, column=0, pady=(5, 15))

        self.add_semester()

    def add_semester(self):
        semester_number = len(self.semesters) + 1

        row_frame = ctk.CTkFrame(self.semesters_frame, fg_color="transparent")
        row_frame.grid(row=len(self.semesters), column=0, sticky="ew", pady=5)
        row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        lbl_name = ctk.CTkLabel(row_frame, text=f"Semester {semester_number}", font=("Arial", 12, "bold"))
        lbl_name.grid(row=0, column=0, padx=5)

        gpa_entry = ctk.CTkEntry(row_frame, placeholder_text="e.g. 3.40", width=100)
        gpa_entry.grid(row=0, column=1, padx=5)

        hours_entry = ctk.CTkEntry(row_frame, placeholder_text="e.g. 15", width=100)
        hours_entry.grid(row=0, column=2, padx=5)

        item = [gpa_entry, hours_entry, row_frame, lbl_name]
        del_btn = ctk.CTkButton(
            row_frame,
            text="Delete",
            width=60,
            fg_color="#a83232",
            hover_color="#7a2323",
            command=lambda: self.delete_semester(item)
        )
        del_btn.grid(row=0, column=3, padx=5)

        self.semesters.append(item)

    def delete_semester(self, item):
        if item in self.semesters:
            self.semesters.remove(item)
            item[2].destroy()
            
            for idx, sem in enumerate(self.semesters, start=1):
                sem[3].configure(text=f"Semester {idx}")

    def calculate_cumulative(self):
        if not self.semesters:
            self.result_label.configure(
                text="Please add at least one semester.",
                text_color="#ff5555"
            )
            return

        try:
            semesters_data = []
            for gpa_entry, hours_entry, _, _ in self.semesters:
                gpa_val = float(gpa_entry.get())
                hours_val = float(hours_entry.get())

                if gpa_val < 0 or hours_val <= 0 or gpa_val > 4.0:
                    raise ValueError

                semesters_data.append({
                    'gpa': gpa_val,
                    'hours': hours_val
                })

            cumulative_gpa = calculate_cumulative_gpa(semesters_data)

            self.result_label.configure(
                text=f"Cumulative GPA: {cumulative_gpa:.2f}",
                text_color="#28a745"
            )

        except ValueError:
            self.result_label.configure(
                text="Please enter valid positive (less than 4) numbers for GPA and credit hours.",
                text_color="#ff5555"
            )


# 5. MAIN WINDOW
class GPAMainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # WINDOW SETTINGS
        self.geometry("1100x650")
        self.minsize(950, 550)
        self.title("GPA Calculator")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.active_color = "#1f538d"
        self.inactive_color = "#3a3a3a"

        self.top_bar = ctk.CTkFrame(self, corner_radius=10)
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        self.top_bar.grid_columnconfigure(5, weight=1)

        # BUTTONS
        self.btn_standard = ctk.CTkButton(
            self.top_bar, text="Standard", height=40, font=("Arial", 13, "bold"),
            fg_color=self.inactive_color, command=self.show_standard
        )
        self.btn_standard.grid(row=0, column=0, padx=5, pady=8)

        self.btn_half = ctk.CTkButton(
            self.top_bar, text="Half-Point", height=40, font=("Arial", 13, "bold"),
            fg_color=self.inactive_color, command=self.show_half
        )
        self.btn_half.grid(row=0, column=1, padx=5, pady=8)

        self.btn_custom = ctk.CTkButton(
            self.top_bar, text="Custom Scale", height=40, font=("Arial", 13, "bold"),
            fg_color=self.inactive_color, command=self.show_custom
        )
        self.btn_custom.grid(row=0, column=2, padx=5, pady=8)

        self.btn_target = ctk.CTkButton(
            self.top_bar, text="Target GPA", height=40, font=("Arial", 13, "bold"),
            fg_color=self.inactive_color, command=self.show_target
        )
        self.btn_target.grid(row=0, column=3, padx=5, pady=8)

        self.btn_cumulative = ctk.CTkButton(
            self.top_bar, text="Cumulative GPA", height=40, font=("Arial", 13, "bold"),
            fg_color=self.inactive_color, command=self.show_cumulative
        )
        self.btn_cumulative.grid(row=0, column=4, padx=5, pady=8)

        # THEME
        self.theme_optionmenu = ctk.CTkOptionMenu(
            self.top_bar, values=["Dark", "Light"], height=35,
            font=("Arial", 12, "bold"), command=ctk.set_appearance_mode
        )
        self.theme_optionmenu.grid(row=0, column=6, padx=10, pady=8, sticky="e")

        # MAIN CONTAINER
        self.container = ctk.CTkFrame(self, corner_radius=10)
        self.container.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.custom_scale = {}

        # CREATE PAGES WITH SCALE TYPES
        self.frame_standard = GPACalculatorUIFrame(
            self.container, "Standard Scale", scale_type="standard"
        )

        self.frame_half = GPACalculatorUIFrame(
            self.container, "Half-Point Scale", scale_type="half_point"
        )

        self.frame_custom = CustomScaleUIFrame(
            self.container, self.save_custom_scale
        )

        self.frame_custom_gpa = GPACalculatorUIFrame(
            self.container, "Custom Scale", scale_type="custom", on_edit_custom=self.edit_custom_scale
        )

        self.frame_target = TargetGPAUIFrame(self.container)
        self.frame_cumulative = CumulativeGPAUIFrame(self.container)

        # SHOW DEFAULT PAGE
        self.show_standard()

    def hide_all_frames(self):
        self.frame_standard.grid_forget()
        self.frame_half.grid_forget()
        self.frame_custom.grid_forget()
        self.frame_custom_gpa.grid_forget()
        self.frame_target.grid_forget()
        self.frame_cumulative.grid_forget()

    def update_button_styles(self, active_btn):
        self.btn_standard.configure(fg_color=self.inactive_color)
        self.btn_half.configure(fg_color=self.inactive_color)
        self.btn_custom.configure(fg_color=self.inactive_color)
        self.btn_target.configure(fg_color=self.inactive_color)
        self.btn_cumulative.configure(fg_color=self.inactive_color)
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
        if self.custom_scale:
            self.show_custom_gpa()
        else:
            self.edit_custom_scale()

    def edit_custom_scale(self):
        self.hide_all_frames()
        self.frame_custom.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.update_button_styles(self.btn_custom)

    def save_custom_scale(self, custom_scale):
        self.custom_scale = custom_scale
        self.frame_custom_gpa.custom_scale_dict = custom_scale
        self.frame_custom_gpa.refresh_table_and_summary()
        self.show_custom_gpa()

    def show_custom_gpa(self):
        self.hide_all_frames()
        self.frame_custom_gpa.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.update_button_styles(self.btn_custom)

    def show_target(self):
        self.hide_all_frames()
        self.frame_target.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.update_button_styles(self.btn_target)

    def show_cumulative(self):
        self.hide_all_frames()
        self.frame_cumulative.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.update_button_styles(self.btn_cumulative)

    def on_close(self):
        self.destroy()


# run
if __name__ == "__main__":
    app = GPAMainWindow()
    app.mainloop()