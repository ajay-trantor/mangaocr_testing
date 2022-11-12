import os
import nagisa
from manga_ocr import MangaOcr
import numpy as np
import json

def perform_ocr(coords_file, image_path):
    with open(coords_file, 'r') as f:
        coords_dict = json.load(f)
    coords = coords_dict['coords']
    word_coords = {'ocr data': []}
    mocr = MangaOcr()
    for coord, img in zip(coords, os.listdir(image_path)) :
        centroids = coord['centroids']
        x1, y1 = coord['bbox']['x1'], coord['bbox']['y1']
        x2, y2 = coord['bbox']['x2'], coord['bbox']['y2']
        if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0 or len(centroids) == 0:
            pass
        else:
            cropped_image = os.path.join(image_path, img)
            text = mocr(cropped_image)
            # print(text)
            words = nagisa.tagging(text).words

            data = {'x': [], 'y': [], 'words': []}
            data['x'].append(x1)
            centroid_num = 0
            for word in words:
                data['words'].append(word)
                if len(words) > 1:
                    centroid_num += len(word)
                    try:
                        cent_coords = centroids[centroid_num - 1]
                        # centroid_val = cent_coords['x']
                        data['x'].append(cent_coords['x'])
                    except IndexError:
                        continue
                else:
                    pass
            data['x'].append(x2)
            data['y'] = [y1, y2]
            word_coords['ocr data'].append(data)
    return word_coords


def reformat_coords(word_coords):
    # word_coords, image = perform_ocr()
    reformated_output = {'coordinates': [], 'words':[]}
    coords_list = word_coords['ocr data']
    for coords in coords_list:
        x = coords['x']
        y = coords['y']
        words = coords['words']
        for x_index, x_val in enumerate(x):
            if x_index + 1 != len(x):
                try:
                    reformated_output['coordinates'].append(
                        {'x0': x_val, 'y0': y[0], 'x1':x[x_index + 1], 'y1':y[0],'x2': x[x_index + 1], 'y2': y[1], 'x3': x_val, 'y3': y[1]})
                    reformated_output['words'].append((words[x_index],-1))
                    # cv.rectangle(image, (x_val, y[0]), (x[x_index + 1], y[1]), (0, 255, 0), 1)
                except IndexError:
                    continue
            else:
                print(x_index)
    return reformated_output

