import subprocess
import itertools
import os

quick = True

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

colors = ['71', '72', '0', '15']
backgrounds = ['999999', 'aaaaaa', 'cccccc', 'dddddd', 'eeeeee', 'ffffff']
angles = list(itertools.product([271, 313, 343, 17, 49, 77], range(17,360,47)))
rotations = ['0', '90', '180', '270']

if quick:
    colors = ['71']
    angles = list(itertools.product([17], [17]))

print(f"Generating {len(angles) * len(colors) * len(backgrounds) * len(rotations)} renders per class")

i = 0

for part in parts:
    try:
        os.mkdir(part)
    except FileExistsError:
        pass

    for color in colors:
        with open('tmp.ldr', 'w') as f:
            f. write(f'1 {color} 0 0 0 1 0 0 0 1 0 0 0 1 {part}.dat')

        for lat,lon in angles:
            subprocess.run([
                'leocad', 
                '--image', f'{part}/{lat}-{lon}-{color}-ffffff.png', 
                '--width', '160', 
                '--height', '160', 
                '--camera-angles', f'{lat}', f'{lon}', 
                'tmp.ldr'
            ], stderr=subprocess.DEVNULL)

            i = i + 1
            print(f'Rendering {part} in color {color} from position {lat}, {lon} ({i} of {len(parts) * len(colors) * len(angles)})')

            for bg in backgrounds:
                subprocess.run([
                    'convert', 
                    f'{part}/{lat}-{lon}-{color}-ffffff.png',
                    '-background', f'#{bg}',
                    '-colorspace', 'Gray',
                    '-gravity', 'center',
                    '-extent', '256x256',
                    '-blur', '2x2',
                    f'{part}/{lat}-{lon}-{color}-{bg}.png',
                ])

                for rotation in rotations[1:]:
                    subprocess.run([
                        'convert', 
                        f'{part}/{lat}-{lon}-{color}-{bg}.png',
                        '-rotate', rotation,
                        f'{part}/{lat}-{lon}-{color}-{bg}-{rotation}.png',
                    ])

