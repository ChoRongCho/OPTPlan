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
    is_heavy: bool
    
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
        # pick an {object} not in the {bin}, it does not include 'place' action
        if self.robot_handempty and not obj.in_box and obj.object_type != 'box':
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and obj.object_type != 'box':
            if obj.is_rigid:
                if all(o.is_soft for o in bin.in_bin_objects):
                    print(f"Place {obj.name} in {bin.name}")
                    bin.in_bin_objects.append(obj)
                    obj.in_box = True
                    self.state_handempty()
                else:
                    print(f"Cannot place {obj.name} in {bin.name} because not all objects in bin are soft")
            else:
                print(f"Place {obj.name} in {bin.name}")
                bin.in_bin_objects.append(obj)
                obj.in_box = True
                self.state_handempty()
        else:
            print(f"Cannot Place {obj.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.is_soft and obj.in_box:
            if not any(o.is_rigid for o in bin.in_bin_objects):
                print(f"Push {obj.name}")
                obj.pushed = True
            else:
                print(f"Cannot push {obj.name} because there is a rigid object in the bin")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # fold an {object}, hand must be empty when folding
        if self.robot_handempty and obj.is_foldable:
            print(f"Fold {obj.name}")
            obj.folded = True
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # pick an {object} in {bin} and place an {object} on platform. After the action, the robot hand is empty
        if obj.in_box and obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_heavy=False,
    is_soft=True, is_foldable=False, is_elastic=True, is_fragile=False, is_rigid=False
)

object1 = Object(
    index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_heavy=False,
    is_soft=False, is_foldable=False, is_elastic=False, is_fragile=False, is_rigid=True
)

object2 = Object(
    index=2, name='green_3D_cylinder', color='green', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_heavy=False,
    is_soft=False, is_foldable=False, is_elastic=False, is_fragile=True, is_rigid=True
)

object3 = Object(
    index=3, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_heavy=False,
    is_soft=False, is_foldable=True, is_elastic=False, is_fragile=False, is_rigid=False
)

white_box = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object3], in_box=True, is_heavy=False,
    is_soft=False, is_foldable=False, is_elastic=False, is_fragile=False, is_rigid=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    # object0: out_box, not in bin
    # object1: out_box, not in bin
    # object2: out_box, not in bin
    # object3: in_box, in white_box
    # white_box: contains object3

    # Goal state
    # object0: in_bin, pushed
    # object1: in_bin
    # object2: in_bin
    # object3: out_box
    # white_box: empty

    # Second, using given rules and object's states, make a task planning strategy
    # 1. Pick and place object0 (soft) in the bin
    # 2. Push object0 to make space
    # 3. Pick and place object1 (rigid) in the bin
    # 4. Pick and place object2 (rigid) in the bin
    # 5. Out object3 from the bin

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box

    # c) Action sequence
    # Step 1: Pick and place object0 (soft) in the bin
    robot.pick(object0, box)
    robot.place(object0, box)

    # Step 2: Push object0 to make space
    robot.push(object0, box)

    # Step 3: Pick and place object1 (rigid) in the bin
    robot.pick(object1, box)
    robot.place(object1, box)

    # Step 4: Pick and place object2 (rigid) in the bin
    robot.pick(object2, box)
    robot.place(object2, box)

    # Step 5: Out object3 from the bin
    robot.out(object3, box)

    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # - object0 is soft and can be pushed to make space.
    # - object1 and object2 are rigid and must be placed after the soft object is in the bin.
    # - object3 is foldable and needs to be out of the bin to satisfy the goal state.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object0.pushed == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == False
    assert white_box.in_bin_objects == [object0, object1, object2]
    print("All task planning is done")
