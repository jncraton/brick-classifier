import subprocess
import itertools
import os
import random

quick = False

random.seed(0)

# Most common parts since 2005 as of May 2021 (except 298c02
parts = [
'3023',
'3020',
'3022',
'6141',
'3004',
'3710',
'3021',
'3795',
'3069b',
'3010',
'3024',
'3005',
'3666',
'3003',
'54200',
'2412b',
'3062b',
'3623',
'3001',
'2431',
'3034',
'3068b',
'3039',
'3040b',
'4032a',
'3009',
'3031',
'2780',
'3660',
'3460',
'2420',
'3700',
'3622',
'3070b',
'3941',
'3032',
'4070',
'3665',
'32062',
'3002',
'4274',
'59900',
'85984',
'15573',
'2540',
'6636',
'98138',
'11477',
'2654',
'3832',
'43093',
'4740',
'3008',
'4519',
'3035',
'87079',
'87580',
'44728',
'30374',
'3713',
'4286',
'48336',
'4162',
'2432',
'3705',
'3937',
'4477',
'2357',
'3829c01',
'6091',
'3749',
'87087',
'2456',
'15068',
'3673',
'4081b',
'6558',
'3298',
'99780',
'60478',
'30414',
'6541',
'3701',
'32028',
'32123b',
'3706',
'63864',
'15712',
'50950',
'3036',
'60897',
'93273',
'32013',
'3958',
'11211',
'2445',
'2877',
'63868',
'59443',
]

color = 15
backgrounds = [3*c for c in ['9f', 'af', 'bf', 'cf', 'df', 'ef', 'ff']]
angles = list(itertools.product([301, 317, 332, 31, 43, 59], range(17,360,23)))
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
        lat += random.randint(-6, 6)
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
    
        shadowx = random.randint(-4, 4)
        shadowy = random.randint(1, 4)
        shadowintensity = hex(random.randint(60,90))[2:]
        blur = random.choice(blurs)
        noise_level = random.choice(noise_levels)
        part_brightness = random.randint(-70, 0)
        brightness = random.randint(-5, 5)
        bg = random.choice(backgrounds)
        rotation = random.randint(0, 360)
        
        subprocess.run([
            'convert',
            f'render.png',
            '-brightness-contrast', f'{part_brightness}',
            '-distort', 'SRT', f'{rotation}',
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

