from django import template
import re

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
    - Остальной текст оставляем без изменений.
    """

    # Регулярное выражение для изображений
    image_regex = r'(https?://(?:[a-zA-Z0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.(?:jpg|jpeg|png|gif|bmp|webp))'

    # Регулярное выражение для YouTube видео
    youtube_regex = r'(https?://(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+))'

    # Регулярное выражение для Vimeo видео
    vimeo_regex = r'(https?://(?:www\.)?vimeo\.com/(\d+))'

    # Регулярное выражение для Яндекс Видео
    yandex_video_regex = r'(https?://yandex\.ru/video/preview/([0-9]+))'

    # Регулярное выражение для RuTube видео
    rutube_video_regex = r'(https?://rutube\.ru/video/([a-zA-Z0-9_-]+))'

    # Функция для замены на тег <img>
    def replace_with_img(match):
        image_url = match.group(0)
        return f'<img width="560" height="315" src="{image_url}" alt="Image" />'

    # Функция для замены на тег <iframe> для YouTube
    def replace_with_youtube_iframe(match):
        video_id = match.group(2)  # Извлекаем id видео
        return f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

    # Функция для замены на тег <iframe> для Vimeo
    def replace_with_vimeo_iframe(match):
        video_id = match.group(2)  # Извлекаем id видео
        return f'<iframe src="https://player.vimeo.com/video/{video_id}" width="560" height="315" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>'

    # Функция для замены на тег <iframe> для Яндекс Видео
    def replace_with_yandex_video_iframe(match):
        video_id = match.group(2)  # Извлекаем id видео
        return f'<iframe width="560" height="315" src="https://yandex.ru/video/preview/{video_id}" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

    # Функция для замены на тег <iframe> для RuTube
    def replace_with_rutube_iframe(match):
        video_id = match.group(2)  # Извлекаем id видео
        return f'<iframe width="560" height="315" src="https://rutube.ru/video/{video_id}/embed/" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

    # Заменяем изображения на <img>
    value = re.sub(image_regex, replace_with_img, value)

    # Заменяем YouTube ссылки на <iframe>
    value = re.sub(youtube_regex, replace_with_youtube_iframe, value)

    # Заменяем Vimeo ссылки на <iframe>
    value = re.sub(vimeo_regex, replace_with_vimeo_iframe, value)

    # Заменяем Яндекс Видео ссылки на <iframe>
    value = re.sub(yandex_video_regex, replace_with_yandex_video_iframe, value)

    # Заменяем RuTube ссылки на <iframe>
    value = re.sub(rutube_video_regex, replace_with_rutube_iframe, value)

    return value