# using the Arcade library created by Paul Vincent Craven
# https://api.arcade.academy/en/latest/
import arcade
import arcade.gui
import random
import math
import csv
import os


""" -----Editable: Constants------ """
# setting the monitor dimensions and target distance
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
RADIUS = 250

# Refresh rate
RATE = 1 / 60  # 60 FPS

# Change this to where you want the files to be saved. The folder created
# will be the patient ID which doesn't need to be entered
ParentDir = '/Users/vivianli/Desktop'

"""-------END OF Editable Constants-------"""


"""-------Do not edit any code below this line-------"""

SEQUENCE_FILE = os.path.join(ParentDir, 'Sequence.csv')

# Number of Targets initialized to 0
TARGET_COUNT = 0
# List of Targets initialized
TARGET_LIST = []
# Number of plays initialized to 0
PLAYS = 0
# Patient ID initialized to 0
PATIENT_ID = 0


""" Circle Initialization """
# Generate all possible target coordinates on the desired circle and store in a list
circle_coordinate_x = []
circle_coordinate_y = []
# in a unit circle, coordinate is notated as (radius* cos(theta), radius* sin(theta))
for i in range(360):
    angle = i * math.pi / 180  # convert degrees to radians
    x = SCREEN_WIDTH / 2 + RADIUS * math.cos(angle)
    y = SCREEN_HEIGHT / 2 + RADIUS * math.sin(angle)
    circle_coordinate_x.append(x)
    circle_coordinate_y.append(y)


# Instruction view class
class SetUpView(arcade.View):
    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()
        # Create a Text Label
        patient_id_label = arcade.gui.UITextArea(text="Patient ID", width=450, height=40, font_size=24,
                                                 font_name="Arial")
        self.v_box.add(patient_id_label.with_space_around(bottom=0))
        # Create a User Input Field
        self.patient_id_field = arcade.gui.UIInputText(width=450, height=40, text=' ')
        self.patient_id_field.text = ''
        self.v_box.add(self.patient_id_field.with_border())

        # Create a start button
        start_button = arcade.gui.UIFlatButton(text="Start Game", width=200)
        start_button.on_click = self.on_buttonclick
        self.v_box.add(start_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def setup(self):
        """Parse Target coordinates from Sequence.csv (Comma Separated Values)"""
        # Initialize empty list to store the target coordinates
        target_list = []

        # Parsing coordinates into the list
        with open(SEQUENCE_FILE) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                temp = [row[0], row[1]]
                target_list.append(temp)

        global TARGET_LIST, TARGET_COUNT, PLAYS
        # Get rid of the headers in the list
        TARGET_LIST = target_list[1:len(target_list)]
        """------ END of Parsing -------"""

        # Number of Targets set to number of set of coordinates
        TARGET_COUNT = len(TARGET_LIST)
        # Number of plays set to 0
        PLAYS = 0

    def on_show(self):
        """ This is run once when we switch to this view"""
        arcade.set_background_color(arcade.csscolor.ORANGE)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.manager.draw()

    def on_buttonclick(self, event):
        game_view = PauseView()
        game_view.setup()
        self.window.show_view(game_view)

    def update(self, delta_time: float):
        global PATIENT_ID
        PATIENT_ID = self.patient_id_field.text


# Main game view class
class GameView(arcade.View):
    """ Our custom View class. """

    """ Initializer """

    def __init__(self, game_view):
        # Call the parent class initializer to set up our view
        super().__init__()
        self.game_view = game_view

        # Set window background to color white
        arcade.set_background_color(arcade.color.WHITE)

        # Variables that will hold sprite lists
        self.circle_list = None  # Invisible large circle
        self.player_list = None  # Cursor
        self.origin_list = None  # Return point in the centre
        self.target_list = None  # Random targets

        # Set up circle info
        self.circle_sprite = None

        # Set up player info
        self.player_sprite = None

        # Set up origin info
        self.origin_sprite = None

        # Set up target infor
        self.target_sprite = None

        # Lists that will store the player coordinates as it moves
        self.player_x = []
        self.player_y = []

        # Set my target folder path
        target_dir = os.path.join(ParentDir, str(PATIENT_ID))

        # Create folder
        os.makedirs(target_dir, exist_ok=True)

        # Set path of circle_hit csv file
        self.circle_hit_file = os.path.join(target_dir, str(PATIENT_ID) + "_circle_hit.csv")
        # Check if file already exists
        self.circle_file_exists = os.path.isfile(self.circle_hit_file)

        # A list of all the trajectory file paths
        self.trajectory_file = []
        for count in range(TARGET_COUNT):
            path = os.path.join(target_dir, str(PATIENT_ID) + "_trajectory" + str(count+1) + ".csv")
            self.trajectory_file.append(path)

        # Hide mouse cursor
        self.window.set_mouse_visible(False)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.circle_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.origin_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()

        for degree in range(360):
            circle_point = arcade.SpriteCircle(4, arcade.color.PURPLE, False)
            # Position the circle point from our pre-generated list
            circle_point.center_x = circle_coordinate_x[degree]
            circle_point.center_y = circle_coordinate_y[degree]
            # Add to list
            self.circle_list.append(circle_point)
        self.circle_list.alpha = 0  # set circle points to transparent

        # Set up the origin as a green circle
        self.origin_sprite = arcade.SpriteCircle(5, arcade.color.GREEN, False)
        self.origin_sprite.center_x = SCREEN_WIDTH / 2
        self.origin_sprite.center_y = SCREEN_HEIGHT / 2
        self.origin_list.append(self.origin_sprite)

        # Set up the player (cursor) as a black circle
        self.player_sprite = arcade.SpriteCircle(3, arcade.color.BLACK, False)
        self.player_sprite.center_x = self.game_view.player_sprite.center_x
        self.player_sprite.center_y = self.game_view.player_sprite.center_y
        self.player_list.append(self.player_sprite)
        self.player_list.alpha = 0  # Hide player when it's moving

        # Set up the target from the parsed coordinate list
        self.target_sprite = arcade.SpriteCircle(3, arcade.color.RED, False)
        self.target_sprite.center_x = int(TARGET_LIST[PLAYS-1][0])  # New target pointed to a new coordinate in each play
        self.target_sprite.center_y = int(TARGET_LIST[PLAYS-1][1])
        self.target_list.append(self.target_sprite)

    # Your drawing code goes here
    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        # Draw all the sprite lists
        self.circle_list.draw()
        self.origin_list.draw()
        self.player_list.draw()
        self.target_list.draw()

        arcade.draw_text("Hit the target", self.window.width / 2, self.window.height - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    # Player moves with the cursor action
    def on_mouse_motion(self, _x, _y, dx, dy):
        self.player_sprite.center_x = _x
        self.player_sprite.center_y = _y

    def update(self, delta_time):
        # Calls update on all sprites
        self.target_list.update()
        self.player_sprite.update()

        # Record Trajectory
        self.player_x.append(self.player_sprite.center_x)
        self.player_y.append(self.player_sprite.center_y)

        # Check where the player (cursor) hits the imaginary circle
        boundary_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.circle_list)
        # Once it hits the circle
        if boundary_hit_list:

            """ CSV Writing """
            """ Trajectory """
            # Writing to trajectory csv file
            with open(self.trajectory_file[PLAYS - 1], 'a') as csvfile:

                # Creating a csv writer object and write
                csvwriter = csv.writer(csvfile)

                # Field names in csv
                headers = ['X', 'Y']
                csvwriter.writerow(headers)

                # Data row of csv file
                for index in range(len(self.player_x)):
                    rows = [[self.player_x[index], self.player_y[index]]]
                    csvwriter.writerows(rows)

            """ Circle Hit """
            # Writing to circle_hit csv file
            with open(self.circle_hit_file, 'a') as csvfile:
                # Field names in csv
                headers = ['targetX', 'targetY', 'hitX', 'hitY']

                # Data rows of csv file
                rows = [[self.target_sprite.center_x, self.target_sprite.center_y, self.player_sprite.center_x,
                         self.player_sprite.center_y]]

                # Creating a csv writer object
                csvwriter = csv.writer(csvfile)

                if not self.circle_file_exists:
                    # Writing the fields only if file is newly created
                    csvwriter.writerow(headers)

                # Writing the data rows
                csvwriter.writerows(rows)

            # Show Pause view after every circle hit
            self.window.show_view(self.game_view)

            # Check length of target list. If it reaches our target count goal, flip to the GameOver view.
            if PLAYS == TARGET_COUNT:
                view = GameOverView()
                self.window.show_view(view)



class PauseView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_list = None  # Cursor
        self.origin_list = None  # Origin

        # Set up player info
        self.player_sprite = None

        # Set up origin info
        self.origin_sprite = None

        # Hide mouse cursor
        self.window.set_mouse_visible(False)

    def setup(self):
        # Reset targets counted
        self.player_list = arcade.SpriteList()
        self.origin_list = arcade.SpriteList()

        # Set up the player (cursor) as a black circle
        self.player_sprite = arcade.SpriteCircle(3, arcade.color.BLACK, False)
        self.player_sprite.center_x = SCREEN_WIDTH / 2 - 100
        self.player_sprite.center_y = SCREEN_HEIGHT / 2 - 100
        self.player_list.append(self.player_sprite)

        # Set up the origin as a green circle
        self.origin_sprite = arcade.SpriteCircle(5, arcade.color.GREEN, False)
        self.origin_sprite.center_x = SCREEN_WIDTH / 2
        self.origin_sprite.center_y = SCREEN_HEIGHT / 2
        self.origin_list.append(self.origin_sprite)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        # Draw Green Dot
        self.origin_list.draw()

        # Draw Player
        self.player_list.draw()

        # Instruction
        arcade.draw_text("Return to Green dot in the centre", self.window.width / 2, self.window.height - 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

        # Display targets left
        count_text = f"Targets left: {TARGET_COUNT - PLAYS}"
        arcade.draw_text(count_text, start_x=10, start_y=10, color=arcade.csscolor.BROWN, font_size=18)

    def on_mouse_motion(self, _x, _y, dx, dy):
        self.player_sprite.center_x = _x
        self.player_sprite.center_y = _y

        # Check if the player (cursor) hits the origin
        origin_hit = arcade.check_for_collision(self.player_sprite, self.origin_sprite)

        # When user moves back to origin, resume game
        if origin_hit:
            global PLAYS
            PLAYS += 1

            # go back to game view
            game_view = GameView(self)
            game_view.setup()
            self.window.show_view(game_view)



class GameOverView(arcade.View):
    """ View to show when game is over"""

    def __init__(self):
        """ This is run once when we switch to this view """
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create a restart button
        restart_button = arcade.gui.UIFlatButton(text="Restart Game", width=200)
        restart_button.on_click = self.on_buttonclick
        self.v_box.add(restart_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x", anchor_y="top", child=self.v_box))

        # Show mouse cursor
        self.window.set_mouse_visible(True)

    def on_draw(self):
        """ Draw this view """
        self.clear()
        arcade.draw_text("Thank You!", self.window.width / 2, self.window.height / 2, arcade.color.BLACK, font_size=50,
                         anchor_x="center")
        # Instruction
        arcade.draw_text("Edit and save new sequence file before restart", self.window.width / 2, 50,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        self.manager.draw()

    def on_buttonclick(self, event):
        start_view = SetUpView()
        start_view.setup()
        self.window.show_view(start_view)

    def on_mouse_press(self, _x: float, _y: float, button: int, modifiers: int):
        pass


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Sensorimotor Game")  # Create our window
    window.set_update_rate(RATE)  # Refresh rate
    start_view = SetUpView()  # Create our view
    start_view.setup()
    window.show_view(start_view)  # Show our view
    arcade.run()  # Keep the window open until the user hits the 'close' button


if __name__ == "__main__":
    main()
