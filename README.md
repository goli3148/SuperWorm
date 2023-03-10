# SuperWorms
## Python and Pygame
This game is written in python with pygame library.

## Install Pygame Library
write this command in CMD of Windows:
```
...\> py -m pip install pygame
```
write this command in terminal of linux\Mac:
```
$ python -m pip install Django
```

## Play Game
In first Screen press any key and then you can direct the worm with keyboard.
In this Game calculating the level of game iss using:
```
level(t+1) = (level(t)^1.2)*2
```
this function is exponential so level increasing won't be linear.
increasing level will cause a random color for worm and fruit.
increasing level also cauese increasing Speed of the game.
