#===================grade into point mapping========================
grade_into_point={
    'A': 4,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3,
    'B-': 2.7,
    'C+':2.3,
    'C':2.0,
    'C-':1.7,
    'D+':1.3,
    'D':1.0,
    'F':0.0
}
#=================semester gpa calculation========================
def calculate_semester_gpa(courses):
    total_points=0
    total_hours=0
    for course in courses:
        points=grade_into_point[course['grade']]*course['credit_hours']
        total_points+=points
        total_hours+=course['credit_hours']
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
        total_points+=semester['gpa']*semester['credit_hours']
        total_hours+=semester['credit_hours']
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
    

    
    
    
        
    
    
    