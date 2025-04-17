import pandas as pd

def add_row(df: pd.DataFrame): # 바뀐이름: 파일.함수명
    
    if isinstance(df, pd.DataFrame):
        new_row = pd.DataFrame([[ "" for _ in df.columns ]], columns=df.columns)
        return pd.concat([df, new_row], ignore_index=True)
    
    else:
        # 초기 리스트 형태일 경우에도 유연하게 처리
        df.append(["" for _ in df[0]])
        return df