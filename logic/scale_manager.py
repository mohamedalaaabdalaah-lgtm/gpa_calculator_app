STANDARD_SCALE = {
    'A+': 4.0, 'A': 4.0, 'A-': 3.7,
    'B+': 3.3, 'B': 3.0, 'B-': 2.7,
    'C+': 2.3, 'C': 2.0, 'C-': 1.7,
    'D+': 1.3, 'D': 1.0, 'F': 0.0  
}

HALF_POINT_SCALE ={
    'A+': 4.0, 'A': 3.5, 
    'B+': 3.0, 'B': 2.5, 
    'C+': 2.0, 'C': 1.5, 
    'D+': 1.0, 'D': 0.5,
    'F': 0.0 
}

def check_scale(scale_data):
    if not isinstance(scale_data, dict) or len(scale_data) == 0:
        return False 
    for grade, points in scale_data.items():
        if not isinstance(grade, str) or not isinstance(points, (int, float)):
            return False
        if points < 0:
            return False

        return True

def get_grade_points(grade, scale_type = "standaed",custom_scale_dict=None):
    grade = grade.upper()

    if scale_type == "standard" :
        scale = STANDARD_SCALE

    elif scale_type == "half_point":
        scale = HALF_POINT_SCALE

    elif scale_type == "custom":
        if custom_scale_dict and grade in custom_scale_dict:
            return float(custom_scale_dict[grade])
        return 0.0

    else:
        raise ValueError("Invalid scale type. use 'standard' or 'half_point' .")  

    if grade in scale:
        return scale[grade]
    else:
        raise KeyError(f"Grade '{grade}' not found in the selected scale.")   