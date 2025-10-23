from numpy.typing import ArrayLike
from scipy import stats
import pandas as pd
from scipy.stats import shapiro

def check_normality_simple(data: ArrayLike, name="데이터") -> bool:
    """
    데이터의 정규성을 검정하는 함수
    
    Parameters
    ----------
    data : array-like
        정규성을 검정할 데이터 (NaN은 자동 제거)
    name : str, default="데이터"
        출력 시 표시될 데이터 이름
    
    Returns
    -------
    bool
        정규분포 가정 충족 여부
        - True: 정규분포 가정 가능 (모수 검정)
        - False: 정규분포 가정 위반 (비모수 검정)
    
    검정 기준
    ---------
    - n < 30: Shapiro-Wilk 검정 (p > 0.05)
    - 30 ≤ n < 100: 왜도/첨도 우선, 필요시 Shapiro-Wilk
    - n ≥ 100: 왜도 기준 (|왜도| < 2, 중심극한정리)
    """
    # NaN 체크
    if pd.isna(data).any():
        print(f"⚠️ 경고: {name}에 NaN 값이 {pd.isna(data).sum()}개 포함됨")
        data = data.dropna()
        print(f"   → NaN 제거 후 n={len(data)}")
    
    n = len(data)
    
    print(f"\n[{name} 정규성 검정] n={n}")
    print("-"*40)
    
    # 왜도와 첨도
    skew = stats.skew(data)
    kurt = stats.kurtosis(data, fisher=True)
    print(f"왜도(Skewness): {skew:.3f}")
    print(f"첨도(Kurtosis): {kurt:.3f}")
    
    # 표본 크기에 따른 판단
    if n < 30:
        stat, p = shapiro(data)
        print(f"Shapiro-Wilk p-value: {p:.4f}")
        is_normal = p > 0.05
        reason = f"Shapiro p={'>' if is_normal else '≤'}0.05"
    elif n < 100:
        if abs(skew) < 1 and abs(kurt) < 2:
            is_normal = True
            reason = "|왜도|<1, |첨도|<2"
        else:
            stat, p = shapiro(data)
            print(f"추가 Shapiro-Wilk p-value: {p:.4f}")
            is_normal = p > 0.05
            reason = f"Shapiro p={'>' if is_normal else '≤'}0.05"
    else:
        is_normal = abs(skew) < 2
        reason = f"|왜도|{'<' if is_normal else '≥'}2 (중심극한정리)"
    
    print(f"결과: {'✅ 정규분포 가정 충족' if is_normal else '❌ 정규분포 가정 위반'} ({reason})")
    return is_normal