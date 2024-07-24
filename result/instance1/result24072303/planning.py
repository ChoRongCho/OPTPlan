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
    is_fragile: bool
    
    # Object physical properties 
    is_elastic: bool
    is_rigid: bool
    is_soft: bool


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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if obj.object_type != 'box' and not obj.in_box and self.robot_handempty:
            self.state_holding(obj)
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.is_rigid and not any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot place {obj.name} in {bin.name} because no soft object in bin")
                return
            if obj.is_fragile and not any(o.is_elastic for o in bin.in_bin_objects):
                print(f"Cannot place {obj.name} in {bin.name} because no elastic object in bin")
                return
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.in_box:
            if any(o.is_fragile for o in bin.in_bin_objects if o != obj):
                print(f"Cannot push {obj.name} because a fragile object is on it")
                return
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.in_box:
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj in bin.in_bin_objects:
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules for bin packing. The 'pick' action ensures that the robot does not attempt to pick up a box and only picks objects not already in the bin. The 'place' action checks for the presence of soft objects before placing rigid ones and elastic objects before placing fragile ones, adhering to the rules. The 'push' action ensures that soft objects are pushed only if no fragile objects are on them, and the 'fold' action allows folding of objects in the bin. The 'out' action removes objects from the bin and places them on a platform, ensuring the robot's hand is empty afterward. These actions ensure safe and efficient bin packing while respecting the constraints provided

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_3D_cuboid', 
    color='yellow', 
    shape='3D_cuboid', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_fragile=False, 
    is_elastic=True, 
    is_rigid=False, 
    is_soft=True
)

object1 = Object(
    index=1, 
    name='black_3D_cylinder', 
    color='black', 
    shape='3D_cylinder', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_fragile=False, 
    is_elastic=False, 
    is_rigid=True, 
    is_soft=False
)

object2 = Object(
    index=2, 
    name='blue_2D_ring', 
    color='blue', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=False, 
    is_fragile=False, 
    is_elastic=False, 
    is_rigid=False, 
    is_soft=False
)

object3 = Object(
    index=3, 
    name='white_box', 
    color='white', 
    shape='box', 
    object_type='box', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    in_box=True, 
    is_fragile=False, 
    is_elastic=False, 
    is_rigid=False, 
    is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State:
    # object0 (yellow_3D_cuboid): out_box, is_soft, is_elastic
    # object1 (black_3D_cylinder): out_box, is_rigid
    # object2 (blue_2D_ring): out_box
    # object3 (white_box): in_box

    # Goal State:
    # object0 (yellow_3D_cuboid): in_bin, pushed
    # object1 (black_3D_cylinder): in_bin
    # object2 (blue_2D_ring): in_bin
    # object3 (white_box): in_box

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place the yellow_3D_cuboid (soft and elastic) into the box
    # 2. Push the yellow_3D_cuboid to make more space
    # 3. Pick and place the black_3D_cylinder (rigid) into the box
    # 4. Pick and place the blue_2D_ring into the box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # Action sequence
    robot.pick(object0, box)  # Pick yellow_3D_cuboid
    robot.place(object0, box)  # Place yellow_3D_cuboid in white_box
    robot.push(object0, box)  # Push yellow_3D_cuboid to make more space

    robot.pick(object1, box)  # Pick black_3D_cylinder
    robot.place(object1, box)  # Place black_3D_cylinder in white_box

    robot.pick(object2, box)  # Pick blue_2D_ring
    robot.place(object2, box)  # Place blue_2D_ring in white_box

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. The yellow_3D_cuboid is soft and elastic, so it can be placed first and pushed to make more space.
    # 2. The black_3D_cylinder is rigid, and it is placed after the soft object (yellow_3D_cuboid) is already in the bin.
    # 3. The blue_2D_ring is neither fragile nor rigid, so it can be placed without any specific constraints.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object0.pushed == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True  # The box itself is always in_box

    print("All task planning is done")
