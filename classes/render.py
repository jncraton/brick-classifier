import subprocess

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

for part in parts:
    with open('tmp.ldr', 'w') as f:
        f. write(f'1 71 0 0 0 1 0 0 0 1 0 0 0 1 {part}.dat')

    for lat in range(15, 360, 60):
        for lon in range(15, 360, 60):
            print(part, lat, lon)
            subprocess.run([
                'leocad', 
                '--image', f'{part}-{lat}-{lon}-center.png', 
                '--width', '160', 
                '--height', '160', 
                '--camera-angles', f'{lat}', f'{lon}', 
                'tmp.ldr'
            ], stderr=subprocess.DEVNULL)

            subprocess.run([
                'convert', 
                f'{part}-{lat}-{lon}-center.png',
                '-colorspace', 'Gray',
                '-gravity', 'center',
                '-extent', '180x180',
                f'{part}-{lat}-{lon}-center.png',
            ])

            for gravity in ['north', 'south', 'east', 'west', 'center']:
                for angle in ['-10', '10']:
                    subprocess.run([
                        'convert', 
                        f'{part}-{lat}-{lon}-center.png',
                        '-gravity', gravity,
                        '-extent', '224x224',
                        '-distort', 'SRT', angle,
                        f'{part}-{lat}-{lon}-{gravity}-{angle}.png',
                    ])
            
                subprocess.run([
                    'convert', 
                    f'{part}-{lat}-{lon}-center.png',
                    '-gravity', gravity,
                    '-extent', '224x224',
                    f'{part}-{lat}-{lon}-{gravity}.png',
                ])
