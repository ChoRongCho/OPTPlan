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
    is_elastic: bool
    is_rigid: bool
    is_fragile: bool
    is_foldable: bool


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
        if obj.object_type == "box":
            print(f"Cannot pick {obj.name} because it is a box.")
            return False
        if obj.in_box:
            print(f"Cannot pick {obj.name} because it is already in the bin.")
            return False
        if not self.robot_handempty:
            print(f"Cannot pick {obj.name} because the robot hand is not empty.")
            return False
        
        # Effects
        self.state_holding(obj)
        print(f"Picked {obj.name}")
        return True
        
    def place(self, obj, bin):
        # Preconditions
        if obj.object_type == "box":
            print(f"Cannot place {obj.name} because it is a box.")
            return False
        if not self.robot_now_holding == obj:
            print(f"Cannot place {obj.name} because it is not being held by the robot.")
            return False
        if obj.is_rigid and not any(o.is_elastic for o in bin.in_bin_objects):
            print(f"Cannot place {obj.name} because there is no elastic object in the bin.")
            return False
        if obj.is_elastic and not any(o.color == "blue" for o in bin.in_bin_objects):
            print(f"Cannot place {obj.name} because there is no blue object in the bin.")
            return False
        
        # Effects
        self.state_handempty()
        obj.in_box = True
        bin.in_bin_objects.append(obj)
        print(f"Placed {obj.name} in {bin.name}")
        return True
    
    def push(self, obj, bin): 
        # Preconditions
        if not self.robot_handempty:
            print(f"Cannot push {obj.name} because the robot hand is not empty.")
            return False
        if not obj.in_box:
            print(f"Cannot push {obj.name} because it is not in the bin.")
            return False
        
        # Effects
        obj.pushed = True
        print(f"Pushed {obj.name}")
        return True
    
    def fold(self, obj, bin):
        # Preconditions
        if not self.robot_handempty:
            print(f"Cannot fold {obj.name} because the robot hand is not empty.")
            return False
        if not obj.is_foldable:
            print(f"Cannot fold {obj.name} because it is not foldable.")
            return False
        
        # Effects
        obj.folded = True
        print(f"Folded {obj.name}")
        return True
    
    def out(self, obj, bin):
        # Preconditions
        if not obj.in_box:
            print(f"Cannot take out {obj.name} because it is not in the bin.")
            return False
        
        # Effects
        self.state_holding(obj)
        obj.in_box = False
        bin.in_bin_objects.remove(obj)
        self.state_handempty()
        print(f"Out {obj.name} from {bin.name}")
        return True

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='transparent_3D_cylinder', color='transparent', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_heavy=False, is_elastic=True, is_rigid=False, is_fragile=False, is_foldable=False
)

object1 = Object(
    index=1, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_heavy=False, is_elastic=False, is_rigid=False, is_fragile=True, is_foldable=True
)

object2 = Object(
    index=2, name='blue_linear', color='blue', shape='linear', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=False, is_heavy=False, is_elastic=True, is_rigid=True, is_fragile=False, is_foldable=False
)

object3 = Object(
    index=3, name='yellow_2D_rectangle', color='yellow', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_heavy=False, is_elastic=False, is_rigid=False, is_fragile=False, is_foldable=True
)

object4 = Object(
    index=4, name='green_2D_rectangle', color='green', shape='2D_rectangle', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], in_box=True, is_heavy=False, is_elastic=False, is_rigid=False, is_fragile=True, is_foldable=False
)

object5 = Object(
    index=5, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object3, object4], in_box=True, is_heavy=False, is_elastic=False, is_rigid=False, is_fragile=False, is_foldable=False
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
        object5.name: object5.in_box,
    }
    
    # Goal state
    goal_state = {
        object0.name: True,
        object1.name: False,
        object2.name: True,
        object3.name: True,
        object4.name: True,
        object5.name: False,
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()

    # b) Define the box
    box = object5
    
    # c) Action sequence
    # 1. Take out yellow_2D_rectangle and green_2D_rectangle from the box
    robot.out(object3, box)
    robot.out(object4, box)
    
    # 2. Place blue_linear in the box (since it is blue and elastic)
    robot.pick(object2, box)
    robot.place(object2, box)
    
    # 3. Place transparent_3D_cylinder in the box (since it is elastic and blue_linear is already in the box)
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # 4. Place yellow_2D_rectangle and green_2D_rectangle back in the box
    robot.pick(object3, box)
    robot.place(object3, box)
    
    robot.pick(object4, box)
    robot.place(object4, box)
    
    # 5. Take out the white_box
    robot.out(object5, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # - Rule 1: Never attempt to pick up and set down an object named box.
    # - Rule 2: When placing a rigid object in the bin, an elastic object must be in the bin before.
    # - Rule 3: When placing an elastic object, a blue object must be in the bin before.
    
    # Finally, check if the goal state is satisfying goal state table.
    assert object0.in_box == True
    assert object1.in_box == False
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_box == True
    assert object5.in_box == False
    print("All task planning is done")
