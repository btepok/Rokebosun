# image creator with osu acc info

import requests
import random
from PIL import Image, ImageDraw, ImageFont

fonts = {'default': 'fonts/UltimaPro.otf',
         'default_bold' : 'fonts/UltimaPro-Bold.otf'}


def download_img(cover):
    response = requests.get(cover)
    filename = f'temp/{random.randrange(0, 999999, 5)}.jpg'
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename

#download_img('https://assets.ppy.sh/beatmaps/701330/covers/cover.jpg?1521173677')

def recent_score_img(data):
    title = data[0]["beatmapset"]["title"]
    cover_link = data[0]["beatmapset"]["covers"]['cover']
    artist = data[0]["beatmapset"]["artist"]
    mapper = data[0]["beatmapset"]["creator"]
    rank = data[0]["rank"]

    acc = float(data[0]['accuracy']) * 100
    acc = "%.2f" % acc

    pp = data[0]['pp']
    pp = "%.1f" % pp

    combo = data[0]['max_combo']
    miss = data[0]['statistics']['count_miss']
    count_50 = data[0]['statistics']['count_50']
    count_100 = data[0]['statistics']['count_100']
    count_300 = data[0]['statistics']['count_300']
    score = data[0]['score']

    #difficult = data[0]['beatmap']['version']

    image_name = download_img(cover_link)
    img = Image.open(image_name)
    area = (10, 10, 480, 250)
    crop_img =  img.crop(area)

    gradient = Image.open('img_templates/gradient.png')
    crop_img.paste(gradient, (0, 0), gradient)

    title_font = ImageFont.truetype(fonts['default_bold'], size=27)
    mapper_font = ImageFont.truetype(fonts['default'], size=18)
    score_det_font = ImageFont.truetype(fonts['default'], size=24)
    score_font = ImageFont.truetype(fonts['default_bold'], size=27)

    draw_text = ImageDraw.Draw(crop_img)
    draw_text.text((6, 6), title, font=title_font, fill='#ffffff')
    draw_text.text((9, 37), f'{artist} mapped by {mapper}', font=mapper_font, fill='#ffffff')

    draw_text.text((6, 76), f'{pp}pp | {acc}% acc | {combo}x', font=score_font, fill='#ffffff')

    draw_text.text((9, 124), 'Missed:', font=score_det_font, fill='#ffa0a9')
    draw_text.text((9, 154), '300:', font=score_det_font, fill='#cdfffb')
    draw_text.text((9, 184), '100:', font=score_det_font, fill='#bcffb5')
    draw_text.text((9, 214), '50:', font=score_det_font, fill='#ffe79c')

    draw_text.text((120, 124), str(miss), font=score_det_font, fill='#ffa0a9')
    draw_text.text((120, 154), str(count_300), font=score_det_font, fill='#cdfffb')
    draw_text.text((120, 184), str(count_100), font=score_det_font, fill='#bcffb5')
    draw_text.text((120, 214), str(count_50), font=score_det_font, fill='#ffe79c')

    draw_text.text((220, 210), f'Score: {str(score)}', font=score_font, fill='#ffffff')

    if rank.upper() == 'A':
        score_A = Image.open('img_templates/score_A.png')
    elif rank.upper() == 'B':
        score_A = Image.open('img_templates/score_B.png')
    elif rank.upper() == 'C':
        score_A = Image.open('img_templates/score_C.png')
    elif rank.upper() == 'D':
        score_A = Image.open('img_templates/score_D.png')
    elif rank.upper() == 'S':
        score_A = Image.open('img_templates/score_S.png')
    elif rank.upper() == 'SS':
        score_A = Image.open('img_templates/score_SS.png')
    elif rank.upper() == 'SH':
        score_A = Image.open('img_templates/score_SH.png')
    elif rank.upper() == 'SSH':
        score_A = Image.open('img_templates/score_SX.png')
    else:
        score_A = Image.open('img_templates/score_None.png')

    crop_img.paste(score_A, (365, 60), score_A)

    filename = f'temp/{random.randrange(0, 99999, 3)}.jpg'
    crop_img.save(filename)
    return filename
