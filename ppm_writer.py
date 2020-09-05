import random

def make_ppm(file_name, buffer):
    height = len(buffer)
    width = len(buffer[0])

    file_name_with_ext = file_name + ".ppm"
    img = open(file_name_with_ext, "w")
    img.write("P3 {} {}\n".format(width, height))
    img.write("255\n")
    for y in range(height):
        for x in range(width):
            img.write("{} {} {}\t".format(*buffer[y][x]))
        img.write("\n")
    img.close()

if __name__ == "__main__":
    width = 1000
    height = 1000
    buffer = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(
                (random.randint(0,255), 
                random.randint(0,255),
                random.randint(0,255)))
        buffer.append(row)

    make_ppm("pic", buffer)
