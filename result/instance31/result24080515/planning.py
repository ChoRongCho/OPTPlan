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
    
    # Object physical properties 
    is_soft: bool
    is_foldable: bool
    is_rigid: bool
    is_elastic: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    out_box: bool


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
        if obj.out_box and self.robot_handempty:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj:
            if obj.is_soft or all(o.is_soft for o in bin.in_bin_objects):
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
            else:
                print(f"Cannot place {obj.name} before placing soft objects")
        else:
            print(f"Cannot place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.in_box:
            print(f"Push {obj.name}")
            obj.pushed = True
        else:
            print(f"Cannot push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and self.robot_handempty:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            self.state_handempty()
        else:
            print(f"Cannot out {obj.name}")

# Reason:
# The robot actions are designed to follow the given rules for a bin_packing task. The preconditions ensure that actions are only performed when the state of the robot and objects meet specific criteria, such as the robot's hand being empty or an object being foldable. The effects update the state of the robot and objects to reflect the changes caused by the actions. This approach ensures that the robot's actions are consistent with the task requirements and constraints, such as placing soft objects before rigid ones and only pushing soft objects. The design also includes checks to prevent invalid actions, enhancing the robustness of the task execution.

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_foldable=False, is_rigid=True, is_elastic=False,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_foldable=False, is_rigid=False, is_elastic=True,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='blue_2D_ring', color='blue', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_foldable=False, is_rigid=False, is_elastic=False,
    in_box=False, out_box=True
)

object3 = Object(
    index=3, name='black_2D_circle', color='black', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_foldable=True, is_rigid=False, is_elastic=False,
    in_box=True, out_box=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_foldable=False, is_rigid=False, is_elastic=False,
    in_box=False, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    objects = [object0, object1, object2, object3, object4]
    box = object4

    # Second, using given rules and object's states, make a task planning strategy
    # The strategy is to place all objects in the box, ensuring soft objects are placed first

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4

    # c) Action sequence
    # Fold the soft and foldable object first
    robot.fold(object3, box)

    # Pick and place the soft object
    robot.pick(object3, box)
    robot.place(object3, box)

    # Pick and place the rigid object
    robot.pick(object0, box)
    robot.place(object0, box)

    # Pick and place the elastic object
    robot.pick(object1, box)
    robot.place(object1, box)

    # Pick and place the remaining object
    robot.pick(object2, box)
    robot.place(object2, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # The actions follow the rules:
    # - Fold the foldable object first
    # - Place the soft object before any rigid or elastic objects
    # - Place the remaining objects

    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object3.folded == True
    assert object4.in_bin_objects == [object3, object0, object1, object2]
    print("All task planning is done")
