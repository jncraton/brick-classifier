import subprocess
import itertools
import os
import random

quick = False

random.seed(0)

parts = [
    '6141',
    '3023',
    '3024',
    '98138',
    '3069b',
    '3004',
    '54200',
    '3710',
    '3005',
    '3020',
]

color = 15
backgrounds = [3*c for c in ['9f', 'af', 'bf', 'cf', 'df', 'ef', 'ff']]
angles = list(itertools.product([a % 360 for a in range(273,360+87,11)], range(17,360,13)))
rotations = ['0', '90', '180', '270']
noise_levels = ['1', '2', '3']
blurs = ['1x1', '2x2']

if quick:
    angles = list(itertools.product([17], [17]))

print(f"Generating {len(angles)} images per class")

render = 0
image = 0

try:
    os.mkdir('train')
except FileExistsError:
    pass
try:
    os.mkdir('val')
except FileExistsError:
    pass
for part in parts:
    try:
        os.mkdir(f'train/{part}')
    except FileExistsError:
        pass
    try:
        os.mkdir(f'val/{part}')
    except FileExistsError:
        pass

    with open('tmp.ldr', 'w') as f:
        f. write(f'1 {color} 0 0 0 1 0 0 0 1 0 0 0 1 {part}.dat')

    for lat,lon in angles:
        lat += random.randint(-3, 3)
        lon += random.randint(-5, 5)

        render = render + 1
        print(f'Rendering {part} from position {lat}, {lon} (render {render} of {len(parts)  * len(angles)})')

        subprocess.run([
            'leocad', 
            '--image', f'render.png', 
            '--width', '160', 
            '--height', '160', 
            '--camera-angles', f'{lat}', f'{lon}', 
            'tmp.ldr'
        ], stderr=subprocess.DEVNULL)

        image += 1
        dataset = 'train' if (image % 10) else 'val'
    
        rotation = random.choice(rotations)
        shadowx = random.randint(-4, 4)
        shadowy = random.randint(1, 4)
        shadowintensity = hex(random.randint(60,90))[2:]
        blur = random.choice(blurs)
        noise_level = random.choice(noise_levels)
        part_brightness = random.randint(-70, 0)
        brightness = random.randint(-5, 5)
        bg = random.choice(backgrounds)
        
        subprocess.run([
            'convert',
            f'render.png',
            '-brightness-contrast', f'{part_brightness}',
            '-rotate', rotation,
            '(', '-clone', '0', '-background', 'gray', '-shadow', f'80x3{shadowx:+}{shadowy:+}', ')',
            '-reverse', '-background', f'#{bg}', '-layers', 'merge', '+repage',
            '-gravity', 'center',
            '-extent', '256x256',
            '-colorspace', 'Gray',
            '-attenuate', f'0.{noise_level}',
            '+noise', 'Laplacian',
            '-blur', blur,
            '-colorspace', 'Gray',
            '-brightness-contrast', f'{brightness}',
            f'{dataset}/{part}/{lat}-{lon}-{bg}-{rotation}-{noise_level}-{blur}{part_brightness}.png',
        ])

        os.unlink(f'render.png')

