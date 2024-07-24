from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic effect predicates for obj
    pushed: bool
    folded: bool
    
    # Predicates for box
    in_bin_objects: list
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_packed: bool
    
    # Object physical properties 
    is_soft: bool
    is_foldable: bool
    is_elastic: bool
    is_fragile: bool
    is_rigid: bool


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
        self.robot_now_holding = None
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Preconditions
        if self.robot_handempty and not obj.in_box:
            # Effects
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and not obj.is_fragile:
            # Effects
            self.state_handempty()
            obj.in_box = True
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        elif self.robot_now_holding == obj and obj.is_fragile:
            # Check if there is a soft object in the bin
            if any(o.is_soft for o in bin.in_bin_objects):
                self.state_handempty()
                obj.in_box = True
                bin.in_bin_objects.append(obj)
                print(f"Place {obj.name} in {bin.name}")
            else:
                print(f"Cannot place fragile {obj.name} without a soft object in the bin")
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if self.robot_handempty and obj.in_box:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if self.robot_handempty and obj.is_foldable:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and obj in bin.in_bin_objects:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures the robot's hand is empty and the object is not already in the bin. The 'place' action checks if the object is fragile and ensures a soft object is in the bin before placing it. The 'push' and 'fold' actions require the robot's hand to be empty, and the object to be in the bin or foldable, respectively. The 'out' action ensures the object is in the bin before removing it. These conditions ensure safe and rule-compliant bin packing

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False, is_soft=True, is_foldable=False, is_elastic=True, is_fragile=False, is_rigid=False)
object1 = Object(index=1, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False, is_soft=True, is_foldable=False, is_elastic=True, is_fragile=False, is_rigid=False)
object2 = Object(index=2, name='blue_linear', color='blue', shape='linear', object_type='obj', pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False, is_soft=False, is_foldable=False, is_elastic=False, is_fragile=True, is_rigid=False)
object3 = Object(index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False, is_soft=True, is_foldable=False, is_elastic=False, is_fragile=False, is_rigid=False)
object4 = Object(index=4, name='white_linear', color='white', shape='linear', object_type='obj', pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False, is_soft=False, is_foldable=True, is_elastic=True, is_fragile=False, is_rigid=False)
object5 = Object(index=5, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj', pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False, is_soft=False, is_foldable=False, is_elastic=False, is_fragile=True, is_rigid=True)
object6 = Object(index=6, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False, is_soft=False, is_foldable=False, is_elastic=False, is_fragile=False, is_rigid=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given table

    # Second, using given rules and object's states, make a task planning strategy
    # Rule 1: It is prohibited to lift and relocate a container
    # Rule 2: Do not place a fragile object if there is no soft object in the bin
    # Rule 3: When a fragile object is in the bin at the initial state, out of the fragile object and replace it into the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object6

    # c) Action sequence
    # Step 1: Out the fragile object (green_3D_cylinder) from the box
    robot.out(object5, box)

    # Step 2: Pick and place the yellow_3D_cuboid into the box
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 3: Pick and place the white_3D_cylinder into the box
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 4: Pick and place the green_3D_cylinder back into the box
    robot.pick(object5, box)
    robot.place(object5, box)

    # Step 5: Ensure the white_2D_circle and white_linear are already in the box
    # No action needed as they are already in the box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason for Step 1: Rule 3 requires us to out the fragile object and replace it into the bin
    # Reason for Step 2: yellow_3D_cuboid is not fragile, so it can be placed directly
    # Reason for Step 3: white_3D_cylinder is not fragile, so it can be placed directly
    # Reason for Step 4: green_3D_cylinder is fragile, but there are now soft objects in the bin (yellow_3D_cuboid and white_3D_cylinder)

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == False
    assert object3.in_box == True
    assert object4.in_box == True
    assert object5.in_box == True
    assert object6.in_box == False
    print("All task planning is done")
