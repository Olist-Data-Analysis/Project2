import numpy as np
from scipy.stats import chi2_contingency

def cramers_v(chi2_stat, n, r, c):
    """
    Cramér's V 효과 크기 계산
    
    카이제곱 검정의 효과 크기를 측정하는 지표로, 두 범주형 변수 간
    연관성의 강도를 0~1 사이 값으로 표현합니다.
    
    Parameters
    ----------
    chi2_stat : float
        카이제곱 통계량 (χ²)
    n : int
        전체 표본 수 (분할표의 총합)
    r : int
        행(row)의 개수
    c : int
        열(column)의 개수
    
    Returns
    -------
    float
        Cramér's V 값 (0~1 사이)
        - 0에 가까울수록: 독립적 (연관성 없음)
        - 1에 가까울수록: 강한 연관성
    """
    return np.sqrt(chi2_stat / (n * min(r-1, c-1)))


def interpret_cramers_v(v):
    """
    Cramér's V 값 해석
    
    Parameters
    ----------
    v : float
        Cramér's V 값 (0~1)
    
    Returns
    -------
    str
        연관성 강도 해석
        
    """
    if v < 0.1:
        return "매우 약한 관계"
    elif v < 0.3:
        return "약한 관계"
    elif v < 0.5:
        return "중간 관계"
    else:
        return "강한 관계"


def check_expected_frequencies(contingency_table):
    """
    카이제곱 검정의 기대빈도 가정 확인
    
    카이제곱 검정을 수행하기 전에 기대빈도가 충분한지 검사합니다.
    기대빈도가 너무 작으면 카이제곱 검정의 정확도가 떨어집니다.
    
    Parameters
    ----------
    contingency_table : array-like
        분할표 (관측 빈도)
    
    Returns
    -------
    bool
        카이제곱 검정 사용 가능 여부
        - True: 카이제곱 검정 사용 가능
        - False: Fisher's exact test 권장
    
    검정 기준
    ---------
    1. 모든 기대빈도 ≥ 5 (이상적)
    2. 기대빈도 < 5인 셀이 전체의 20% 이하 (허용 가능)
    
    Notes
    -----
    - 2×2 분할표에서 기대빈도 < 5인 경우: Fisher's exact test 필수
    - 큰 분할표에서 일부 셀만 < 5: 카이제곱 검정 여전히 사용 가능
    """
    # 카이제곱 검정으로 기대빈도 계산
    chi2_stat, p_val, dof, expected = chi2_contingency(contingency_table)
    
    print("\n[기대빈도 확인]")
    print("-"*40)
    
    # -------------------------------------------------------------------------
    # 1. 최소 기대빈도 확인
    # -------------------------------------------------------------------------
    min_expected = expected.min()
    print(f"최소 기대빈도: {min_expected:.2f}")
    
    # -------------------------------------------------------------------------
    # 2. 기대빈도 < 5인 셀의 비율 계산
    # -------------------------------------------------------------------------
    cells_below_5 = (expected < 5).sum()  # 5 미만인 셀 개수
    total_cells = expected.size  # 전체 셀 개수
    percent_below_5 = (cells_below_5 / total_cells) * 100
    
    print(f"5 미만 셀: {cells_below_5}/{total_cells} ({percent_below_5:.1f}%)")
    
    # -------------------------------------------------------------------------
    # 3. 카이제곱 검정 적합성 판단
    # -------------------------------------------------------------------------
    # 조건: 최소 기대빈도 ≥ 5 AND 5 미만 셀 비율 ≤ 20%
    if min_expected < 5 or percent_below_5 > 20:
        print("⚠️ 주의: Fisher's exact test 사용 권장")
        print("   (기대빈도가 너무 작아 카이제곱 검정 부정확)")
        return False
    else:
        print("✅ 카이제곱검정 사용 가능")
        return True


def standardized_residuals(observed, expected):
    """
    표준화 잔차 계산
    
    각 셀의 관측값과 기대값의 차이를 표준화하여 어느 셀이
    독립성 가정에서 크게 벗어나는지 파악합니다.
    
    Parameters
    ----------
    observed : array-like
        관측 빈도 (분할표)
    expected : array-like
        기대 빈도 (chi2_contingency의 결과)
    
    Returns
    -------
    array
        표준화 잔차 행렬
        
    해석
    ----
    - |잔차| > 2: 해당 셀이 독립성에서 유의하게 벗어남
    - |잔차| > 3: 매우 강한 연관성 (이상치 수준)
    - 양수: 관측값이 기대값보다 큼 (과대 표현)
    - 음수: 관측값이 기대값보다 작음 (과소 표현)
    """
    return (observed - expected) / np.sqrt(expected)