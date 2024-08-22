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
    is_rigid: bool
    is_elastic: bool
    is_soft: bool
    
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
        self.robot_now_holding = False
        self.robot_base_pose = True
    
    # basic state
    def state_handempty(self):
        self.robot_handempty = True
        self.robot_base_pose = False
    
    # basic state
    def state_holding(self, objects):
        self.robot_handempty = False
        self.robot_now_holding = objects
        self.robot_base_pose = False
    
    # basic state
    def state_base(self):
        self.robot_base_pose = True
    
    def pick(self, obj, bin):
        # Preconditions
        if obj.out_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.out_box = False
            obj.in_box = False
            print(f"Pick {obj.name}")
        else:
            print(f"Cannot Pick {obj.name}")
        
    def place(self, obj, bin):
        # Preconditions
        if self.robot_now_holding == obj and obj.out_box:
            # Effects
            self.state_handempty()
            obj.in_box = True
            obj.out_box = False
            bin.in_bin_objects.append(obj)
            print(f"Place {obj.name} in {bin.name}")
        else:
            print(f"Cannot Place {obj.name} in {bin.name}")
    
    def push(self, obj, bin): 
        # Preconditions
        if obj.in_box and self.robot_handempty and obj.is_soft:
            # Effects
            obj.pushed = True
            print(f"Push {obj.name}")
        else:
            print(f"Cannot Push {obj.name}")
    
    def fold(self, obj, bin):
        # Preconditions
        if obj.is_elastic and self.robot_handempty:
            # Effects
            obj.folded = True
            print(f"Fold {obj.name}")
        else:
            print(f"Cannot Fold {obj.name}")
    
    def out(self, obj, bin):
        # Preconditions
        if obj.in_box and self.robot_handempty:
            # Effects
            self.state_holding(obj)
            obj.in_box = False
            obj.out_box = True
            bin.in_bin_objects.remove(obj)
            self.state_handempty()
            print(f"Out {obj.name} from {bin.name}")
        else:
            print(f"Cannot Out {obj.name} from {bin.name}")

    def dummy(self):
        pass


 # Object Initial State
object0 = Object(
    index=0, name='red_3D_polyhedron', color='red', shape='3D_polyhedron', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=False, is_soft=True,
    in_box=False, out_box=True
)

object1 = Object(
    index=1, name='yellow_3D_cylinder', color='yellow', shape='3D_cylinder', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=False, is_soft=False,
    in_box=False, out_box=True
)

object2 = Object(
    index=2, name='black_2D_ring', color='black', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=True, is_elastic=False, is_soft=False,
    in_box=True, out_box=False
)

object3 = Object(
    index=3, name='white_2D_ring', color='white', shape='2D_ring', object_type='obj',
    pushed=False, folded=False, in_bin_objects=[], is_rigid=False, is_elastic=True, is_soft=False,
    in_box=True, out_box=False
)

object4 = Object(
    index=4, name='white_box', color='white', shape='box', object_type='box',
    pushed=False, folded=False, in_bin_objects=[object2, object3], is_rigid=False, is_elastic=False, is_soft=False,
    in_box=True, out_box=False
)

if __name__ == "__main__":
    # First, using goal table, describe the initial state and final state of each object
    # Initial state
    initial_state = {
        object0.name: object0.in_box,
        object1.name: object1.in_box,
        object2.name: object2.in_box,
        object3.name: object3.in_box,
        object4.name: object4.in_bin_objects
    }
    
    # Goal state
    goal_state = {
        object0.name: True,
        object1.name: True,
        object2.name: True,
        object3.name: True,
        object4.name: [object0, object1, object2, object3]
    }
    
    # Second, using given rules and object's states, make a task planning strategy
    # Strategy:
    # 1. Pick and place the soft object (object0) first.
    # 2. Pick and place the rigid object (object1).
    # 3. Ensure the objects already in the box (object2 and object3) are correctly placed.
    # 4. Push the soft object if necessary.
    # 5. Fold the elastic object if necessary.
    
    # Third, make an action sequence. You should be aware of the robot action effects such as 'push' or 'out'. 
    # a) Initialize the robot
    robot = Robot()
    
    # b) Define the box
    box = object4
    
    # Action sequence
    # 1. Pick and place the soft object (object0)
    robot.pick(object0, box)
    robot.place(object0, box)
    
    # 2. Pick and place the rigid object (object1)
    robot.pick(object1, box)
    robot.place(object1, box)
    
    # 3. Ensure the objects already in the box (object2 and object3) are correctly placed
    # No action needed as they are already in the box
    
    # 4. Push the soft object if necessary
    robot.push(object0, box)
    
    # 5. Fold the elastic object if necessary
    robot.fold(object3, box)
    
    # Fourth, after making all actions, fill your reasons according to the rules
    # Reasons:
    # - Placed the soft object first to satisfy the rule: "Before place a fragile or rigid object, soft object should be in the box if there is any soft objects."
    # - Placed the rigid object next.
    # - Pushed the soft object after placing it in the bin.
    # - Folded the elastic object as it is foldable.
    
    # Finally, check if the goal state is satisfying goal state table. Use a template below. These are examples.
    assert object0.in_box == True
    assert object1.in_box == True
    assert object2.in_box == True
    assert object3.in_box == True
    assert object4.in_bin_objects == [object0, object1, object2, object3]
    
    print("All task planning is done")
