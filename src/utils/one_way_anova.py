import matplotlib.pyplot as plt
import numpy as np
import scikit_posthocs as sp
from scipy.stats import levene, shapiro
from statsmodels.stats.multicomp import MultiComparison
import pingouin as pg
import pandas as pd


def check_normality(data, group_labels, alpha=0.05):
    """
    각 그룹의 정규성 검정 수행
    
    ANOVA의 가정사항 중 정규성을 검증합니다.
    각 그룹별로 Shapiro-Wilk 검정을 수행하여 정규분포 여부를 판단합니다.
    
    Parameters
    ----------
    data : list of arrays
        각 그룹의 데이터를 담은 리스트
    group_labels : list
        각 그룹의 이름
    alpha : float
        유의수준 (기본값: 0.05)
    
    Returns
    -------
    bool
        모든 그룹이 정규성을 만족하는지 여부
        - True: 모든 그룹이 정규분포
        - False: 일부 그룹이 정규분포 아님
    """
    print("\n[정규성 검정 - Shapiro-Wilk Test]")
    print("-"*50)
    
    results = []
    for label, group_data in zip(group_labels, data):
        stat, p_value = shapiro(group_data)
        is_normal = "정규분포 ✓" if p_value > alpha else "정규분포 X"
        results.append({
            '그룹': label,
            'W-통계량': round(stat, 4),
            'p-value': round(p_value, 4),
            '판정': is_normal
        })
        
    result_df = pd.DataFrame(results)
    print(result_df)
    
    all_normal = all(r['p-value'] > alpha for r in results)
    if all_normal:
        print("\n✅ 모든 그룹이 정규성 가정을 만족합니다.")
    else:
        print("\n⚠️ 일부 그룹이 정규성 가정을 만족하지 않습니다.")
        print("   → 비모수 검정(Kruskal-Wallis) 고려")
    
    return all_normal


def check_homogeneity(data, group_labels, alpha=0.05):
    """
    등분산성 검정 수행
    
    ANOVA의 가정사항 중 등분산성을 검증합니다.
    Levene's test를 사용하여 그룹 간 분산의 동일성을 검정합니다.
    
    Parameters
    ----------
    data : list of arrays
        각 그룹의 데이터를 담은 리스트
    alpha : float
        유의수준 (기본값: 0.05)
    
    Returns
    -------
    bool
        등분산성 만족 여부
        - True: 등분산성 만족
        - False: 등분산성 위반
    """
    print("\n[등분산성 검정 - Levene's Test]")
    print("-"*50)
    
    stat, p_value = levene(*data)
    
    print(f"Levene 통계량: {stat:.4f}")
    print(f"p-value: {p_value:.4f}")
    
    if p_value > alpha:
        print("✅ 등분산성 가정을 만족합니다.")
        equal_var = True
    else:
        print("⚠️ 등분산성 가정을 만족하지 않습니다.")
        print("   → Welch's ANOVA 또는 Games-Howell 사후검정 권장")
        equal_var = False
    
    return equal_var


def calculate_eta_squared(f_statistic, df_between, df_within):
    """
    에타제곱 (효과 크기) 계산
    
    ANOVA 결과의 실질적 중요성을 평가하는 효과 크기를 계산합니다.
    에타제곱은 집단 차이가 전체 변동의 몇 %를 설명하는지 나타냅니다.
    
     주의: 이 함수는 F 통계량을 이용한 근사 공식을 사용합니다.
    정확한 계산을 위해서는 SS(Sum of Squares) 값이 필요하지만,
    F 통계량만으로도 충분히 신뢰할 수 있는 근사치를 제공합니다.
    
    근사 공식: η² ≈ (F × df_between) / (F × df_between + df_within)
    정확한 공식: η² = SS_between / SS_total
    
    Parameters
    ----------
    f_statistic : float
        F 통계량
    df_between : int
        집단 간 자유도
    df_within : int
        집단 내 자유도
    
    Returns
    -------
    tuple
        (에타제곱 값, 해석 문구)
    """
    
    # 근사 공식 사용
    eta_squared = (f_statistic * df_between) / (f_statistic * df_between + df_within)
    
    if eta_squared < 0.01:
        interpretation = "매우 작은 효과"
    elif eta_squared < 0.06:
        interpretation = "작은 효과"
    elif eta_squared < 0.14:
        interpretation = "중간 효과"
    else:
        interpretation = "큰 효과"
    
    return eta_squared, interpretation

def calculate_epsilon_squared(h_statistic, k, n):
    """
    엡실론제곱 (비모수 효과 크기) 계산
    
    Kruskal-Wallis 검정 결과의 실질적 중요성을 평가하는 효과 크기를 계산합니다.
    엡실론제곱은 집단 차이가 전체 순위 변동의 몇 %를 설명하는지 나타냅니다.
    
    Parameters
    ----------
    h_statistic : float
        Kruskal-Wallis H 통계량
    k : int
        집단(그룹) 수
    n : int
        전체 표본 크기
    
    Returns
    -------
    tuple
        (엡실론제곱 값, 해석 문구)
    
    Notes
    -----
    공식: ε² = (H - k + 1) / (n - k)
    - H: Kruskal-Wallis H 통계량
    - k: 그룹 수
    - n: 전체 표본 수
    
    해석 기준 (Cohen's 기준과 동일):
    - < 0.01: 매우 작은 효과
    - 0.01 ~ 0.06: 작은 효과
    - 0.06 ~ 0.14: 중간 효과
    - ≥ 0.14: 큰 효과
    """
    # 엡실론제곱 계산
    epsilon_squared = (h_statistic - k + 1) / (n - k)
    
    
    # 효과 크기 해석
    if epsilon_squared < 0.01:
        interpretation = "매우 작은 효과"
    elif epsilon_squared < 0.06:
        interpretation = "작은 효과"
    elif epsilon_squared < 0.14:
        interpretation = "중간 효과"
    else:
        interpretation = "큰 효과"
    
    return epsilon_squared, interpretation


def perform_tukey_hsd(data, labels):
    """
    Tukey HSD 사후검정 수행
    
    ANOVA에서 유의한 차이가 발견된 경우, 어느 집단 간에 차이가 있는지
    구체적으로 확인하기 위한 다중비교 검정을 수행합니다.
    
    Parameters
    ----------
    data : list of arrays
        각 그룹의 데이터
    labels : list
        각 그룹의 이름
    
    Returns
    -------
    TukeyHSDResults
        Tukey HSD 검정 결과 객체
    """
    print("\n[Tukey HSD 사후검정]")
    print("-"*50)
    
    # 데이터를 긴 형식으로 변환
    all_data = []
    all_labels = []
    
    for label, group_data in zip(labels, data):
        all_data.extend(group_data)
        all_labels.extend([label] * len(group_data))
    
    # Tukey HSD 수행
    mc = MultiComparison(all_data, all_labels)
    result = mc.tukeyhsd()
    
    print(result)
    
    # -----------------------------------------------------------------------------
    # 결과 해석
    # -----------------------------------------------------------------------------
    print("\n[결과 해석]")
    print("-"*50)
    
    # 1. 각 그룹의 평균 계산 및 정렬
    group_means = {}
    for i, label in enumerate(labels):
        group_means[label] = np.mean(data[i])
    
    sorted_groups = sorted(group_means.items(), key=lambda x: x[1], reverse=True)
    
    print("평균 순위:")
    for rank, (group, mean) in enumerate(sorted_groups, 1):
        print(f"  {rank}위: {group} (평균: {mean:.2f})")
    
    # 2. 유의성 관계 파악
    print("\n그룹 간 관계:")
    sig_matrix = {}
    
    # Tukey 결과에서 정보 추출
    for row in result.summary().data[1:]:  # 헤더 제외
        group1 = str(row[0]).strip()
        group2 = str(row[1]).strip()
        meandiff = float(row[2])
        p_adj = float(row[3])
        reject = str(row[6]).strip() == 'True'
        
        # 양방향으로 저장
        sig_matrix[(group1, group2)] = reject
        sig_matrix[(group2, group1)] = reject
        
        # 관계 출력
        if reject:
            print(f"  • {group1} ≠ {group2} (p={p_adj:.4f}, 유의한 차이)")
        else:
            print(f"  • {group1} ≈ {group2} (p={p_adj:.4f}, 차이 없음)")

    
    # 3. 시각화
    fig = result.plot_simultaneous(figsize=(10, 6))
    plt.title('Tukey HSD 95% 신뢰구간')
    plt.xlabel('그룹 간 평균 차이')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    return result


def perform_gameshowell(df, dv_col, group_col):
    """
    Games-Howell 사후검정 수행
    
    등분산성 가정을 만족하지 않을 때 사용하는 사후검정입니다.
    정규성은 만족하지만 등분산성이 위반된 경우에 적합합니다.
    
    Parameters
    ----------
    df : pandas.DataFrame
        분석할 데이터프레임
    dv_col : str
        종속변수(연속형) 컬럼명
    group_col : str
        집단변수(범주형) 컬럼명
    
    Returns
    -------
    pandas.DataFrame
        Games-Howell 검정 결과
    """
    
    print("\n[Games-Howell 사후검정]")
    print("-"*50)
    print("※ 등분산성 가정을 만족하지 않아 Games-Howell 사용\n")
    
    # Games-Howell 수행
    result = pg.pairwise_gameshowell(dv=dv_col, between=group_col, data=df)
    
    # =========================================================================
    # pingouin 버전에 따른 컬럼명 확인 및 처리
    # =========================================================================
    # 최신 버전: 'pval'과 'reject' 대신 'p-unc'와 'sig' 사용
    # 구버전: 'pval'과 'reject' 사용
    
    # p-value 컬럼 확인
    if 'pval' in result.columns:
        pval_col = 'pval'
    elif 'p-unc' in result.columns:
        pval_col = 'p-unc'
    else:
        raise ValueError("p-value 컬럼을 찾을 수 없습니다.")
    
    # reject/sig 컬럼 확인 (없으면 직접 생성)
    if 'reject' not in result.columns and 'sig' not in result.columns:
        result['reject'] = result[pval_col] < 0.05
        reject_col = 'reject'
    elif 'reject' in result.columns:
        reject_col = 'reject'
    else:
        reject_col = 'sig'
        result['reject'] = result[reject_col]  # 호환성을 위해 'reject' 컬럼 추가
    
    # 결과 출력을 위한 컬럼 선택
    display_cols = ['A', 'B', 'mean(A)', 'mean(B)', 'diff', pval_col]
    if reject_col in result.columns:
        display_cols.append(reject_col)
    
    print("[사후검정 결과]")
    print("-"*50)
    try:
        from IPython.display import display
        display(result[display_cols].round(4))
    except ImportError:
        print(result[display_cols].round(4))
    
    # -----------------------------------------------------------------------------
    # 결과 해석
    # -----------------------------------------------------------------------------
    print("\n[결과 해석]")
    print("-"*50)
    
    # 1. 각 그룹의 평균 계산 및 정렬
    group_means = df.groupby(group_col)[dv_col].mean().sort_values(ascending=False)
    
    print("평균 순위:")
    for rank, (group, mean) in enumerate(group_means.items(), 1):
        print(f"  {rank}위: {group} (평균: {mean:.2f})")
    
    # 2. 유의성 관계 파악
    print("\n그룹 간 관계:")
    for _, row in result.iterrows():
        is_significant = row['reject']
        p_value = row[pval_col]
        
        if is_significant:
            print(f"  • {row['A']} ≠ {row['B']} (p={p_value:.4f}, 유의한 차이)")
        else:
            print(f"  • {row['A']} ≈ {row['B']} (p={p_value:.4f}, 차이 없음)")
    
    # 3. 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 평균 차이와 신뢰구간 시각화
    y_pos = range(len(result))
    comparisons = [f"{row['A']}-{row['B']}" for _, row in result.iterrows()]
    diffs = result['diff'].values
    
    # 신뢰구간 계산 (SE * 1.96)
    errors = result['se'].values * 1.96
    
    colors = ['red' if reject else 'gray' for reject in result['reject']]
    
    ax.barh(y_pos, diffs, xerr=errors, color=colors, alpha=0.6, capsize=5)
    ax.axvline(x=0, color='black', linestyle='--', linewidth=1)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(comparisons)
    ax.set_xlabel('평균 차이 (95% CI)')
    ax.set_title('Games-Howell 사후검정 결과')
    ax.grid(True, alpha=0.3, axis='x')
    
    # 범례
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='red', alpha=0.6, label='유의한 차이 (p<0.05)'),
                      Patch(facecolor='gray', alpha=0.6, label='차이 없음 (p≥0.05)')]
    ax.legend(handles=legend_elements)
    
    plt.tight_layout()
    plt.show()
    
    return result


def perform_dunn_test(df, dv_col, group_col):
    """
    Dunn's 사후검정 수행
    
    Kruskal-Wallis 검정 후 사용하는 비모수 사후검정입니다.
    정규성 가정을 만족하지 않을 때 사용합니다.
    
    Parameters
    ----------
    df : pandas.DataFrame
        분석할 데이터프레임
    dv_col : str
        종속변수(연속형) 컬럼명
    group_col : str
        집단변수(범주형) 컬럼명
    
    Returns
    -------
    pandas.DataFrame
        Dunn's test 검정 결과
    """
    print("\n[Dunn's Test 사후검정]")
    print("-"*50)
    print("※ 정규성 가정을 만족하지 않아 비모수 사후검정 사용\n")
    
    # Dunn's test 수행 (Bonferroni 보정)
    # 반환되는 p-value는 이미 다중비교 보정이 완료된 값
    dunn_result = sp.posthoc_dunn(df, val_col=dv_col, 
                                    group_col=group_col, p_adjust='bonferroni')
    
    print("[사후검정 결과 - p-value 행렬 (Bonferroni 보정 적용됨)]")
    print("-"*50)
    print(dunn_result.round(4))
    
    # -----------------------------------------------------------------------------
    # 결과 해석
    # -----------------------------------------------------------------------------
    print("\n[결과 해석]")
    print("-"*50)
    
    # 1. 각 그룹의 중앙값 계산 및 정렬
    group_medians = df.groupby(group_col)[dv_col].median().sort_values(ascending=False)
    
    print("중앙값 순위 (비모수 검정은 순위 기반이므로 중앙값 참조):")
    for rank, (group, median) in enumerate(group_medians.items(), 1):
        mean = df.groupby(group_col)[dv_col].mean()[group]
        print(f"  {rank}위: {group} (중앙값: {median:.2f}, 참고-평균: {mean:.2f})")
    
    # 2. 유의성 관계 파악
    print("\n그룹 간 관계:")
    groups = dunn_result.columns.tolist()
    for i in range(len(groups)):
        for j in range(i+1, len(groups)):
            p_val = dunn_result.iloc[i, j]
            sig = "유의한 차이" if p_val < 0.05 else "차이 없음"
            symbol = "≠" if p_val < 0.05 else "≈"
            print(f"  • {groups[i]} {symbol} {groups[j]} (p={p_val:.4f}, {sig})")
    
    # 3. 시각화
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # 히트맵으로 p-value 시각화
    import seaborn as sns
    
    # p-value를 색상으로 표현 (낮을수록 진한 색)
    mask = np.triu(np.ones_like(dunn_result, dtype=bool))
    
    sns.heatmap(dunn_result, mask=mask, annot=True, fmt='.4f', 
                cmap='RdYlGn_r', center=0.05, vmin=0, vmax=0.2,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                ax=ax)
    
    ax.set_title('Dunn\'s Test p-value 히트맵\n(낮을수록 유의한 차이, Bonferroni 보정 적용)')
    plt.tight_layout()
    plt.show()
    
    return dunn_result