from src.logic.app_logic import app_logic
import gradio as gr 
import pandas as pd

def json_to_user_component(user_db) :    
    
    if user_db.get('real_name') :
        real_name = user_db['real_name']
    else :
        real_name = ""
    
    if user_db.get('summary') :
        summary = user_db['summary']
    else :
        summary = ""
   
    if user_db.get('skill_stack') :
        skill_stack = user_db['skill_stack']
    else :
        skill_stack = ""

    if user_db.get('education') :
        final_degree = user_db['education'][0]['final_degree']
        major = user_db['education'][0]['major']
        school_name = user_db['education'][0]['school_name']
        gpa = user_db['education'][0]['gpa']
        degree_date = user_db['education'][0]['degree_date']        
    else :
        final_degree = ""
        major = ""
        school_name = ""
        gpa = ""
        degree_date = ""

    if user_db.get('education_and_exp') :
        education_exp = pd.DataFrame(user_db['education_and_exp'])
    else :
        education_exp = pd.DataFrame(columns=['교육명', '기간 (YYYY.MM - YYYY.MM)'])

    if user_db.get('work_experiences') :
        work_experiences = pd.DataFrame(user_db['work_experiences'])
    else :
        work_experiences = pd.DataFrame(columns=['회사명','근무기간 (YYYY.MM - YYYY.MM)' , '직책', '주요 업무'])     

    if user_db.get('certificates') :
        cerificates = pd.DataFrame(user_db['certificates'])
    else :
        cerificates = pd.DataFrame(columns=['자격증명', '취득일 (YYYY.MM.DD)']) 

    if user_db.get('awards') :
        awards = pd.DataFrame(user_db['awards'])
    else :
        awards = pd.DataFrame(columns=['수상명', '수상일 (YYYY.MM.DD)']) 

    if user_db.get('languages') :
        languages = pd.DataFrame(user_db['languages'])
    else :
        languages = pd.DataFrame(columns=['어학시험/점수', '취득일 (YYYY.MM.DD)']) 

    return gr.update(value=real_name), gr.update(value=summary), gr.update(value=skill_stack), gr.update(value=final_degree), gr.update(value=major), gr.update(value=school_name), gr.update(value=gpa), gr.update(value=degree_date), gr.update(value=education_exp), gr.update(value=work_experiences), gr.update(value=cerificates), gr.update(value=awards), gr.update(value=languages)
