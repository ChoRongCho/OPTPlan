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
    is_in_bin: bool
    is_out_box: bool
    
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
        if obj.object_type != 'box' and not obj.is_in_bin and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.is_out_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if obj.object_type != 'box' and self.robot_now_holding == obj:
            if obj.is_rigid and not any(o.is_soft for o in bin.in_bin_objects):
                print(f"Cannot place {obj.name} in {bin.name} because no soft objects in bin")
                return
            if obj.is_soft and any(o.is_elastic for o in bin.in_bin_objects):
                print(f"Cannot place {obj.name} in {bin.name} because no elastic objects in bin")
                return
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.is_in_bin = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.is_in_bin:
            if any(o.is_elastic for o in bin.in_bin_objects):
                print(f"Cannot push {obj.name} because there is a fragile object on it")
                return
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_in_bin:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.is_in_bin and self.robot_handempty:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.is_in_bin = False
            obj.is_out_box = True
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

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
    is_in_bin=False, 
    is_out_box=True, 
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
    is_in_bin=False, 
    is_out_box=True, 
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
    is_in_bin=False, 
    is_out_box=True, 
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
    is_in_bin=True, 
    is_out_box=False, 
    is_elastic=False, 
    is_rigid=False, 
    is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state is already described in the given code

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick yellow_3D_cuboid and place it in the white_box
    # 2. Push yellow_3D_cuboid to make more space
    # 3. Pick black_3D_cylinder and place it in the white_box
    # 4. Pick blue_2D_ring and place it in the white_box

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object3

    # c) Perform the actions
    robot.pick(object0, box)  # Pick yellow_3D_cuboid
    robot.place(object0, box)  # Place yellow_3D_cuboid in white_box
    robot.push(object0, box)  # Push yellow_3D_cuboid to make more space

    robot.pick(object1, box)  # Pick black_3D_cylinder
    robot.place(object1, box)  # Place black_3D_cylinder in white_box

    robot.pick(object2, box)  # Pick blue_2D_ring
    robot.place(object2, box)  # Place blue_2D_ring in white_box

    # Fourth, after making all actions, fill your reasons according to the rules
    # 1. yellow_3D_cuboid is soft and elastic, so it can be placed first and pushed to make more space.
    # 2. black_3D_cylinder is rigid, so it must be placed after a soft object is in the bin.
    # 3. blue_2D_ring is neither soft nor rigid, so it can be placed last.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.is_in_bin == True
    assert object0.pushed == True
    assert object1.is_in_bin == True
    assert object2.is_in_bin == True
    assert object3.in_bin_objects == [object0, object1, object2]
    print("All task planning is done")