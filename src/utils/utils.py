from matplotlib.colors import LinearSegmentedColormap

# 사용자 정의 컬러맵 생성
def generate_colormap(colors: list, name: str = 'custom', n_colors=256):
    # n_colors=256은 256개의 색상 레벨을 생성하여 더 부드러운 전환을 만듦
    cmap_name = name
    custom_cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_colors)

    return custom_cmap