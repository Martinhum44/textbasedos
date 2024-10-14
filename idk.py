import os
import shutil
import cv2
import numpy as np
import BTH
import time
import keyboard
import math

currdir = "text-based OS"
createNewFile = True
for fileName in os.listdir():
  if fileName == "text-based OS":
    createNewFile = False
    break

if createNewFile:
  os.makedirs("text-based OS")

class Video:
  def __init__(self, fps, width, height):
    self.fps:int = fps
    self.frames:list[list[int]] = []
    if self.fps < 0:
      raise ValueError("frames per second cannot be less than 0")
    if self.fps > 100:
      raise ValueError("frames per second cannot be more than 100")
    self.width:int = abs(width)
    self.height:int = abs(height)
  
  def __len__(self):
    return math.floor(len(self.frames)/self.fps*1000)

  def __iter__(self):
    self.index = 0
    return self
  
  def __next__(self):
    if(self.index < len(self.frames)):
      result = self.frames[self.index]
      self.index += 1 
      return result
    else:
      self.index = 0
      raise StopIteration
  
  def getVideoDetails(self):
    return (self.frames, self.fps, (self.width, self.height))
  
  def append(self, frame):
    if len(frame) != self.height and len(frame[0]) != self.width:
      raise ValueError(f"invalid height and width values. Expected: height: {self.height} width: {self.width} \n Got: height: {len(frame)} width: {len(frame)}")
    self.frames.append(frame)
  
  def save(self, path):
    if os.path.exists(path):
      raise FileExistsError(f"File at path {path} already exists")
    
    if len(self.frames) == 0:
      raise ValueError("frames amount must be grater than zero")
    
    out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*"DIVX"),self.getVideoDetails()[1],self.getVideoDetails()[2])
    for frame in self:
      frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
      out.write(frame)
    out.release()
  
  def __getitem__(self, index):
    return self.frames[index]
  
class PlayingVideo(Video):
  def __init__(self, fps, width, height):
    super().__init__(fps, width, height)
    self.current_frame = None
    self.numbered_frame = None

  def append(self, frame):
    if len(frame) != self.height and len(frame[0]) != self.width:
      raise ValueError(f"invalid height and width values. Expected: height: {self.height} width: {self.width} \n Got: height: {len(frame)} width: {len(frame)}")
    self.frames.append(frame)
    if self.current_frame is None:
      self.changeCurrentFrame(0)
 
  def changeCurrentFrame(self, to):
    if to >= len(self.frames):
      raise IndexError("Last Frame Reached")
    
    if to < 0:
      raise IndexError("'to' value is less than 0")
    
    self.current_frame = cv2.cvtColor(self[to], cv2.COLOR_BGR2GRAY)
    self.numbered_frame = to
  
  def printCurrentFrame(self):
    frame = self.current_frame
    for line in frame:
      mapped_line = [numberToText(pixel) for pixel in line]
      print("".join(mapped_line))

def kilosMegasYKWIM(data):
  if data < 1000:
    return f"{data}B"
  elif data > 999 and data < 1000000:
    return f"{(data/1000)}KB"
  else:
    return f"{(data/1000000)}MB"

def numberToText(pixel):
  if pixel < 40:
    return "@@"
  elif pixel < 80:
    return "$$"
  elif pixel < 120:
    return "??"
  elif pixel < 160:
    return "**"
  elif pixel < 200:
    return "--"
  elif pixel < 240:
    return ".."
  else:
    return "  "

def createFile(fileName, contents):
  with open(currdir + "/" + fileName, "w") as newFile:
    newFile.write(contents)
  print(f"successfuly created a new file at {currdir}")


def createDirectory(dirName):
  os.makedirs(currdir + "/" + dirName)
  print(f"made new directory at {currdir}")


def deleteFile(fileName):
  try:
    size = BTH.getSize("text-based OS/" + fileName)
    os.remove("text-based OS/" + fileName)
    print(f"file: {fileName} deleted. \n freed up {kilosMegasYKWIM(size)}")
  except FileNotFoundError:
    print(f"file {fileName} not found")
  except Exception:
    print("something went wrong")
    print("")


def readFile(fileName):
  try:
    if fileName.endswith(".txt"):
      size = BTH.getSize(currdir + "/" + fileName)
      print(f"file: {fileName}")
      print("")
      with open(currdir + "/" + fileName, "r") as file:
        print(file.read())
        print("")
        print(f"size of file: {kilosMegasYKWIM(size)}")
        print("")
        print("")
    elif fileName.endswith(".png") or fileName.endswith(".jpg") or fileName.endswith(".jpeg"):
      size = BTH.getSize(currdir + "/" + fileName)
      if size > 10000:
        print(f"image file too large to render. \n Maximum size: 10KB \n file size: {kilosMegasYKWIM(size)} \n use the 'cmp' command to compress s file")
      else:
        img = cv2.imread(currdir + "/" + fileName)
        fileArray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(f"Size of image: {len(fileArray)}x{len(fileArray[0])} \n")
        for line in fileArray:
          _line = [numberToText(pixel) for pixel in line]
          print("".join(_line))
        print("")
        print(f"size of file: {kilosMegasYKWIM(size)}")
        print("")
        print("")
    else:
      print("file type not supported")
  except FileNotFoundError as e:
    print(f"file {fileName} not found. Detailed error: {e}")
  except Exception as e:
    print(f"something went wrong. More details: {e}")


def viewDisc():
  discSize = 0
  print(currdir + ":")
  print("----------------------------------------------")
  for file in os.listdir(currdir):
    if os.path.isfile(currdir + "/" + file):
      size = BTH.getSize(currdir + "/" + file)
      print(f"file: {file}   {kilosMegasYKWIM(size)}")
      print("")
      discSize += size
    elif os.path.isdir(currdir + "/" + file):
      print(f"directory: {file}")
      print("")

  print("----------------------------------------------")
  print(f"size of {currdir}: {kilosMegasYKWIM(discSize)}")


def overwriteFile(fileName, contents):
  if(os.path.splitext(fileName)[1] != ".txt"):
    return print("only .txt files are supported")
  
  if os.path.exists(currdir + "/" + fileName):
    with open(currdir + "/" + fileName, "r") as f:
      print(f"file contents: \n{f.read()}")

    with open(currdir + "/" + fileName, "w") as f:
      f.write(contents)
      print(f"overwritten file {fileName} successfully")
  else:
    print("file does not exist")


def changeDir(dir):
  global currdir
  if os.path.exists("text-based OS/" +
                    dir) and os.path.isdir("text-based OS/" + dir):
    currdir = "text-based OS/" + dir
    print(f"changed directory to {dir}")
    print("")
  else:
    print("path does not exist")


def deleteDir(dirName):
  if os.path.isdir(f"{currdir}/{dirName}"):
    shutil.rmtree(f"{currdir}/{dirName}")
    print(f"successfully deleted directory at {currdir}")
  else:
    print(f"directory does not exist in {currdir}")


def format():
  try:
    for file in os.listdir("text-based OS"):
      if os.path.isfile("text-based OS/" + file):
        os.remove("text-based OS/" + file)
      else:
        shutil.rmtree("text-based OS/" + file)

  except Exception as e:
    print(f"something went wrong. More details: {e}")
  else:
    print("formatted OS successfully")
    changeDir("")


def move(which, where):
  try:
    if os.path.exists(currdir+"/"+which):
      shutil.move(currdir+"/"+which, "text-based OS/"+where)
      print(f"file {which} moved to directory {where}")
    else:
      print("file does not exist")
  except FileNotFoundError:
    print("directory does not exist")
  except Exception as e:
    print(f"something went wrong. More details: {e}")

def paint(where) -> None:
  try:
    if os.path.exists(f"{currdir}/{where}"):
      return print(f"file {where} already exists")

    if os.path.splitext(where)[1] not in [".png", ".jpg", ".jpeg"]:
      return print(f"file type {os.path.splitext(where)[1]} not supported")

    try:
      height = int(input("image height: "))
      width = int(input("image width: "))
    except ValueError:
      return print("Witdh and height must be numbers")

    if height*width > 10000:
      return print("Image size cannot be grater than 10000 pixels")

    print("\n currently painted photo: ")
    print("[]\n")
    
    photo = []
    charPhoto = []
    for line in range(height):
      line1 = []
      charLine = []
      try:
        for pixel in range(width):
          inp = input(f"darkness of pixel {line}x{pixel} (9 lightest 0 darkest): \n type 'e' to exit \n")
          if inp == "e":
            raise InterruptedError("Image creation exited")
          darkness = int(inp)*27
            
          while (darkness > 255 or darkness < 0):
            
            print(f"Expected darkness to be from 0 to 9. darkness={inp} ")
            inp = input(f"darkness of pixel {line}x{pixel} (9 lightest 0 darkest): \n type 'e' to exit \n")
            if inp == "e":
              raise InterruptedError("Image creation exited")
            darkness = int(inp)*27
            
          line1.append(darkness)
          charLine.append(numberToText(darkness))
          print(" \n currently painted photo: ")
          
          for list in charPhoto:
            print("".join(list))
          if pixel == width-1:
            print("".join(charLine)+"\n[]")
          else:
            print("".join(charLine)+"[]")
          
          print("")          
        charPhoto.append(charLine)
        photo.append(line1)
          
      except ValueError as e:
          print(f"Expected darkness to be number type. Detailed error: {e} \n Image creation exited due to error.")
          break
      except InterruptedError as e:
          print(e)
          break
    else:
      photo = np.array(photo, dtype=np.uint8)
      cv2.imwrite(f"{currdir}/{where}", photo)
      print(f"Successfully saved image to {currdir}/{where}")

  except Exception as e:
    print(f"Something went wrong. Detailed error: {e}")

def takePhoto(where) -> None:
  try:
    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
      return print("Could not open camera")

    _, ext = os.path.splitext(where)
    if ext != ".png" :
      return print(f"image type {ext} not supported. Only .png is supported")
    
    if os.path.exists(f"{currdir}/{where}"):
      return print(f"file {where} already exists in directory {currdir}.")

    print("Opening camera in 3 seconds. \n Press space to exit \n press the 't' key to take a photo")
    time.sleep(3)

    while True:
      ret, frame = capture.read()

      if not ret:
        print("Could not read frame")
      photo = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
      photo = cv2.resize(photo, (50,30), interpolation=cv2.INTER_AREA)
      for line in photo:
        _line = [numberToText(pixel) for pixel in line]
        print("".join(_line))
      print("")

      if keyboard.is_pressed("space"):
         print("Photo taking exited")
         break 
      
      if keyboard.is_pressed("t"):
        cv2.imwrite(f"{currdir}/{where}", photo)
        print(f"Took photo and saved it to {currdir}/{where}")
        break
      cv2.waitKey(50)
        
  
  except FileExistsError:
    print(f"file {where} already exists in directory {currdir}.")

def captureVideo(where) -> None:
  DIR:str = f"{currdir}/{where}"
  try:
    capture = cv2.VideoCapture(0)

    if not capture.isOpened():
      return print("Could not open camera")

    _, ext = os.path.splitext(where)
    if ext != ".mp4" :
      return print(f"video type {ext} not supported. Only .mp4 is supported")
    FPS = int(input("Frames per second for this video: "))
    VIDEO = Video(FPS, 50, 30)
    print("Recording video in 3 seconds. \n Press space to stop recording.")
    time.sleep(3)

    while True:
      ret, frame = capture.read()

      if not ret:
        print("Could not read frame")
      photo = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
      photo = cv2.resize(photo, (50,30), interpolation=cv2.INTER_AREA)
      for line in photo:
        _line = [numberToText(pixel) for pixel in line]
        print("".join(_line))
      print("")
      VIDEO.append(photo)

      if keyboard.is_pressed("space"):
         print("Video capturing exited")
         break 
      
      cv2.waitKey(int(1000//VIDEO.getVideoDetails()[1]))
    capture.release()

    save = input("Save the video? (Y/N) \n")

    if save.strip() == "y" or save.strip() == "Y":
      details = VIDEO.getVideoDetails()
      VIDEO.save(DIR)
      print(f"Video saved to path {where}")
      print("")
      print(f"Video details: \n Duration: {len(VIDEO)/1000} seconds \n Framerate: {details[1]} FPS \n Amount of frames: {len(details[0])} \n File size: {kilosMegasYKWIM((BTH.getSize(DIR)))}")
    else:
      print("Video discarded "+save)

  except FileExistsError as e:
    return print(e)
  
  except ValueError as e:
    return print(e)

def viewVideo(path) -> None:
  DIR:str = f"{currdir}/{path}"
  if not os.path.exists(DIR):
    return print(f"path {path} does not exist")
  
  _, ext = os.path.splitext(path)
  if ext != ".mp4" :
    return print(f"video type {ext} not supported. Only .mp4 is supported")
  
  cap = cv2.VideoCapture(DIR)
  FPS = cap.get(cv2.CAP_PROP_FPS)
  WIDTH = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
  HEIGHT = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
  VIDEO = PlayingVideo(int(FPS), int(WIDTH), int(HEIGHT))

  while True:
    ret, frame = cap.read()
    if not ret:
      break
    VIDEO.append(frame)
  cap.release()

  print("Playing video in 3 seconds \n e to exit \n p to pause")
  time.sleep(3)
  for frame in VIDEO:
    try:
      print("")
      VIDEO.printCurrentFrame()
      VIDEO.changeCurrentFrame(VIDEO.numbered_frame+1)
      if keyboard.is_pressed("e"):
        print(" \n Video watching exited \n")
        break
      if keyboard.is_pressed("p"):
        print(f" \n Video paused at frame {VIDEO.numbered_frame}, second {float(VIDEO.numbered_frame/FPS)}  \n 'u' to unpause \n hold 'b' to rewind \n hold 'f' to go foward")
        while not keyboard.is_pressed("u"):
          if keyboard.is_pressed("f"):
            if VIDEO.numbered_frame == len(VIDEO.getVideoDetails()[0])-1:
              VIDEO.changeCurrentFrame(0)
            else:
              VIDEO.changeCurrentFrame(VIDEO.numbered_frame+1)
            VIDEO.printCurrentFrame()
            print(f" \n Video paused at frame {VIDEO.numbered_frame}, second {float(VIDEO.numbered_frame/FPS)}  \n 'u' to unpause \n hold 'b' to rewind \n hold 'f' to go foward")

          if keyboard.is_pressed("b"):
            if VIDEO.numbered_frame == 0:
              VIDEO.changeCurrentFrame(len(VIDEO.getVideoDetails()[0])-1)
            else:
              VIDEO.changeCurrentFrame(VIDEO.numbered_frame-1)
            VIDEO.printCurrentFrame()
            print(f" \n Video paused at frame {VIDEO.numbered_frame}, second {float(VIDEO.numbered_frame/FPS)}  \n 'u' to unpause \n hold 'b' to rewind \n hold 'f' to go foward")
      time.sleep(1/VIDEO.getVideoDetails()[1])
    except IndexError as e:
      print("")
      print(e)
  details = VIDEO.getVideoDetails()
  print(f"Video details: \n Duration: {len(VIDEO)/1000} seconds \n Framerate: {details[1]} FPS \n Amount of frames: {len(details[0])} \n File size: {kilosMegasYKWIM((BTH.getSize(DIR)))}")
  
while True:
  cho = input(f"""

  {currdir}
  
  commands:
  rdf: read file
  cfl: create file
  cdr: create directory
  dfl: delete file
  ddr: delete directory
  owf: overwrite file
  chd: change directory
  dis: display current directory
  mve: move file to
  pnt: paint and save as and image file to file 
  tke: take a picture and save as an image file to file 
  rec: record a video and save to
  fmt: format OS (WARNING: YOU'LL LOSE ALL YOUR FILES)
  viw: view recorded video
  """)
  print("")

  if cho[:3] == "cfl":
    contents = input("file contents: \n")
    createFile(cho[4:], contents)

  elif cho[:3] == "cdr":
    createDirectory(cho[4:])

  elif cho[:3] == "dfl":
    deleteFile(cho[4:])

  elif cho[:3] == "ddr":
    deleteDir(cho[4:])

  elif cho[:3] == "owf":
    contents = input("new file contents: \n")
    overwriteFile(cho[4:], contents)

  elif cho[:3] == "chd":
    changeDir(cho[4:])

  elif cho[:3] == "rdf":
    readFile(cho[4:])

  elif cho[:3] == "dis":
    viewDisc()

  elif cho[:3] == "fmt":
    format()

  elif cho[:3] == "mve":
    fose = input("move file to:")
    move(cho[4:], fose)
    
  elif cho[:3] == "pnt":
    paint(cho[4:])

  elif cho[:3] == "tke":
    takePhoto(cho[4:])

  elif cho[:3] == "rec":
    captureVideo(cho[4:])
  
  elif cho[:3] == "viw":
    viewVideo(cho[4:])
    
  else:
    print("command does not exist")
