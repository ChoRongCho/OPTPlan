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
    is_foldable: bool
    is_elastic: bool
    
    # Preconditions and effects for bin_packing task planning (max: 2)
    in_box: bool
    is_packed: bool


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
        if self.robot_handempty and not obj.in_box:
            print(f"Pick {obj.name}")
            self.state_holding(obj)
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # place an {object} on the {bin or not bin}
        if self.robot_now_holding == obj and not obj.in_box:
            print(f"Place {obj.name} in {bin.name}")
            bin.in_bin_objects.append(obj)
            obj.in_box = True
            self.state_handempty()
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # push an {object} downward in the bin, hand must be empty when pushing
        if self.robot_handempty and obj.in_box and obj.is_elastic:
            print(f"Push {obj.name}")
            obj.pushed = True
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
        if obj in bin.in_bin_objects:
            print(f"Out {obj.name} from {bin.name}")
            bin.in_bin_objects.remove(obj)
            obj.in_box = False
            self.state_holding(obj)
            self.state_handempty()
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, 
    name='yellow_2D_rectangle', 
    color='yellow', 
    shape='2D_rectangle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=True, 
    is_elastic=False, 
    in_box=False, 
    is_packed=False
)

object1 = Object(
    index=1, 
    name='white_2D_ring', 
    color='white', 
    shape='2D_ring', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_elastic=True, 
    in_box=False, 
    is_packed=False
)

object2 = Object(
    index=2, 
    name='transparent_2D_circle', 
    color='transparent', 
    shape='2D_circle', 
    object_type='obj', 
    pushed=False, 
    folded=False, 
    in_bin_objects=[], 
    is_foldable=False, 
    is_elastic=True, 
    in_box=False, 
    is_packed=False
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
    is_foldable=False, 
    is_elastic=False, 
    in_box=True, 
    is_packed=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    initial_state = {
        object0.name: object0,
        object1.name: object1,
        object2.name: object2,
        object3.name: object3
    }
    
    # Final State
    goal_state = {
        object0.name: {'in_box': True, 'folded': True, 'is_packed': True},
        object1.name: {'in_box': True, 'is_packed': True},
        object2.name: {'in_box': True, 'is_packed': True},
        object3.name: {'in_bin_objects': [object0, object1, object2], 'is_packed': True}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Fold the yellow_2D_rectangle since it is foldable.
    # 2. Place the yellow_2D_rectangle in the box.
    # 3. Place the white_2D_ring in the box.
    # 4. Push the white_2D_ring since it is elastic.
    # 5. Place the transparent_2D_circle in the box.
    # 6. Push the transparent_2D_circle since it is elastic.
    # 7. Mark all objects as packed.

    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object3
    
    # c) Perform the actions
    # Fold the yellow_2D_rectangle
    robot.fold(object0, box)
    
    # Place the yellow_2D_rectangle in the box
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Place the white_2D_ring in the box
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Push the white_2D_ring
    robot.push(object1, box)
    
    # Place the transparent_2D_circle in the box
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Push the transparent_2D_circle
    robot.push(object2, box)
    
    # Mark all objects as packed
    object0.is_packed = True
    object1.is_packed = True
    object2.is_packed = True
    object3.is_packed = True
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # - Folded the yellow_2D_rectangle because it is foldable.
    # - Placed the yellow_2D_rectangle first because it is not elastic.
    # - Placed and pushed the white_2D_ring because it is elastic.
    # - Placed and pushed the transparent_2D_circle because it is elastic.
    # - Marked all objects as packed to satisfy the goal state.

    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object0.folded == True
    assert object0.is_packed == True
    
    assert object1.in_box == True
    assert object1.is_packed == True
    
    assert object2.in_box == True
    assert object2.is_packed == True
    
    assert object3.in_bin_objects == [object0, object1, object2]
    assert object3.is_packed == True
    
    print("All task planning is done")
