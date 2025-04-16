import pandas as pd

def generate_user_info_json_korean(
                    real_name: str, 
                    summary: str, 
                    skill_stack: list[str], 
                    final_degree: str, 
                    major: str, 
                    school_name: str, 
                    gpa: str, 
                    # degree_date: str ("YYYY.MM - YYYY.MM") ,
                    degree_date: str, # ("YYYY.MM - YYYY.MM")
                    education_and_exp_df: pd.DataFrame, 
                    work_experiences_df: pd.DataFrame,
                    certificates_df: pd.DataFrame, 
                    awards_df: pd.DataFrame, 
                    languages_df: pd.DataFrame,
                    ) -> dict :
    

    # ✅ education은 단일 항목 리스트로 구성
    education_json = [{
        "school_name": school_name,
        "degree_date": degree_date,
        "final_degree": final_degree,
        "major": major,
        "gpa": gpa
    }]

    # ✅ 전체 JSON 구조 생성
    user_info_json = {
        "real_name": real_name,
        "summary": summary,
        "skill_stack": skill_stack,
        "education": education_json,
        "education_and_exp": education_and_exp_df,
        "work_experiences": work_experiences_df,
        "certificates": certificates_df,
        "awards": awards_df,
        "languages": languages_df,
    }
    print(user_info_json)
    return user_info_json  # 이 반환값은 이후 DB 저장 로직이나 PDF 생성으로 전달