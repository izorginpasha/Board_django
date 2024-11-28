from django import template
import re
from bs4 import BeautifulSoup


register = template.Library()



@register.filter()
def censorship(text):
   """
   value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   STOP_LIST = [
       'мат',
       'редиска',
       'сук',
   ]


   for word in STOP_LIST:
      if word in text:
          text = text.lower().replace(word.lower(), word[0]+'***')


   return f'{text}'


from django import template
import re

register = template.Library()


@register.filter(name='media_embed')
def media_embed(value):
    """
    Преобразует URL-адреса изображений и видео в соответствующие HTML теги:
    - Ссылки на изображения заменяются на <img>
    - Ссылки на YouTube видео заменяются на <iframe>
    - Ссылки на Vimeo видео заменяются на <iframe>
    - Ссылки на Яндекс Видео заменяются на <iframe>
    - Ссылки на RuTube видео заменяются на <iframe>
    - Обрабатывает существующие <img> теги, добавляя размеры и стили.
    """

    # Регулярное выражение для YouTube видео
    youtube_regex = r'(https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+))'
    vimeo_regex = r'(https?://(?:www\.)?vimeo\.com/(\d+))'
    yandex_video_regex = r'(https?://yandex\.ru/video/preview/([0-9]+))'
    rutube_video_regex = r'(https?://rutube\.ru/video/([a-zA-Z0-9_-]+))'

    def replace_with_youtube_iframe(match):
        video_id = match.group(2)
        return f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

    def replace_with_vimeo_iframe(match):
        video_id = match.group(2)
        return f'<iframe src="https://player.vimeo.com/video/{video_id}" width="560" height="315" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>'

    def replace_with_yandex_video_iframe(match):
        video_id = match.group(2)
        return f'<iframe width="560" height="315" src="https://yandex.ru/video/preview/{video_id}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

    def replace_with_rutube_iframe(match):
        video_id = match.group(2)
        return f'<iframe width="560" height="315" src="https://rutube.ru/video/{video_id}/embed/" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

    # Используем BeautifulSoup для обработки существующих HTML-тегов
    soup = BeautifulSoup(value, 'html.parser')

    # Обработка тегов <img>
    for img in soup.find_all('img'):
        img['width'] = '400'
        img['height'] = '300'
        img['style'] = 'object-fit: cover;'

    for span in soup.find_all('span'):
        text_length = len(span.get_text())
        if text_length > 50:
            span['style'] = 'display: block; background-color: lightblue;'
        else:
            span['style'] = 'display: inline-block; background-color: lightgreen;'
    # Обработка текста и замена ссылок на видео
    text = str(soup)
    text = re.sub(youtube_regex, replace_with_youtube_iframe, text)
    text = re.sub(vimeo_regex, replace_with_vimeo_iframe, text)
    text = re.sub(yandex_video_regex, replace_with_yandex_video_iframe, text)
    text = re.sub(rutube_video_regex, replace_with_rutube_iframe, text)

    # Возвращаем обработанный HTML
    return text