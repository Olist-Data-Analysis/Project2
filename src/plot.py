# 표준 라이브러리
from typing import Sequence, Any

# 서드 파티 라이브러리
import pandas as pd
from numpy.typing import ArrayLike
from matplotlib.axes import Axes
from matplotlib.colors import Colormap
import seaborn as sns


# 박스플롯 시각화 함수
def plot_box(axes: Axes, x: ArrayLike | Sequence[ArrayLike], ylabel, label:Sequence[str] = None, color: str | Sequence[str] = 'skyblue', target_value=None, target_label='기준값'):
    bp = axes.boxplot(x=x, label=label, patch_artist=True)
    color = [color] if isinstance(color, str) else color
    for i in range(len(color)):
        bp['boxes'][i].set_facecolor(color[i])
    if target_value:
        axes.axhline(target_value, color='red', linestyle='--', linewidth=2)
        axes.text(1.1, target_value, f'{target_label}: {target_value}')
    axes.set_ylabel(ylabel)
    axes.set_title(f'{ylabel} 분포 박스플롯')
    axes.grid(True, alpha=0.3)


# 히스토그램 시각화 함수
def plot_hist(axes: Axes, x: pd.Series, xlabel: str, alpha: float, bins: int, density=False, color: str | Sequence[str] = 'skyblue', target_value=None, target_label='기준값'):
    axes.hist(x, bins=bins, edgecolor='black', alpha=alpha, color=color, density=density)
    if target_value:
        axes.axvline(target_value, color='red', linestyle='--', linewidth=2, label=target_label)
        axes.axvline(x.mean(), color='blue', linestyle='--', linewidth=2, label=f'평균: {x.mean():.1f}')
    
    axes.set_xlabel(f'{xlabel}')
    axes.set_ylabel('빈도')
    axes.set_title(f'{xlabel} 분포')
    axes.legend()
    axes.grid(True, alpha=0.3)


# 누적 막대그래프 시각화 함수
def plot_stacked_bar(data: pd.DataFrame, axes: Axes, var1: str, var2: str, label: str, colors: dict = None, cmap: str | Colormap | None = None, xrotation=0, yrotation=0):
    data.T.plot(kind='bar', stacked=True, ax=axes, colormap=cmap, color=colors)
    axes.set_title(f'{var1}별 {var2} 분포')
    axes.set_xlabel(var1)
    axes.set_ylabel(label)
    axes.legend(title=var2)
    axes.tick_params(axis='x', labelrotation=xrotation)
    axes.tick_params(axis='y', labelrotation=yrotation)

# 히트맵 시각화 함수
def plot_heatmap(data: pd.DataFrame, axes: Axes, var1: str, var2: str, label: str, cmap: str | Colormap | None = 'YlOrRd'):
    sns.heatmap(data, annot=True, fmt='d', cmap=cmap, ax=axes, cbar_kws={'label': label})
    axes.set_title(f'{var1} × {var2} 히트맵')

# 비율 막대그래프 시각화 함수
def plot_prop_bar(data: pd.DataFrame, axes: Axes, var1: str, var2: str, colors: Any = None, cmap: str | Colormap | None = None, xrotation=0, yrotation=0):
    prop_table = data.div(data.sum(axis=1), axis=0) * 100
    prop_table.plot(kind='bar', ax=axes, color=colors)
    axes.set_title(f'{var1}별 {var2} 비율(%)')
    axes.set_ylabel('비율(%)')
    axes.set_xlabel(var1)
    axes.set_xticklabels(axes.get_xticklabels(), rotation=0)
    axes.legend(title=f'{var2}', bbox_to_anchor=(1.05, 1))
    axes.tick_params(axis='x', labelrotation=xrotation)
    axes.tick_params(axis='y', labelrotation=yrotation)