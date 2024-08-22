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
                print(f"Place {obj.name in bin.name}")
                bin.in_bin_objects.append(obj)
                self.state_handempty()
                obj.in_box = True
                obj.out_box = False
            else:
                print(f"Cannot place {obj.name} before soft objects")
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
            print(f"Cannot out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=True, is_foldable=False, is_elastic=True,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='blue_2D_ring', color='blue', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_foldable=False, is_elastic=False,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_foldable=False, is_elastic=True,
    in_box=False, out_box=True
)

object3 = Object(
    index=3, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_foldable=True, is_elastic=False,
    in_box=True, out_box=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[], is_soft=False, is_foldable=False, is_elastic=False,
    in_box=False, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_box,
        white_box.name: white_box.in_bin_objects
    }
    
    # Goal state
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        object3.name: True,
        white_box.name: [object0, object1, object2, object3]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = white_box
    
    # c) Action sequence
    # Pick and place the soft object first
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Push the soft object
    robot.push(object0, box)
    
    # Pick and place the foldable object
    robot.pick(object3, box)
    robot.fold(object3, box)
    robot.place(object3, box)
    
    # Pick and place the remaining objects
    robot.pick(object1, box)
    robot.place(object1, box)
    
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # - Pick and place the soft object first to satisfy the rule that soft objects should be placed before rigid objects.
    # - Push the soft object to ensure it is properly placed in the bin.
    # - Fold the foldable object before placing it in the bin.
    # - Place the remaining objects in the bin.
    
    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert white_box.in_bin_objects == [object0, object1, object2, object3]
    
    print("All task planning is done")
