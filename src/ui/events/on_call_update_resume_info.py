import pandas as pd

from src.logic.app_logic import app_logic


def _df_to_list(df):
    if isinstance(df, pd.DataFrame):
        return df.to_dict(orient="records")
    return []

def call_update_resume_info(
                    real_name: str, 
                    summary: str, 
                    skill_stack: list[str], 
                    final_degree: str, 
                    major: str, 
                    school_name: str, 
                    gpa: str, 
                    # degree_date: str ("YYYY.MM - YYYY.MM") ,
                    degree_date: str,
                    education_and_exp : dict, 
                    work_experiences : dict, 
                    certificates : dict, 
                    awards : dict, 
                    languages : dict
                    ) -> None :

    resume_fields = {
        'real_name': real_name,
        'summary': summary,
        'skill_stack': skill_stack,
        'education': [{
            'school_name': school_name,
            'degree_date': degree_date,
            'final_degree': final_degree,
            'major': major,
            'gpa': gpa
        }],

        'education_and_exp': _df_to_list(education_and_exp),
        'work_experiences': _df_to_list(work_experiences),
        'certificates': _df_to_list(certificates),
        'awards': _df_to_list(awards),
        'languages': _df_to_list(languages),
    }

    # 기존 인스턴스(app_logic)를 사용하여 원래 함수 호출
    app_logic.update_resume_info(**resume_fields)
