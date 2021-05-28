import face_recognition
import os
import cv2
import csv

KNOWN_FACES_DIR = 'detected'
TOLERANCE = 0.6
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = 'hog'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model
video = cv2.VideoCapture('test.mp4')

# Returns (R, G, B) from name
def name_to_color(name):
    color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color

print('Loading known faces...')
known_faces = []
known_names = []
timer = []
data = []


for filename in os.listdir(KNOWN_FACES_DIR):

    # Next we load every file of faces of known person
    # Load an image
    image = face_recognition.load_image_file(f'{KNOWN_FACES_DIR}/{filename}')
    # Get 128-dimension face encoding
    encoding = face_recognition.face_encodings(image)[0]
    # Append encodings and name
    known_faces.append(encoding)
    known_names.append(filename[:len(filename)-4])



while True:
    # calculating the time in mili seconds
    millis = video.get(cv2.CAP_PROP_POS_MSEC)
    # Calculating the time using the formula number of frames/fps of the video
    fps = video.get(cv2.CAP_PROP_FPS)
    fpos = video.get(cv2.CAP_PROP_POS_FRAMES)
    time1 = float(fpos / fps)
    # if we want the number of frames
    #total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)

    ret, image = video.read()

    # Load image
    print(f'Filename {filename}', end='')

    # grabbing face locations
    locations = face_recognition.face_locations(image, model=MODEL)

    # Now since we know loctions, we can pass them to face_encodings as second argument
    # Without that it will search for faces once again slowing down whole process
    encodings = face_recognition.face_encodings(image, locations)

    print(f', found {len(encodings)} face(s)')
    for face_encoding, face_location in zip(encodings, locations):

        # We use compare_faces (but might use face_distance as well)
        # Returns array of True/False values in order of passed known_faces
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)


        # Since order is being preserved, we check if any face was found then grab index
        # then label (name) of first matching known face

        match = None
        if True in results:  # If at least one is true, get a name of first of found labels
            match = known_names[results.index(True)]
            print(f' - {match} from {results}')
            timer.append(time1)


            # Each location contains positions in order: top, right, bottom, left
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            # Get color by name using our fancy function
            color = name_to_color(match)

            # Paint frame
            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)

            # Now we need smaller, filled grame below for a name
            # This time we use bottom in both corners - to start from bottom and move 50 pixels down
            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2] + 22)

            # Paint frame
            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)

            # Wite a name
            cv2.putText(image, match, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
            print(timer)
            start_time = timer[0]
            end_time = timer[len(timer)-1]
            flag=False
            if data!=[]:
                for i in range(len(data)):
                    if data[i][0]==match and data[i][1]==start_time:
                        data.append([match, start_time, end_time])
                        data.pop(i)
                        flag=True
                if flag==False:
                    data.append([match, start_time, end_time])
            else:
                data.append([match, start_time, end_time])
            # writing the csv file
            with open('deets.csv', 'w', newline='') as f:
                header = (['Match', 'Starting time', 'Ending time'])
                thewriter = csv.writer(f, delimiter='\t', lineterminator='\n', )
                thewriter.writerow(header)
                thewriter.writerows(data)
    # Show image
    cv2.imshow(filename, image)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


