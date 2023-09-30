import sys
from time import sleep
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QFileDialog
import pygame
import os
import threading
import random

app = QApplication(sys.argv)
app.setStyleSheet("QWidget { background-color: #1e283a; color: #eaebec; }")

window = QWidget()
window.setGeometry(100, 100, 280, 80)
window.setWindowTitle("Background Music")
layout = QGridLayout()
toggleButton = QPushButton("Start Music")
timeLabel = QLabel("0:00 | 0:00")
layout.addWidget(toggleButton)
layout.addWidget(timeLabel)
window.setLayout(layout)

pygame.mixer.init()

unpaused = False

toplay = [("music/" + f) for f in os.listdir("music")]

for i in range(len(toplay)):
  temp = toplay[i]
  j = random.randint(0, len(toplay) - 1)
  toplay[i] = toplay[j]
  toplay[j] = temp

pygame.mixer.music.load(toplay[0])

currentlength = str(int(divmod(pygame.mixer.Sound(toplay[0]).get_length(), 60)[0])) + ":" + str(int(divmod(pygame.mixer.Sound(toplay[0]).get_length(), 60)[1]))

pygame.mixer.music.play()
pygame.mixer.music.pause()

def toggle_music():
  global unpaused
  if toggleButton.text() == "Start Music":
    toggleButton.setText("Stop Music")
    pygame.mixer.music.unpause()
    sleep(0.01)
    unpaused = True
  else:
    toggleButton.setText("Start Music")
    unpaused = False
    pygame.mixer.music.pause()

def run_playlist():
  global toplay, unpaused, currentlength
  while True:
    sleep(0.01)
    timeLabel.setText(str(int(divmod(pygame.mixer.music.get_pos() / 1000, 60)[0])) + ":" + str(int(divmod(pygame.mixer.music.get_pos() / 1000, 60)[1])) + " | " + currentlength)
    if not pygame.mixer.music.get_busy() and unpaused:
      toplay = toplay[1:] + [toplay[0]]
      pygame.mixer.music.load(toplay[0])
      currentlength = str(int(divmod(pygame.mixer.Sound(toplay[0]).get_length(), 60)[0])) + ":" + str(int(divmod(pygame.mixer.Sound(toplay[0]).get_length(), 60)[1]))
      pygame.mixer.music.play()

toggleButton.clicked.connect(toggle_music)
playlist_thread = threading.Thread(target=run_playlist)
playlist_thread.daemon = True
playlist_thread.start()

window.show()

sys.exit(app.exec_())
