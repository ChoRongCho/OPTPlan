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
        # Preconditions
        if obj.object_type == 'box':
            print(f"Cannot pick {obj.name} because it is a box.")
            return
        if obj.in_box:
            print(f"Cannot pick {obj.name} because it is already in the bin.")
            return
        if not self.robot_handempty:
            print(f"Cannot pick {obj.name} because the robot hand is not empty.")
            return
        
        # Effects
        self.state_holding(obj)
        print(f"Picked {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if obj.object_type == 'box':
            print(f"Cannot place {obj.name} because it is a box.")
            return
        if not self.robot_now_holding == obj:
            print(f"Cannot place {obj.name} because it is not being held by the robot.")
            return
        if obj.is_rigid and not obj.in_box:
            print(f"Cannot place {obj.name} because it is rigid and not in the bin.")
            return
        
        # Effects
        obj.in_box = True
        obj.is_packed = True
        self.state_handempty()
        bin.in_bin_objects.append(obj)
        print(f"Placed {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if not obj.is_soft:
            print(f"Cannot push {obj.name} because it is not soft.")
            return
        if not self.robot_handempty:
            print(f"Cannot push {obj.name} because the robot hand is not empty.")
            return
        
        # Effects
        obj.pushed = True
        print(f"Pushed {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if not obj.is_elastic:
            print(f"Cannot fold {obj.name} because it is not foldable.")
            return
        if not self.robot_handempty:
            print(f"Cannot fold {obj.name} because the robot hand is not empty.")
            return
        
        # Effects
        obj.folded = True
        print(f"Folded {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj not in bin.in_bin_objects:
            print(f"Cannot remove {obj.name} because it is not in the bin.")
            return
        if not self.robot_handempty:
            print(f"Cannot remove {obj.name} because the robot hand is not empty.")
            return
        
        # Effects
        bin.in_bin_objects.remove(obj)
        obj.in_box = False
        self.state_handempty()
        print(f"Removed {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='white_3D_cylinder', color='white', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=True, is_rigid=False, is_soft=True
)

object1 = Object(
    index=1, name='black_3D_cylinder', color='black', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_packed=False,
    is_elastic=False, is_rigid=True, is_soft=False
)

object2 = Object(
    index=2, name='white_2D_circle', color='white', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False,
    is_elastic=True, is_rigid=True, is_soft=False
)

object3 = Object(
    index=3, name='blue_2D_circle', color='blue', shape='2D_circle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False,
    is_elastic=True, is_rigid=True, is_soft=False
)

object4 = Object(
    index=4, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_packed=False,
    is_elastic=True, is_rigid=False, is_soft=False
)

white_box = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2, object3, object4], in_box=False, is_packed=False,
    is_elastic=False, is_rigid=False, is_soft=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_box,
        object4.name: object4.in_box,
        white_box.name: white_box.in_bin_objects
    }
    
    # Goal state
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        object3.name: True,
        object4.name: True,
        white_box.name: [object0, object1, object2, object3, object4]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = white_box
    
    # c) Make an action sequence
    # Step 1: Push the soft object to make space
    robot.push(object0, box)
    
    # Step 2: Pick and place the white_3D_cylinder
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # Step 3: Pick and place the black_3D_cylinder
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasoning:
    # 1. Pushed the white_3D_cylinder because it is soft and to make space in the bin.
    # 2. Picked and placed the white_3D_cylinder because it is soft and elastic.
    # 3. Picked and placed the black_3D_cylinder because it is rigid and the 3D object (white_3D_cylinder) is already in the bin.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples. 
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert white_box.in_bin_objects == [object2, object3, object4, object0, object1]
    print("All task planning is done")
