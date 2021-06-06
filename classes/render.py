import subprocess
import itertools
import os

parts = [
    '3001',
    '3002',
    '3003',
    '3004',
    '3005',
    '3006',
    '3007',
    '3008',
    '3009',
    '3010',
]

colors = ['71', '72', '0', '15']
backgrounds = ['999999', 'aaaaaa', 'cccccc', 'dddddd', 'eeeeee', 'ffffff']
angles = list(itertools.product([271, 313, 343, 17, 49, 77], range(17,360,47)))
num_rotations = 4

print(f"Generating {len(angles) * len(colors) * len(backgrounds) * num_rotations} renders per class")

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

            print(f'Rendering {part} in color {color} from position {lat}, {lon} ({i} of {len(parts) * len(colors) * len(angles)})')
            i = i + 1

            for bg in backgrounds:

                subprocess.run([
                    'convert', 
                    f'{part}/{lat}-{lon}-{color}-ffffff.png',
                    '-background', f'#{bg}',
                    '-gravity', 'center',
                    '-extent', '256x256',
                    f'{part}/{lat}-{lon}-{color}-{bg}.png',
                ])

                for rotation in ['90', '180', '270']:
                    subprocess.run([
                        'convert', 
                        f'{part}/{lat}-{lon}-{color}-ffffff.png',
                        '-rotate', rotation,
                        f'{part}/{lat}-{lon}-{color}-{bg}-{rotation}.png',
                    ])

