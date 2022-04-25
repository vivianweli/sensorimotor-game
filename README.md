# Sensorimotor Adaptation Game
This game is made to enable visuomotor research. It asks the patient to move the cursor from the centre of the screen towards a target placed on an invisible circle. An external tablet (e.g. Wacom tablet) is recommended to act as a large trackpad. 

## Setup
Download this repository and open the main.py in any IDE environment supporting Python 3.8.2. This game was made with the Arcade library (https://api.arcade.academy/en/latest/), which needs to be installed. 

### Customization
Open main.py and the editable constants should be marked in the top few lines. 
You can edit...
1. Game screen dimensions: width and height.
2. Radius of the invisible circle: targets should exist on the circumference of this circle.
 > :warning: Please make sure the target coordinates you select in Sequence.csv lie on the circle circumference with this radius.
3. Refresh rate: how frequently the program will capture your data. 
4. Parent Directory: this will be where your output csv files are saved. 

### Target Coordinates Selection 
1. Open the Sequence.csv file.
2. You can edit your target coordinates for your desired trial. Keep the headers 'targetX' and 'targetY'. 
3. Press Save. 
4. **Place this file in the Parent Directory you selected above!**
> Arcade uses the first quadrant, so all your coordinates must be positive!

## GamePlay
Run the program in your IDE. A trial composes of the following 4 stages. 
### Initialization
<img src="https://user-images.githubusercontent.com/104324501/165000377-9e91a0d9-3199-41ac-9c3f-7ad9e7f41f5c.png">

The patient ID has to be entered in the text box. Double-click the field before inputting. 
This ID will be the the name of the folder that contains all the output .csv files in your specified parent directory.
> :warning: Please keep this ID unique for each trial of each patient. If multiple trials (perhaps with a different Sequence.csv) are wished to be conducted on the same patient (e.g. ID = 3), either change the parent directory to avoid washing previous data OR varying the ID (e.g. ID = 3.1)
Press the Start game button to continue. 

> Note: there is currently a bug in the Arcade GUI implementation that will over-enlarge the second character and beyond, but the ID will still be parsed correctly. 
<img src="https://user-images.githubusercontent.com/104324501/165000400-8c6e4bc4-2c76-494e-b1ba-8b0435c7596d.png">
Navigate to the origin (green circle) to start the game. 

### Play 
<img src="https://user-images.githubusercontent.com/104324501/165000422-954a6d13-7cbd-41a5-b72b-f087f9d19eec.png">
The patient navigates the cursor to hit the target (red circle). The target coordinates are pre-determined based on your Sequence.csv file. The play ends when the cursor touches any point on the circumference of the invisible circle (not necessarily the target). The cursor is made invisible intentionally. 

### Recalibration
<img src="https://user-images.githubusercontent.com/104324501/165000410-4ab4eb93-229e-497e-91e3-062058189aa2.png">
The number of targets remaining is displayed at the bottom left corner. Patients have to move the cursor back to the origin before the next play where a new target will be displayed. 

### Game Over
<img src="https://user-images.githubusercontent.com/104324501/165000425-f9ddae61-804c-40a8-8608-d4a63f827065.png">
When all the targets are played, the game is over. To exit, simply close the window. 
To restart, press the restart button at the top. The game will take you back to the Initialization stage where a new trial will begin. 

- To run the same Sequence.csv: simply press restart and the next game will implement the same coordinates. 
- To run different Sequence.csv: make changes and SAVE the Sequence.csv file BEFORE pressing restart.

## Data Collected
In the desired parent directory, you will find a folder for each trial with each patient ID entered during gameplay as the folder name. For instance, ID = 3, then folder name is 3. 

### circle_hit.csv
<img src="https://user-images.githubusercontent.com/104324501/165001092-0482751f-94bc-490a-913e-6dbf7bba3110.png">
targetX and targetY are target coordinates specified in your Sequence.csv file. hitX and hitY indicate the coordinate of collision between the cursor and the invisible circle. Remember, the patient doesn't necessarily hit the target point. 

### trajectory#.csv
<img src="https://user-images.githubusercontent.com/104324501/165001326-2a822725-b59a-4a17-a216-80d528ba746c.png">
In each trial, the number of plays is determined by the number of target coordinates in the Sequence.csv file. For each play, a trajectory file is generated. In each play, coordinates are captured as the patient moves the cursor to hit the target. The number of data points recorded is dependent on the refresh rate. For instance, 120 Hz capture twice as frequency than 60 Hz. You will see that all trajectories start around the centre coordinates due to the Recalibration stage. 

## Footnotes and Credit
This game is an individual research project endeavor for the Memory, Action, & Cognition Lab (https://www.cartermaclab.org/) at McMaster University (Hamilton, Ontario, Canada). It was inspired by a similar program in the paper _Flexible explicit but rigid implicit learning in a visuomotor adaptation task_ (https://journals.physiology.org/doi/full/10.1152/jn.00009.2015) authored by Krista M. Bond and Jordan A. Taylor. 




