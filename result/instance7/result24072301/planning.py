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
    is_elastic: bool
    is_soft: bool
    is_foldable: bool
    in_box: bool


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
        self.robot_now_holding = None
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
            print(f"Cannot place {obj.name} because the robot is not holding it.")
            return
        
        # Effects
        obj.in_box = True
        bin.in_bin_objects.append(obj)
        self.state_handempty()
        print(f"Placed {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if not obj.is_soft:
            print(f"Cannot push {obj.name} because it is not soft.")
            return
        if not obj.in_box:
            print(f"Cannot push {obj.name} because it is not in the bin.")
            return
        if not self.robot_handempty:
            print(f"Cannot push {obj.name} because the robot hand is not empty.")
            return
        
        # Effects
        obj.pushed = True
        print(f"Pushed {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if not obj.is_foldable:
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
        if not obj.in_box:
            print(f"Cannot out {obj.name} because it is not in the bin.")
            return
        if obj.is_soft:
            print(f"Cannot out {obj.name} because it is soft.")
            return
        
        # Effects
        obj.in_box = False
        bin.in_bin_objects.remove(obj)
        self.state_holding(obj)
        print(f"Out {obj.name} from {bin.name}")

# Reason:
# The robot actions are designed to follow the given rules strictly. The 'pick' and 'place' actions ensure that boxes are never picked or placed, adhering to rule 1. The 'fold' action is prioritized for foldable objects as per rule 2. The 'out' action handles rigid objects in the bin initially, complying with rule 3. The 'push' action is specifically for soft objects in the bin, following rule 4. These actions ensure that the robot's behavior aligns with the specified constraints and task requirements for bin packing

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(index=0, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_foldable=True, in_box=False)
object1 = Object(index=1, name='brown_3D_cuboid', color='brown', shape='3D_cuboid', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=True, is_soft=True, is_foldable=False, in_box=False)
object2 = Object(index=2, name='blue_2D_ring', color='blue', shape='2D_ring', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_foldable=False, in_box=False)
object3 = Object(index=3, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=True, is_foldable=False, in_box=True)
object4 = Object(index=4, name='white_box', color='white', shape='box', object_type='box', pushed=False, folded=False, in_bin_objects=[], is_elastic=False, is_soft=False, is_foldable=False, in_box=False)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial State
    initial_state = {
        "yellow_2D_rectangle": {"in_box": False, "folded": False},
        "brown_3D_cuboid": {"in_box": False, "pushed": False},
        "blue_2D_ring": {"in_box": False},
        "red_3D_polyhedron": {"in_box": True, "pushed": False},
        "white_box": {"in_bin_objects": []}
    }
    
    # Goal State
    goal_state = {
        "yellow_2D_rectangle": {"in_box": False, "folded": True},
        "brown_3D_cuboid": {"in_box": True, "pushed": True},
        "blue_2D_ring": {"in_box": True},
        "red_3D_polyhedron": {"in_box": True, "pushed": True},
        "white_box": {"in_bin_objects": [1, 2, 3]}
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object4
    
    # c) Action sequence
    # Rule 2: Fold the foldable object first
    robot.fold(object0, box)
    
    # Rule 4: Push the soft object in the bin
    robot.push(object3, box)
    
    # Rule 3: Out the rigid object and replace it into the bin
    robot.out(object3, box)
    robot.place(object3, box)
    robot.push(object3, box)
    
    # Pick and place the remaining objects
    robot.pick(object1, box)
    robot.place(object1, box)
    robot.push(object1, box)
    
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reason:
    # 1. Folded the yellow_2D_rectangle because it is foldable.
    # 2. Pushed the red_3D_polyhedron because it is soft and initially in the bin.
    # 3. Outed and replaced the red_3D_polyhedron because it was initially in the bin.
    # 4. Pushed the brown_3D_cuboid because it is soft.
    # 5. Placed the blue_2D_ring in the bin as it is not foldable or soft.
    
    # Finally, check if the goal state is satisfying goal state table.
    assert object0.folded == True
    assert object1.in_box == True
    assert object1.pushed == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object3.pushed == True
    assert object4.in_bin_objects == [object1, object2, object3]
    
    print("All task planning is done")
