import customtkinter as ctk

#link all backend files
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

    def __init__(self, parent, scale_name):
        super().__init__(parent)

        #window size
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # INPUT PANEL
        self.input_frame = ctk.CTkFrame(self,corner_radius=8)
        self.input_frame.grid(row=0,column=0,sticky="ew",padx=10,pady=10)

        # Course Name
        ctk.CTkLabel(
            self.input_frame,
            text="Course Name:",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=0,
            padx=8,
            pady=8,
            sticky="w"
        )

        #input course name
        self.entry_name = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="e.g. Physics",
            width=140
        )

        self.entry_name.grid(
            row=0,
            column=1,
            padx=8,
            pady=8
        )

        # Credit Hours
        ctk.CTkLabel(
            self.input_frame,
            text="Credit Hours:",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=2,
            padx=8,
            pady=8,
            sticky="w"
        )

        #input Credit Hour
        self.entry_hours = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="e.g. 3",
            width=80
        )

        self.entry_hours.grid(
            row=0,
            column=3,
            padx=8,
            pady=8
        )

        # Grade
        ctk.CTkLabel(
            self.input_frame,
            text="Grade:",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=4,
            padx=8,
            pady=8,
            sticky="w"
        )

        #input grade
        self.combo_grade = ctk.CTkOptionMenu(
            self.input_frame,
            values=[
                "A+",
                "A",
                "A-",
                "B+",
                "B",
                "B-",
                "C+",
                "C",
                "D",
                "F"
            ],
            width=90
        )

        self.combo_grade.grid(
            row=0,
            column=5,
            padx=8,
            pady=8
        )

        # Add Course Button
        self.btn_add = ctk.CTkButton(
            self.input_frame,
            text="+ Add Course",
            font=("Arial", 12, "bold")
        )

        self.btn_add.grid(
            row=0,
            column=6,
            padx=12,
            pady=8
        )

        # COURSES TABLE
        self.table_frame = ctk.CTkScrollableFrame(
            self,
            label_text=f"Added Courses ({scale_name})"
        )

        self.table_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=5
        )

        self.table_frame.grid_columnconfigure(
            (0, 1, 2, 3),
            weight=1
        )

        # Table Headers
        headers = [
            "Course Name",
            "Credit Hours",
            "Grade",
            "Action"
        ]

        for col, header in enumerate(headers):

            ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=("Arial", 12, "bold"),
                text_color="#888888"
            ).grid(
                row=0,
                column=col,
                pady=5
            )

        # dummy_data = [
        #     ("Physics", "3", "A"),
        #     ("Maths", "4", "B+")
        # ]

        # for idx, (name, hours, grade) in enumerate(
        #     dummy_data,
        #     start=1
        # ):

        #     ctk.CTkLabel(
        #         self.table_frame,
        #         text=name
        #     ).grid(
        #         row=idx,
        #         column=0,
        #         pady=4
        #     )

        #     ctk.CTkLabel(
        #         self.table_frame,
        #         text=hours
        #     ).grid(
        #         row=idx,
        #         column=1,
        #         pady=4
        #     )

        #     ctk.CTkLabel(
        #         self.table_frame,
        #         text=grade
        #     ).grid(
        #         row=idx,
        #         column=2,
        #         pady=4
        #     )

        #     ctk.CTkButton(
        #         self.table_frame,
        #         text="Delete",
        #         width=60,
        #         fg_color="#a83232",
        #         hover_color="#7a2323"
        #     ).grid(
        #         row=idx,
        #         column=3,
        #         pady=4
        #     )


        # SUMMARY BAR
        self.summary_frame = ctk.CTkFrame(self,corner_radius=8,fg_color="#1f538d")
        self.summary_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        self.summary_frame.grid_columnconfigure((0, 1, 2),weight=1)

        # Total Hours
        ctk.CTkLabel(
            self.summary_frame,
            text="Total Hours: 7",
            font=("Arial", 14, "bold"),
            text_color="white"
        ).grid(
            row=0,
            column=0,
            pady=12
        )

        # Total Points
        ctk.CTkLabel(
            self.summary_frame,
            text="Total Points: 25.2",
            font=("Arial", 14, "bold"),
            text_color="white"
        ).grid(
            row=0,
            column=1,
            pady=12
        )

        # GPA
        ctk.CTkLabel(
            self.summary_frame,
            text="GPA: 3.60",
            font=("Arial", 16, "bold"),
            text_color="#00FFC2"
        ).grid(
            row=0,
            column=2,
            pady=12
        )



# 2. CUSTOM SCALE CONFIGURATION
class CustomScaleUIFrame(ctk.CTkFrame):

    def __init__(self, parent, on_save):
        super().__init__(parent)

        # Function that will run after Save
        self.on_save = on_save

        # Store Entry widgets
        self.entries = []

        # TITLE
        ctk.CTkLabel(
            self,
            text="Custom Scale Configurations",
            font=("Arial", 18, "bold")
        ).pack(
            pady=15
        )

        # SCROLL FRAME
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            width=400,
            height=300
        )

        self.scroll_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # HEADERS
        ctk.CTkLabel(
            self.scroll_frame,
            text="Grade",
            font=("Arial", 13, "bold")
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=5
        )

        ctk.CTkLabel(
            self.scroll_frame,
            text="Point Value",
            font=("Arial", 13, "bold")
        ).grid(
            row=0,
            column=1,
            padx=20,
            pady=5
        )

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
            ("F", "0.0")
        ]

        # CREATE GRADE ROWS
        for idx, (grade, value) in enumerate(
            grades,
            start=1
        ):

            # Grade label
            ctk.CTkLabel(
                self.scroll_frame,
                text=grade,
                font=("Arial", 14, "bold")
            ).grid(
                row=idx,
                column=0,
                padx=20,
                pady=6
            )

            # Point value entry
            entry = ctk.CTkEntry(
                self.scroll_frame,
                width=100
            )

            entry.insert(
                0,
                value
            )

            entry.grid(
                row=idx,
                column=1,
                padx=20,
                pady=6
            )

            # Save entry in list
            self.entries.append(entry)

        # SAVE BUTTON
        ctk.CTkButton(
            self,
            text="Save Custom Scale",
            font=("Arial", 13, "bold"),
            fg_color="#28a745",
            hover_color="#1e7e34",
            command=self.save_scale
        ).pack(
            pady=15
        )

    # SAVE CUSTOM SCALE

    def save_scale(self):

        try:

            custom_scale = {}

            grades = [
                "A+",
                "A",
                "A-",
                "B+",
                "B",
                "B-",
                "C+",
                "C",
                "D",
                "F"
            ]

            # Get values from Entry widgets

            for grade, entry in zip(
                grades,
                self.entries
            ):

                value = float(
                    entry.get()
                )

                # go to dictionary ex: {"A+": 4.0, "A": 3.75, "B+": 3.5, ...}
                custom_scale[grade] = value

            # Send the scale to Main Window

            self.on_save(custom_scale)

        except ValueError:
            self.lbl_error = ctk.CTkLabel(self, text="", text_color="#FF4D4D", font=("Arial", 12, "bold"))
            self.lbl_error.pack(pady=5)
            self.lbl_error.configure(text="Please enter valid point values.")

#  TARGET GPA PAGE
class TargetGPAUIFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # TITLE
        ctk.CTkLabel(
            self,
            text="Target GPA",
            font=("Arial", 22, "bold")
        ).grid(
            row=0,
            column=0,
            pady=(25, 5)
        )

        ctk.CTkLabel(
            self,
            text="Calculate the GPA you need to reach your target.",
            font=("Arial", 13)
        ).grid(
            row=1,
            column=0,
            pady=(0, 20)
        )

        # INPUT FRAME
        self.input_frame = ctk.CTkFrame(
            self,
            corner_radius=10
        )

        self.input_frame.grid(
            row=2,
            column=0,
            padx=80,
            pady=10,
            sticky="ew"
        )

        self.input_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # CURRENT GPA
        ctk.CTkLabel(
            self.input_frame,
            text="Current GPA:",
            font=("Arial", 13, "bold")
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=12,
            sticky="w"
        )

        self.entry_current_gpa = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="e.g. 3.20"
        )

        self.entry_current_gpa.grid(
            row=0,
            column=1,
            padx=15,
            pady=12,
            sticky="ew"
        )

        # COMPLETED HOURS
        ctk.CTkLabel(
            self.input_frame,
            text="Completed Credit Hours:",
            font=("Arial", 13, "bold")
        ).grid(
            row=1,
            column=0,
            padx=15,
            pady=12,
            sticky="w"
        )

        self.entry_completed_hours = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="e.g. 60"
        )

        self.entry_completed_hours.grid(
            row=1,
            column=1,
            padx=15,
            pady=12,
            sticky="ew"
        )

        # TARGET GPA
        ctk.CTkLabel(
            self.input_frame,
            text="Target GPA:",
            font=("Arial", 13, "bold")
        ).grid(
            row=2,
            column=0,
            padx=15,
            pady=12,
            sticky="w"
        )

        self.entry_target_gpa = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="e.g. 3.50"
        )

        self.entry_target_gpa.grid(
            row=2,
            column=1,
            padx=15,
            pady=12,
            sticky="ew"
        )

        # FUTURE HOURS
        ctk.CTkLabel(
            self.input_frame,
            text="Future Credit Hours:",
            font=("Arial", 13, "bold")
        ).grid(
            row=3,
            column=0,
            padx=15,
            pady=12,
            sticky="w"
        )

        self.entry_future_hours = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="e.g. 15"
        )

        self.entry_future_hours.grid(
            row=3,
            column=1,
            padx=15,
            pady=12,
            sticky="ew"
        )

        # CALCULATE BUTTON
        ctk.CTkButton(
            self.input_frame,
            text="Calculate Required GPA",
            font=("Arial", 13, "bold"),
            command=self.calculate_target
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            padx=15,
            pady=20
        )

        # RESULT
        self.result_label = ctk.CTkLabel(
            self,
            text="Required GPA: --",
            font=("Arial", 20, "bold"),
            text_color="#00FFC2"
        )

        self.result_label.grid(
            row=3,
            column=0,
            pady=25
        )

    # CALCULATE TARGET GPA
    def calculate_target(self):

        try:
            current_gpa = float(self.entry_current_gpa.get())

            completed_hours = float(self.entry_completed_hours.get())

            target_gpa = float(self.entry_target_gpa.get())

            future_hours = float(self.entry_future_hours.get())

            if completed_hours < 0:
                raise ValueError

            if future_hours <= 0:
                raise ValueError

            # required_gpa = (
            #     (
            #         target_gpa *
            #         (completed_hours + future_hours)
            #     )
            #     -
            #     (
            #         current_gpa *
            #         completed_hours
            #     )
            # ) / future_hours

            # Target impossible

            # if required_gpa > 4.0:

            #     self.result_label.configure(
            #         text=(
            #             f"Required GPA: {required_gpa:.2f}\n"
            #             "Target is not achievable."
            #         ),
            #         text_color="#ff5555"
            #     )

            # else:

            #     self.result_label.configure(
            #         text=f"Required GPA: {required_gpa:.2f}",
            #         text_color="#00FFC2"
            #     )

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

        self.grid_rowconfigure(
            2,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # TITLE
        ctk.CTkLabel(
            self,
            text="Cumulative GPA",
            font=("Arial", 22, "bold")
        ).grid(
            row=0,
            column=0,
            pady=(20, 5)
        )

        ctk.CTkLabel(
            self,
            text="Add your semesters and calculate your cumulative GPA.",
            font=("Arial", 13)
        ).grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

        # MAIN FRAME
        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=10
        )

        self.main_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=50,
            pady=10
        )

        self.main_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # HEADERS 
        header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=10
        )

        header_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        ctk.CTkLabel(
            header_frame,
            text="Semester",
            font=("Arial", 13, "bold")
        ).grid(
            row=0,
            column=0
        )

        ctk.CTkLabel(
            header_frame,
            text="GPA",
            font=("Arial", 13, "bold")
        ).grid(
            row=0,
            column=1
        )

        ctk.CTkLabel(
            header_frame,
            text=" semester Credit Hours",
            font=("Arial", 13, "bold")
        ).grid(
            row=0,
            column=2
        )

        # SEMESTERS FRAME
        self.semesters_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            height=250
        )

        self.semesters_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=5
        )

        self.semesters_frame.grid_columnconfigure(
            0,
            weight=1
        )

        # ADD SEMESTER buttom
        ctk.CTkButton(
            self.main_frame,
            text="+ Add Semester",
            font=("Arial", 13, "bold"),
            command=self.add_semester
        ).grid(
            row=2,
            column=0,
            pady=12
        )

        # CALCULATE
        ctk.CTkButton(
            self.main_frame,
            text="Calculate Cumulative GPA",
            font=("Arial", 13, "bold"),
            command=self.calculate_cumulative
        ).grid(
            row=3,
            column=0,
            pady=(0, 15)
        )

        # RESULT
        self.result_label = ctk.CTkLabel(
            self,
            text="Cumulative GPA: --",
            font=("Arial", 20, "bold"),
            text_color="#00FFC2"
        )

        self.result_label.grid(
            row=3,
            column=0,
            pady=15
        )

        # Add first semester

        self.add_semester()

    # ADD SEMESTER
    def add_semester(self):

        semester_number = len(
            self.semesters
        ) + 1

        row_frame = ctk.CTkFrame(
            self.semesters_frame,
            fg_color="transparent"
        )

        row_frame.grid(
            row=len(self.semesters),
            column=0,
            sticky="ew",
            pady=5
        )

        row_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        # Semester Name

        ctk.CTkLabel(
            row_frame,
            text=f"Semester {semester_number}",
            font=("Arial", 12, "bold")
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        # GPA

        gpa_entry = ctk.CTkEntry(
            row_frame,
            placeholder_text="e.g. 3.40",
            width=100
        )

        gpa_entry.grid(
            row=0,
            column=1,
            padx=5
        )

        # Credit Hours

        hours_entry = ctk.CTkEntry(
            row_frame,
            placeholder_text="e.g. 15",
            width=100
        )

        hours_entry.grid(
            row=0,
            column=2,
            padx=5
        )

        # Store entries

        self.semesters.append(
            (
                gpa_entry,
                hours_entry,
                row_frame
            )
        )



    # CALCULATE CUMULATIVE GPA
    def calculate_cumulative(self):

        try:

            total_points = 0
            total_hours = 0

            for (
                gpa_entry,
                hours_entry,
                row_frame
            ) in self.semesters:

                gpa = float(
                    gpa_entry.get()
                )

                hours = float(
                    hours_entry.get()
                )

                if gpa < 0 or hours <= 0:
                    raise ValueError

                total_points += gpa * hours

                total_hours += hours

            cumulative_gpa = (
                total_points /
                total_hours
            )

            self.result_label.configure(
                text=(
                    f"Cumulative GPA: "
                    f"{cumulative_gpa:.2f}"
                ),
                text_color="#00FFC2"
            )

        except ValueError:

            self.result_label.configure(
                text=(
                    "Please enter valid "
                    "GPA and credit hours."
                ),
                text_color="#ff5555"
            )


# 5. MAIN WINDOW
class GPAMainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        # WINDOW SETTINGS
        self.geometry(
            "1100x650"
        )

        self.minsize(
            950,
            550
        )

        self.title(
            "GPA Calculator"
        )


        self.grid_rowconfigure(
            1,
            weight=1
        )

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.active_color = "#1f538d"#مداس علي 

        self.inactive_color = "#3a3a3a"#مش مداس عليه

        self.top_bar = ctk.CTkFrame(
            self,
            corner_radius=10
        )

        self.top_bar.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=15,
            pady=10
        )

        
        self.top_bar.grid_columnconfigure(
            5,
            weight=1
        )

        # STANDARD BUTTON
        self.btn_standard = ctk.CTkButton(
            self.top_bar,
            text="Standard ",
            height=40,
            font=("Arial", 13, "bold"),
            fg_color=self.inactive_color,
            command=self.show_standard
        )

        self.btn_standard.grid(
            row=0,
            column=0,
            padx=5,
            pady=8
        )

        self.btn_half = ctk.CTkButton(
            self.top_bar,
            text="Half-Point ",
            height=40,
            font=("Arial", 13, "bold"),
            fg_color=self.inactive_color,
            command=self.show_half
        )

        self.btn_half.grid(
            row=0,
            column=1,
            padx=5,
            pady=8
        )

        self.btn_custom = ctk.CTkButton(
            self.top_bar,
            text="Custom Scale",
            height=40,
            font=("Arial", 13, "bold"),
            fg_color=self.inactive_color,
            command=self.show_custom
        )

        self.btn_custom.grid(
            row=0,
            column=2,
            padx=5,
            pady=8
        )


        self.btn_target = ctk.CTkButton(
            self.top_bar,
            text="Target GPA",
            height=40,
            font=("Arial", 13, "bold"),
            fg_color=self.inactive_color,
            command=self.show_target
        )

        self.btn_target.grid(
            row=0,
            column=3,
            padx=5,
            pady=8
        )

 

        self.btn_cumulative = ctk.CTkButton(
            self.top_bar,
            text="Cumulative GPA",
            height=40,
            font=("Arial", 13, "bold"),
            fg_color=self.inactive_color,
            command=self.show_cumulative
        )

        self.btn_cumulative.grid(
            row=0,
            column=4,
            padx=5,
            pady=8
        )

        # THEME
        self.theme_optionmenu = ctk.CTkOptionMenu(
            self.top_bar,
            values=[
                "Dark",
                "Light"
            ],
            height=35,
            font=("Arial", 12, "bold"),
            command=ctk.set_appearance_mode
        )

        self.theme_optionmenu.grid(
            row=0,
            column=6,
            padx=10,
            pady=8,
            sticky="e"
        )

        # ====================================================
        # MAIN CONTAINER
        # ====================================================

        self.container = ctk.CTkFrame(
            self,
            corner_radius=10
        )

        self.container.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 15)
        )

        #عشان لما نكر الwindow
        self.container.grid_rowconfigure(
            0,
            weight=1
        )

        self.container.grid_columnconfigure(
            0,
            weight=1
        )

        # CUSTOM SCALE STORAGE
        self.custom_scale = {}

        # ====================================================
        # CREATE PAGES
        # ====================================================

        # Standard GPA
        self.frame_standard = GPACalculatorUIFrame(
            self.container,
            "Standard Scale"
        )


        # Half Point GPA
        self.frame_half = GPACalculatorUIFrame(
            self.container,
            "Half-Point Scale"
        )

        # Custom Scale Configuration
        self.frame_custom = CustomScaleUIFrame(
            self.container,
            self.save_custom_scale
        )

        # Custom GPA Calculator
        self.frame_custom_gpa = GPACalculatorUIFrame(
            self.container,
            "Custom Scale"
        )

        # Target GPA
        self.frame_target = TargetGPAUIFrame(
            self.container
        )

        # Cumulative GPA
        self.frame_cumulative = CumulativeGPAUIFrame(
            self.container
        )

        # SHOW DEFAULT PAGE
        self.show_standard()


    # HIDE ALL FRAMES
    def hide_all_frames(self):

        self.frame_standard.grid_forget()

        self.frame_half.grid_forget()

        self.frame_custom.grid_forget()

        self.frame_custom_gpa.grid_forget()

        self.frame_target.grid_forget()

        self.frame_cumulative.grid_forget()


    # UPDATE BUTTON COLORS
    def update_button_styles(self,active_btn):
        self.btn_standard.configure(fg_color=self.inactive_color)

        self.btn_half.configure(fg_color=self.inactive_color)

        self.btn_custom.configure(fg_color=self.inactive_color)

        self.btn_target.configure(fg_color=self.inactive_color)

        self.btn_cumulative.configure(fg_color=self.inactive_color)

        active_btn.configure(fg_color=self.active_color) # active

    #  STANDARD
    def show_standard(self):

        self.hide_all_frames()

        self.frame_standard.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.update_button_styles(
            self.btn_standard
        )

    # SHOW HALF POINT
    def show_half(self):

        self.hide_all_frames()

        self.frame_half.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.update_button_styles(
            self.btn_half
        )

    # SHOW CUSTOM CONFIGURATION
    def show_custom(self):

        self.hide_all_frames()

        self.frame_custom.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.update_button_styles(
            self.btn_custom
        )

    # SAVE CUSTOM SCALE
    def save_custom_scale(
        self,
        custom_scale
    ):

        # Store custom scale

        self.custom_scale = custom_scale

        # Go automatically to Custom GPA page

        self.show_custom_gpa()

    # SHOW CUSTOM GPA
    def show_custom_gpa(self):

        self.hide_all_frames()

        self.frame_custom_gpa.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        # Custom GPA belongs to Custom Scale button

        self.update_button_styles(
            self.btn_custom
        )

    # SHOW TARGET GPA
    def show_target(self):

        self.hide_all_frames()

        self.frame_target.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.update_button_styles(
            self.btn_target
        )

    # SHOW CUMULATIVE GPA
    def show_cumulative(self):

        self.hide_all_frames()

        self.frame_cumulative.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10,
            pady=10
        )

        self.update_button_styles(
            self.btn_cumulative
        )

# run
if __name__ == "__main__":

    app = GPAMainWindow()

    app.mainloop()