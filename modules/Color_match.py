import colorsys

# 기본 색상 매핑 (RGB 값에 가장 가까운 색상 이름)
COLOR_NAMES = {
    (0, 0, 0): 'black',
    (255, 255, 255): 'white',
    (255, 0, 0): 'red',
    (0, 255, 0): 'green',
    (0, 0, 255): 'blue',
    (255, 255, 0): 'yellow',
    (255, 0, 255): 'magenta',
    (0, 255, 255): 'cyan',
    (128, 0, 0): 'maroon',
    (0, 128, 0): 'dark green',
    (0, 0, 128): 'navy',
    (128, 128, 0): 'olive',
    (128, 0, 128): 'purple',
    (0, 128, 128): 'teal',
    (128, 128, 128): 'gray',
    (255, 165, 0): 'orange',
    (255, 192, 203): 'pink',
    (165, 42, 42): 'brown',
    (240, 230, 140): 'khaki',
    (230, 230, 250): 'lavender'
}

def recommend_color(rgb):
    """보색 추천 함수"""
    r, g, b = rgb
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    h_complement = (h + 0.5) % 1.0  # 보색 계산
    r2, g2, b2 = colorsys.hls_to_rgb(h_complement, l, s)
    return (int(r2 * 255), int(g2 * 255), int(b2 * 255))

def rgb_to_hex(rgb):
    """RGB 튜플을 HEX 문자열로 변환 (BGR 순서 주의)"""
    return '#{:02x}{:02x}{:02x}'.format(rgb[2], rgb[1], rgb[0])

def find_nearest_color_name(rgb):
    """RGB에 가장 가까운 기본 색상 이름 찾기"""
    min_distance = float('inf')
    nearest_color = 'unknown'
    
    for color_rgb, name in COLOR_NAMES.items():
        distance = sum((a - b) ** 2 for a, b in zip(rgb, color_rgb))
        if distance < min_distance:
            min_distance = distance
            nearest_color = name
    
    return nearest_color
