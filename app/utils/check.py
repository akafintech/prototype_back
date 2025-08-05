import re

def check_language(text:str) -> bool:
    """한글 포함 여부 확인

    Args:
        text (str): 판별할 문자열

    Returns:
        bool: 판별결과 (True: 한글 포함, False: 한글 미포함)
    """
    # 한글이 포함된 경우
    if re.search(r'[가-힣]', text):
        return True
    
    # 한글이 전혀 포함되지 않은 경우
    else:
        return False
