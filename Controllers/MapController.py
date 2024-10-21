import os


def getMap():

# @app.get('/map'
    pgm_file = os.getcwd() + "/new.pgm"
    # image = Image.open(pgm_file)
    # # Rotate the image by 90 degrees (you can specify a different angle)
    # rotated_image = ImageOps.flip(image)
    #
    # rotated_image.save('new.pgm')
    # rotated_image.show()
    # exit()

    with open(pgm_file, 'rb') as f:  # Open the file in text mode for P2 format
        # Skip comments and metadata lines
        magic_number = f.readline().decode('utf-8').strip()
        if magic_number not in ['P2', 'P5']:
            raise ValueError("Invalid PGM format")

        # Skip comments and metadata lines
        while True:
            line = f.readline().decode('utf-8').strip()
            if not line.startswith('#'):
                break

        # Read PGM header
        width, height = map(int, line.split())
        print(width, height)
        max_val = int(f.readline())
        # print("max", f.read())

        # Read pixel values
        data = f.read()
        # print(data)
        #
        coordinates = []
        # coordinates = []
        X = []
        Y = []
        for w in range(width):
            for h in range(height):
                pixel_value = int(data[h * width + w])
                # # You may want to adjust the condition based on your specific requirements
                if pixel_value < 205:
                    # X.append(x)
                    # Y.append(y)
                    # coordinates.append((x, y))
                    coordinates.append({
                        'x': w,
                        'y': h
                    })

    return {"status": 1, "x": X, 'data': coordinates}