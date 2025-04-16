
def json_to_user_component(user_db : dict) :
        
    real_name = user_db['real_name']
    summary = user_db['summary']
    skill_stack = user_db['skill_stack']
    final_degree = user_db['education']['final_degree']
    major = user_db['education']['major']
    school_name = user_db['education']['school_name']
    gpa = user_db['education']['gpa']
    degree_date = user_db['education']['degree_date']
    education_exp = user_db['education_and_exp']
    work_experiences = user_db['work_experiences']
    cerificates = user_db['certificates']
    awards = user_db['awards']
    languages = user_db['languages']

    return real_name, summary, skill_stack, final_degree, major, school_name, gpa, degree_date, education_exp, work_experiences, cerificates, awards, languages

