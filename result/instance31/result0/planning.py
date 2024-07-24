from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj

    # Object physical properties predicates
    is_rigid: bool = False
    is_foldable: bool = False
    is_elastic: bool = False
    is_fragile: bool = False

    # bin_packing predicates expressed as a boolean (max 2)
    is_in_box: bool = False
    is_out_box: bool = True


class Robot:
    # Define skills
    def __init__(self,
                 name: str = "UR5",
                 goal: str = None,
                 actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
    
        self.robot_handempty = True
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Preconditions
        if obj.is_out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_out_box = False
            obj.is_in_box = False
            print(f"Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj:
            # Effects
            self.state_handempty()
            obj.is_in_box = True
            obj.is_out_box = False
            print(f"Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.is_in_box:
            # Effects
            print(f"Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable:
            # Effects
            print(f"Fold {obj.name}")
    
    def pick_out(self, obj, bin):
        # Preconditions
        if obj.is_in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.is_in_box = False
            obj.is_out_box = True
            self.state_handempty()
            print(f"Pick_Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


# Create objects based on the initial state
object0 = Object(index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj', is_rigid=True, is_in_box=False, is_out_box=True)
object1 = Object(index=1, name='beige_1D_ring', color='beige', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=False, is_out_box=True)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', is_elastic=True, is_in_box=False, is_out_box=True)
object3 = Object(index=3, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj', is_fragile=True, is_foldable=True, is_in_box=True, is_out_box=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', is_in_box=False, is_out_box=False)

# Create the robot
robot = Robot()

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal: All objects should be in the white_box
    goal_state = {
        'yellow_3D_cylinder': 'in_box',
        'beige_1D_ring': 'in_box',
        'blue_1D_ring': 'in_box',
        'black_2D_circle': 'in_box',
        'white_box': 'box'
    }
    
    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'.
    # Step-by-step action sequence to achieve the goal state
    
    # 1. Pick the yellow_3D_cylinder and place it in the white_box
    robot.pick(object0, object4)
    robot.place(object0, object4)
    
    # 2. Pick the beige_1D_ring and place it in the white_box
    robot.pick(object1, object4)
    robot.place(object1, object4)
    
    # 3. Pick the blue_1D_ring and place it in the white_box
    robot.pick(object2, object4)
    robot.place(object2, object4)
    
    # 4. Pick out the black_2D_circle from the white_box (since it is fragile and needs to be placed last)
    robot.pick_out(object3, object4)
    
    # 5. Place the black_2D_circle back into the white_box
    robot.place(object3, object4)
    
    # after making all actions, fill your reasons according to the rules
    # Reasons:
    # 1. It is prohibited to lift and relocate a container (Rule 1) - We did not move the white_box.
    # 2. When fold a object, the object must be foldable (Rule 2) - No folding was required.
    # 3. When place a fragile objects, the soft objects must be in the bin (Rule 3) - The black_2D_circle was placed last after ensuring all other objects were in the bin.
    # 4. When a soft object in the bin at the initial state, out of the soft object and replace it into the bin (Rule 4) - The black_2D_circle was taken out and placed back in.

    # check if the goal state is satisfying goal state table
    assert object0.is_in_box == True
    assert object1.is_in_box == True
    assert object2.is_in_box == True
    assert object3.is_in_box == True
    assert object4.is_in_box == False  # white_box itself is not inside another box

    print("All objects are in the correct final state.")
