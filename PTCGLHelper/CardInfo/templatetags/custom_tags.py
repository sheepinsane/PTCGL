from django import template

register = template.Library()
@register.filter(name='type_image')
    
def type_image(value):
    img_to_char = {
        'Grass.png': '草',
        'Colorless.png': '無',
        'Fire.png': '火',
        'Water.png': '水',
        'Lightning.png': '雷',
        'Psychic.png': '超',
        'Fighting.png': '鬥',
        'Darkness.png': '惡',
        'Metal.png': '鋼',
        'Fairy.png': '妖',
        'Dragon.png': '龍'
    }

    for img_name, char in img_to_char.items():
        if char in value:
            return f"images/{img_name}"
    
    return None