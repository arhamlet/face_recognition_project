# Face Recognition Project
The project is subdivided into three parts.

## Script 1
This part takes an input picture `test1` and outputs the faces in the `detected` folder.

## Script 2
This part takes the faces from the `detected` folder and a video `test.mp4` as the input and outputs a csv file `deets.csv`. Face recognition is applied on the video and the matches as well as their time interval of appearance are stored in the csv file.
This part has some short-comings with respect to obtaining time intervals for faces that leave and then reappear in the video. Needs some improvement.

## Script 3
In this part, the csv file `deets.csv` is taken as input along with the video `test.mp4`. The script obtains the name of the person and the interval of the appearance of that person from the csv file. Afterwards, it crops the video and generates a new video clip for each person of the interval mentioned in the csv file.

## Creating environment
Use the requirements file to create the environment in anaconda. Use the command

`conda env create --name projenv --file requirements.txt`