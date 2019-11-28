import cv2

with open("media/park_joy_444_720p50.y4m", "rb") as temp_file:
    header = temp_file.readline().decode().split()
    print("header: ", header)
    imageWidth = int(header[1][1:])
    print(imageWidth)
    imageHeight = int(header[2][1:])
    print(imageHeight)
    yuvFormat = list(header[-1])[1:]
    print([int(n) for n in yuvFormat])

    temp_file.readline()
    yMatrix = temp_file.read(imageHeight * imageWidth)
    temp_file.read(imageHeight * imageWidth)
    temp_file.read(imageHeight * imageWidth)

    print(temp_file.readline())

    path = "/home/luis/Desktop/CSLP/p04/video-encoding/python/media/img01.png"

    image = cv2.imread(path)
    assert image is not None

    window_name = "pic"

    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

