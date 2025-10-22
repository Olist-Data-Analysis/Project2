# 표준 라이브러리
from typing import Sequence, Any

# 서드 파티 라이브러리
import numpy as np
import pandas as pd
from numpy.typing import ArrayLike
from matplotlib.axes import Axes
from scipy import stats
from matplotlib.colors import Colormap
import seaborn as sns


# 박스플롯 시각화 함수
def plot_box(
        ax: Axes, x: ArrayLike | Sequence[ArrayLike], 
        ylabel, label:Sequence[str] = None, tick_labels=None, 
        color: str | Sequence[str] = 'skyblue', target_value=None, target_label='기준값',
        xrotation=0, yrotation=0
    ):
    bp = ax.boxplot(x=x, label=label, tick_labels=tick_labels, patch_artist=True)
    color = [color] if isinstance(color, str) else color
    for i in range(len(color)):
        bp['boxes'][i].set_facecolor(color[i])
    if target_value:
        ax.axhline(target_value, color='red', linestyle='--', linewidth=2)
        ax.text(1.1, target_value, f'{target_label}: {target_value}')
    ax.set_ylabel(ylabel)
    ax.set_title(f'{ylabel} 분포 박스플롯')
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', labelrotation=xrotation)
    ax.tick_params(axis='y', labelrotation=yrotation)


# 히스토그램 시각화 함수
def plot_hist(ax: Axes, x: pd.Series, xlabel: str, alpha: float, bins: int, density=False, color: str | Sequence[str] = 'skyblue', target_value=None, target_label='기준값'):
    ax.hist(x, bins=bins, edgecolor='black', alpha=alpha, color=color, density=density)
    if target_value:
        ax.axvline(target_value, color='red', linestyle='--', linewidth=2, label=target_label)
        ax.axvline(x.mean(), color='blue', linestyle='--', linewidth=2, label=f'평균: {x.mean():.1f}')
    
    ax.set_xlabel(f'{xlabel}')
    ax.set_ylabel('빈도')
    ax.set_title(f'{xlabel} 분포')
    ax.legend()
    ax.grid(True, alpha=0.3)


# 누적 막대그래프 시각화 함수
def plot_stacked_bar(
        data: pd.DataFrame, ax: Axes, var1: str, var2: str, label: str,
        colors: dict = None, cmap: str | Colormap | None = None,
        xrotation=0, yrotation=0,
        normalize: str = None
    ):
    """
    normalize: None, 'column', 'row', 'all'
    - 'column': 각 열 별로 정규화
    - 'row': 각 행 별로 정규화  
    - 'all': 전체 데이터 기준 정규화
    """
    if normalize == 'column':
        # 각 열의 합으로 나누어 비율로 변환 (0~1)
        plot_data = data.div(data.sum(axis=0), axis=1) * 100  # 백분율로
        fmt = '.1f'
        label = f'{label} (%)'
    elif normalize == 'row':
        plot_data = data.div(data.sum(axis=1), axis=0) * 100
        fmt = '.1f'
        label = f'{label} (%)'
    elif normalize == 'all':
        plot_data = (data / data.sum().sum()) * 100
        fmt = '.1f'
        label = f'{label} (%)'
    else:
        plot_data = data
        fmt = 'd'
    plot_data.T.plot(kind='bar', stacked=True, ax=ax, colormap=cmap, color=colors)
    ax.set_title(f'{var1}별 {var2} 분포')
    ax.set_xlabel(var1)
    ax.set_ylabel(label)
    ax.legend(title=var2)
    ax.tick_params(axis='x', labelrotation=xrotation)
    ax.tick_params(axis='y', labelrotation=yrotation)

# 히트맵 시각화 함수
def plot_heatmap(data: pd.DataFrame, ax: Axes, var1: str, var2: str, label: str, cmap: str | Colormap | None = 'YlOrRd', normalize: str = None):
    """
    normalize: None, 'column', 'row', 'all'
    - 'column': 각 열 별로 정규화
    - 'row': 각 행 별로 정규화  
    - 'all': 전체 데이터 기준 정규화
    """
    if normalize == 'column':
        # 각 열의 합으로 나누어 비율로 변환 (0~1)
        plot_data = data.div(data.sum(axis=0), axis=1) * 100  # 백분율로
        fmt = '.1f'
        label = f'{label} (%)'
    elif normalize == 'row':
        plot_data = data.div(data.sum(axis=1), axis=0) * 100
        fmt = '.1f'
        label = f'{label} (%)'
    elif normalize == 'all':
        plot_data = (data / data.sum().sum()) * 100
        fmt = '.1f'
        label = f'{label} (%)'
    else:
        plot_data = data
        fmt = 'd'
    sns.heatmap(plot_data, annot=True, fmt=fmt, cmap=cmap, ax=ax, 
                cbar_kws={'label': label})
    ax.set_title(f'{var1} × {var2} 히트맵')

# 비율 막대그래프 시각화 함수
def plot_prop_bar(data: pd.DataFrame, ax: Axes, var1: str, var2: str, colors: Any = None, cmap: str | Colormap | None = None, xrotation=0, yrotation=0):
    prop_table = data.div(data.sum(axis=1), axis=0) * 100
    prop_table.plot(kind='bar', ax=ax, color=colors)
    ax.set_title(f'{var1}별 {var2} 비율(%)')
    ax.set_ylabel('비율(%)')
    ax.set_xlabel(var1)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.legend(title=f'{var2}', bbox_to_anchor=(1.05, 1))
    ax.tick_params(axis='x', labelrotation=xrotation)
    ax.tick_params(axis='y', labelrotation=yrotation)


def plot_mean_sem(
        x: ArrayLike | Sequence[ArrayLike], ax: Axes, 
        var1: str, var2: str, labels: list,
        colors: Any = None,
        xrotation=0, yrotation=0
    ):
    means = [np.mean(d) for d in x]
    sems = [stats.sem(d) for d in x]
    x_pos = np.arange(len(labels))

    ax.bar(x_pos, means, yerr=[1.96*s for s in sems], capsize=8,
            color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    ax.set_title(f'{var1}별 평균 {var2} (95% CI)')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(labels)
    ax.set_ylabel(f'평균 {var2}')
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', labelrotation=xrotation)
    ax.tick_params(axis='y', labelrotation=yrotation)

def plot_scatter_jitter(
        x: ArrayLike, ax: Axes, 
        var1: str, var2: str, labels: list, 
        colors: Any = None,
        xrotation=0, yrotation=0
    ):
    for i, (_, data) in enumerate(zip(labels, x)):
        x = np.random.normal(i, 0.04, size=len(data))
        ax.scatter(x, data, alpha=0.5, s=30, color=colors[i])
    ax.set_title(f'{var1}별 {var2} 분포')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_ylabel(f'{var2}')
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', labelrotation=xrotation)
    ax.tick_params(axis='y', labelrotation=yrotation)