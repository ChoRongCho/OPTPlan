from dataclasses import dataclass

@dataclass
class Object:
    # Basic dataclass
    index: int
    name: str
    color: str
    shape: str
    object_type: str  # box or obj
    
    # Basic Effect Robot Action Predicates for object_type = obj
    pushed: bool
    folded: bool
    
    # Bin Predicates for object_type = bin
    in_bin: list
    
    # Object physical properties predicates
    is_elastic: bool
    is_soft: bool
    is_rigid: bool
    
    # bin_packing predicates expressed as a boolean (max 2)
    is_fragile: bool
    is_heavy: bool


class Robot:
    def __init__(self, name: str = "UR5", goal: str = None, actions: dict = None):
        self.name = name
        self.goal = goal
        self.actions = actions
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = True

    def state_handempty(self):
        self.robot_handempty = True
        self.robot_now_holding = None
        self.robot_base_pose = False

    def state_holding(self, obj):
        self.robot_handempty = False
        self.robot_now_holding = obj
        self.robot_base_pose = False

    def state_base(self):
        self.robot_base_pose = True

    def pick(self, obj, bin):
        if self.robot_handempty and obj.object_type == 'obj' and obj not in bin.in_bin:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")

    def place(self, obj, bin):
        if not self.robot_handempty and self.robot_now_holding == obj:
            if obj.is_soft and not obj.pushed:
                print(f"Cannot Place {obj.name} because it is soft and not pushed")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin.append(obj)
                self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")

    def push(self, obj, bin):
        if self.robot_handempty and obj.object_type == 'obj':
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot Push {obj.name}")

    def fold(self, obj, bin):
        if self.robot_handempty and obj.object_type == 'obj':
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")

    def pick_out(self, obj, bin):
        if obj in bin.in_bin:
            print(f"Pick_Out {obj.name} from {bin.name}")
            bin.in_bin.remove(obj)
            self.state_holding(obj)
        else:
            print(f"Cannot Pick_Out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' action ensures the robot can only pick objects not already in the bin and not boxes. The 'place' action checks if the object is soft and pushed before placing it in the bin. The 'push' and 'fold' actions require the robot's hand to be empty. The 'pick_out' action allows the robot to remove objects from the bin and hold them. These conditions ensure the robot's actions are valid and follow the specified rules for bin packing.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_3D_cuboid', color='yellow', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin=[], is_elastic=False, is_soft=True, is_rigid=False, is_fragile=False, is_heavy=False)
object1 = Object(index=1, name='white_1D_ring', color='white', shape='1D_ring', object_type='obj', pushed=False, folded=False, in_bin=[], is_elastic=True, is_soft=False, is_rigid=False, is_fragile=False, is_heavy=False)
object2 = Object(index=2, name='blue_1D_ring', color='blue', shape='1D_ring', object_type='obj', pushed=False, folded=False, in_bin=[], is_elastic=True, is_soft=False, is_rigid=False, is_fragile=False, is_heavy=False)
object3 = Object(index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj', pushed=False, folded=False, in_bin=[], is_elastic=True, is_soft=False, is_rigid=True, is_fragile=False, is_heavy=False)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin=[], is_elastic=False, is_soft=False, is_rigid=False, is_fragile=False, is_heavy=False)

if __name__ == "__main__":
    # First, using goal table, describe the final state of each object
    # Goal state:
    # object0 (yellow_3D_cuboid) -> in white_box
    # object1 (white_1D_ring) -> pushed and in white_box
    # object2 (blue_1D_ring) -> out of box
    # object3 (white_2D_circle) -> in white_box
    # object4 (white_box) -> remains as box

    # Second, make your order, you should be aware of the robot action effects such as 'push' or 'pick_out etc'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the bin (box)
    bin = object4

    # Third, after making all actions, fill your reasons according to the rules
    # Rule 1: Never pick and place a box
    # Rule 3: When placing soft objects, they must be pushed before packed in the bin
    # Rule 4: When a rigid object is in the bin at the initial state, take it out and replace it into the bin

    # Step-by-step action sequence:
    # 1. Pick out the rigid object (white_2D_circle) from the bin
    robot.pick_out(object3, bin)

    # 2. Push the soft object (yellow_3D_cuboid)
    robot.push(object0, bin)

    # 3. Pick and place the soft object (yellow_3D_cuboid) into the bin
    robot.pick(object0, bin)
    robot.place(object0, bin)

    # 4. Push the elastic object (white_1D_ring)
    robot.push(object1, bin)

    # 5. Pick and place the elastic object (white_1D_ring) into the bin
    robot.pick(object1, bin)
    robot.place(object1, bin)

    # 6. Pick and place the rigid object (white_2D_circle) back into the bin
    robot.pick(object3, bin)
    robot.place(object3, bin)

    # Fourth, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0 in bin.in_bin
    assert object1 in bin.in_bin and object1.pushed
    assert object2 not in bin.in_bin
    assert object3 in bin.in_bin
    assert object4.object_type == 'box'
    print("All task planning is done")
