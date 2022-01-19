from PIL import Image
from PIL import ImageDraw
import os
from tqdm import tqdm
import imageio
import math
import random
from collections import deque

def shift(arr, d):
    items = deque(arr)
    items.rotate(d)
    return list(items)

def getPalette(filename, colornumber):
    img = Image.open(filename)
    draw = ImageDraw.Draw(img)
    img = img.convert('P', palette=Image.ADAPTIVE, colors=int(
        colornumber))  # reduce cantidad de colores
    newfilename = filename.split('.')[0] + f'-{colornumber}.png'
    img.save(newfilename)
    img = Image.open(newfilename)
    palette = img.getpalette()  # guarda paleta en arreglo de 256*3 de largo
    tuple = []
    tuple_palette = []
    for i in range(len(palette)):  # guarda paleta en arreglo real de 256*3
        if i % 3 == 2:
            tuple.append(palette[i])
            tuple_palette.append(tuple)
            tuple = []
        else:
            tuple.append(palette[i])

    height, width = img.size
    map = {str(i):[] for i in range(colornumber)}
    for y in range(height):  # guarda coordenadas por color
        for x in range(width):
            pixel = img.getpixel((x, y))
            map[str(pixel)].append([x, y])

    color_table = []
    color_table_val = {}
    for i in range(colornumber):
        color_table.append(str(i)) # tabla de colores
        color_table_val[str(i)] = tuple_palette[i] # tabla de conversión
    return map, color_table, color_table_val

def paletteCycling(filename, colornumber):
    map, color_table, color_table_val = getPalette(filename, colornumber)
    newfilename = filename.split('.')[0] + f'-{colornumber}.png'
    img = Image.open(newfilename)
    folder = newfilename.split('.')[0]
    if not os.path.isdir(folder):
        os.mkdir(folder)
    os.chdir(folder)
    counter = 0
    print("\nPalette swapping...\n")
    for i in tqdm(range(int(colornumber))):
        for j in range(colornumber):
            for coord in map[str(j)]:
                color_rgb = color_table_val[str(color_table[j])]
                img.putpixel((coord[0], coord[1]),
                                (color_rgb[0], color_rgb[1], color_rgb[2]))
            img.save(newfilename.split('.')[0] + f'-{counter}.png')
            counter += 1
        color_table = shift(color_table, -1)

    images = []
    print("\nGenerating gif...\n")
    with imageio.get_writer('gif.gif', mode='I', duration=0.1) as writer:
        for i in tqdm(range(counter)):
            image = imageio.imread(newfilename.split('.')[0] + f'-{i}.png')
            writer.append_data(image)

#paletteCycling("martinyop.png",16)

def horizontalOscillation(filename, interval, distorsion, iter): # intervalo normal 0.012, distorsion 10 es piola 256 es brigido, iter 256 si quiero el largo, 90 para loop para img de 256x256
    map, color_table, color_table_val = getPalette(filename, 256)
    newfilename = filename.split('.')[0] + f'-256-{interval*1000}-{distorsion}-moved-horizontal.png'
    img = Image.open(filename)
    height, width = img.size
    image = {}
    for y in range(height): # guarda las filas de pixeles en un diccionario
        image[str(y)] = []
        for x in range(width):
            image[str(y)].append(img.getpixel((x, y)))
    folder = newfilename.split('.')[0]
    if not os.path.isdir(folder):
        os.mkdir(folder)
    os.chdir(folder)
    sin_count = 0
    print("\nVertical oscillation...\n")
    for i in tqdm(range(iter)): #
        for y in range(height):
            if i < iter//2:
                image[str(y)] = shift(image[str(y)],abs(math.floor(distorsion*math.sin(sin_count)))) # rota el arreglo
            else:
                image[str(y)] = shift(image[str(y)],-abs(math.floor(distorsion*math.sin(sin_count)))) # rota el arreglo. eliminar si es 256
            for x in range(width):
                color_rgb = image[str(y)][x] # saca el color del pixel
                img.putpixel((x, y),(color_rgb[0], color_rgb[1], color_rgb[2])) # cambia el color del pixel
            sin_count += interval
        img.save(newfilename.split('.')[0] + f'-{i}.png')

    print("\nGenerating gif...\n")
    with imageio.get_writer('gif.gif', mode='I', duration=0.1) as writer:
        for i in tqdm(range(iter)):
            image = imageio.imread(newfilename.split('.')[0] + f'-{i}.png')
            writer.append_data(image)

def verticalOscillation(filename, interval, distorsion, iter): # intervalo normal 0.012, distorsion 10 es piola 256 es brigido, iter 256 si quiero el largo, 90 para loop para img de 256x256
    map, color_table, color_table_val = getPalette(filename, 256)
    newfilename = filename.split('.')[0] + f'-256-{str(interval*1000)}-{str(distorsion)}-moved-vertical.png'
    img = Image.open(filename)
    height, width = img.size
    image = {}
    for x in range(width): # guarda las filas de pixeles en un diccionario
        image[str(x)] = []
        for y in range(height):
            image[str(x)].append(img.getpixel((x, y)))
    folder = newfilename.split('.')[0]
    if not os.path.isdir(folder):
        os.mkdir(folder)
    os.chdir(folder)
    sin_count = 0
    print("\nVertical oscillation...\n")
    for i in tqdm(range(iter)): #
        for x in range(width):
            if i < iter//2:
                image[str(x)] = shift(image[str(x)],abs(math.floor(distorsion*math.sin(sin_count)))) # rota el arreglo
            else:
                image[str(x)] = shift(image[str(x)],-abs(math.floor(distorsion*math.sin(sin_count)))) # rota el arreglo. eliminar si es 256
            for y in range(height):
                color_rgb = image[str(x)][y] # saca el color del pixel
                img.putpixel((x, y),(color_rgb[0], color_rgb[1], color_rgb[2])) # cambia el color del pixel
            sin_count += interval
        img.save(newfilename.split('.')[0] + f'-{i}.png')

    print("\nGenerating gif...\n")
    with imageio.get_writer('gif.gif', mode='I', duration=0.1) as writer:
        for i in tqdm(range(iter)):
            image = imageio.imread(newfilename.split('.')[0] + f'-{i}.png')
            writer.append_data(image)

#verticalOscillation("vacacionebase.png", 0.012, 10, 256)

# horizontalOscillation("martinyop.png",0.012,40,66)

def randomizeHorizontal(filename, iter, seed):
    map, color_table, color_table_val = getPalette(filename, 256)
    random.seed(seed)
    newfilename = filename.split('.')[0] + '-256-randomized-horizontal.png'
    img = Image.open(filename)
    height, width = img.size
    image = {}
    for y in range(height): # guarda las filas de pixeles en un diccionario
        image[str(y)] = []
        for x in range(width):
            image[str(y)].append(img.getpixel((x, y)))
    folder = newfilename.split('.')[0]
    if not os.path.isdir(folder):
        os.mkdir(folder)
    os.chdir(folder)
    print("\nRandomizing...\n")
    for i in tqdm(range(iter)):
        for y in range(height):
            image[str(y)] = shift(image[str(y)],random.randint(0,256)) # rota el arreglo
            for x in range(width):
                color_rgb = image[str(y)][x] # saca el color del pixel
                img.putpixel((x, y),(color_rgb[0], color_rgb[1], color_rgb[2])) # cambia el color del pixel
        img.save(newfilename.split('.')[0] + f'-{iter}-{i}.png')

    print("\nGenerating gif...\n")
    with imageio.get_writer('gif.gif', mode='I', duration=0.1) as writer:
        for i in tqdm(range(256)):
            image = imageio.imread(newfilename.split('.')[0] + f'-{iter}-{i}.png')
            writer.append_data(image)

def randomizeVertical(filename, iter, seed):
    map, color_table, color_table_val = getPalette(filename, 256)
    random.seed(seed)
    newfilename = filename.split('.')[0] + '-256-randomized-vertical.png'
    img = Image.open(filename)
    height, width = img.size
    image = {}
    for x in range(width): # guarda las filas de pixeles en un diccionario
        image[str(x)] = []
        for y in range(height):
            image[str(x)].append(img.getpixel((x, y)))
    folder = newfilename.split('.')[0]
    if not os.path.isdir(folder):
        os.mkdir(folder)
    os.chdir(folder)
    print("\nRandomizing...\n")
    for i in tqdm(range(iter)):
        for y in range(height):
            image[str(y)] = shift(image[str(y)],random.randint(0,256)) # rota el arreglo
            for x in range(width):
                color_rgb = image[str(y)][x] # saca el color del pixel
                img.putpixel((x, y),(color_rgb[0], color_rgb[1], color_rgb[2])) # cambia el color del pixel
        img.save(newfilename.split('.')[0] + f'-{iter}-{i}.png')

    print("\nGenerating gif...\n")
    with imageio.get_writer('gif.gif', mode='I', duration=0.1) as writer:
        for i in tqdm(range(256)):
            image = imageio.imread(newfilename.split('.')[0] + f'-{iter}-{i}.png')
            writer.append_data(image)

randomizeHorizontal("base.png", 256, 69)