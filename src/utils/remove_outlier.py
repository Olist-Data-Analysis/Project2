import numpy as np
from scipy import stats


def detect_and_remove_outliers(data, column: str, method='iqr'):
    """
    통계적 방법으로 이상치 탐지 및 제거
    
    Parameters:
    - method: 'iqr' (사분위수), 'zscore' (Z-점수), 'percentile' (백분위)
    """
    data = data.copy()
    original_count = len(data)
    
    # 음수 제거 (물리적으로 불가능)
    data = data[data[column] >= 0]
    negative_removed = original_count - len(data)
    
    if method == 'iqr':
        # IQR 방식: Q1 - 1.5*IQR ~ Q3 + 1.5*IQR
        Q1 = data[column].quantile(0.25)
        Q3 = data[column].quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # 하한은 0 이상으로 보정
        lower_bound = max(0, lower_bound)
        
    elif method == 'zscore':
        # Z-score 방식: |Z| < 3
        z_scores = np.abs(stats.zscore(data[column]))
        threshold = 3
        mask = z_scores < threshold
        
        lower_bound = 0
        upper_bound = data[column].max()
        data = data[mask]
        
    elif method == 'percentile':
        # 백분위수 방식: 1% ~ 99%
        lower_bound = data[column].quantile(0.01)
        upper_bound = data[column].quantile(0.99)
    
    # IQR 또는 percentile 방식일 때 적용
    if method in ['iqr', 'percentile']:
        data = data[(data[column] >= lower_bound) & (data[column] <= upper_bound)]
    
    outliers_removed = original_count - len(data)
    
    print(f"\n[{method.upper()} 방식 이상치 제거 결과]")
    print(f"음수 제거: {negative_removed:,}건")
    print(f"이상치 제거: {outliers_removed:,}건 ({outliers_removed/original_count*100:.2f}%)")
    print(f"최종 데이터: {len(data):,}건")
    print(f"범위: {lower_bound:.1f} ~ {upper_bound:.1f} 시간")
    
    return data, lower_bound, upper_bound