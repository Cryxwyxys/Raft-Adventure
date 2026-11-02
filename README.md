# Quick intro
A game about steering your raft down a river a canyon, using your physical input.
The game was developed as a three-week Erasmus school project between a school in Germany and a school in the Czech Republic.
The game is written in Python using the pygame library.
The controls are provided via a self-built "motion-input device" built with an Arduino Leonardo.

# The Game
The premise of the game is very simple: you steer a raft down an endless river and avoid stones and the cliffs on the side.
If you hit them, you lose a life; if you lose too many, you die.
You can pick up planks floating in the water to repair your raft and survive longer.
Your score is saved in a score.txt file, and you can even display the top 10 scores from the menu.

## Input
As mentioned, the input is provided via an Arduino Leonardo using HID.
In this case, the Leonardo simulates a joystick. This is done so the mouse can be used freely while the game is being played.
If no joystick is connected, the mouse is used for the game's controls.
Connected to the Leonardo is an MPU-6050 gyroscope/accelerometer, which is attached to a makeshift raft.
The gyroscope is used to measure the tilt of the raft so the player can steer the raft in the game by tilting the real one.
In our case, we used a Euro pallet as a raft and suspended it on tires, shifting our weight to tilt it.
