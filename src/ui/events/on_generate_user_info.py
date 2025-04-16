import pandas as pd

def _remap_dataframe(df : pd.DataFrame , keymap : dict):
    if isinstance(df, pd.DataFrame):
        return [
                {keymap.get(k, k): v for k, v in row.items()}
                for _, row in df.iterrows()
            ]
    else:
        return []


def generate_user_info_json(
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
    
    # ✅ 그라디오 헤더 → 실제 저장 키 이름 매핑
    education_and_exp_keymap = {
        "교육명": "edu_exp",
        "기간 (YYYY.MM - YYYY.MM)": "edu_exp_date"
    }
    work_experiences_keymap = {
        "회사명": "company",
        "근무기간 (YYYY.MM - YYYY.MM)": "work_date",
        "직책": "position",
        "주요 업무": "work_description"
    }
    certificates_keymap = {
        "자격증명": "certificate",
        "취득일 (YYYY.MM.DD)": "certificate_date",
        "발급기관": "certificate_org"
    }
    awards_keymap = {
        "수상명": "award",
        "수상일 (YYYY.MM.DD)": "award_date",
        "주최기관": "award_org"
    }
    languages_keymap = {
        "언어": "language",
        "시험/레벨": "language_level",
        "취득일 (YYYY.MM.DD)": "language_date"
    }

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
        "education_and_exp": _remap_dataframe(education_and_exp_df, education_and_exp_keymap),
        "work_experiences": _remap_dataframe(work_experiences_df, work_experiences_keymap),
        "certificates": _remap_dataframe(certificates_df, certificates_keymap),
        "awards": _remap_dataframe(awards_df, awards_keymap),
        "languages": _remap_dataframe(languages_df, languages_keymap),
    }
    return user_info_json  # 이 반환값은 이후 DB 저장 로직이나 PDF 생성으로 전달