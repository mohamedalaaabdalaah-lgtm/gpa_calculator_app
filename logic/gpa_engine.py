from gpa_calculator_app.logic.scale_manager import get_grade_points 

#=================semester gpa calculation========================
def calculate_semester_gpa(courses , scale_type = "standard",custom_scale_dict = None):
    total_points=0
    total_hours=0
    for course in courses:
        points=get_grade_points(course['grade'],scale_type , custom_scale_dict) * float(course['hours'])
        total_points+=points
        total_hours+=float(course['hours'])
    if total_hours==0:
        gpa=0
    else:
        gpa=total_points/total_hours
    return gpa
#=================cumulative gpa calculation========================
def calculate_cumulative_gpa(semesters):
    total_points=0
    total_hours=0
    for semester in semesters:
        total_points+=semester['gpa']*semester['hours']
        total_hours+=semester['hours']
    if total_hours==0:
        gpa=0
    else:
        gpa=total_points/total_hours
    return gpa
#=================required gpa calculation========================
def calculate_required_gpa(current_gpa, current_hours, target_gpa, target_hours):
    total_points_required=target_gpa*target_hours
    total_points_current=current_gpa*current_hours
    points_needed=total_points_required-total_points_current
    hours_needed=target_hours-current_hours
    if hours_needed<=0:
        return 0 
    required_gpa=points_needed/hours_needed
    return required_gpa
    

    
    
    
        
    
    
    