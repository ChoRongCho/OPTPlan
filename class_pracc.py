import re


def main():
    strings = """
Answer
Object Name: white_3D_cylinder object

Descriptions about object
The object in the images is a white, three-dimensional (3D) cylinder. From the side view, it has a conical shape that widens from a narrow base to a broader top, resembling a truncated cone. The side view highlights the object's vertical dimension, with a slightly flared upper edge and a smooth surface that appears to be uniform in texture.

From the top view, the object is circular, confirming its cylindrical shape. The top view shows the open mouth of the cylinder, which is wide and round, with a consistent circular shape. The interior appears to be hollow, and the walls seem to be of moderate thickness, maintaining the object's structural integrity.

The color of the object is white, which is consistent in both images. The white color suggests that the object might be made of a material like plastic, paper, or ceramic, commonly used for containers or cups. The surface appears to be smooth and clean, without any noticeable patterns or designs.

In summary, the object is a white 3D cylinder with a conical profile when viewed from the side and a circular shape when viewed from the top. Its uniform color and smooth texture make it a simple yet functional object, possibly used for holding or containing small items.
"""
    name_match = re.search(r"Object Name: ([\w\d_]+) object", strings)
    if not name_match:
        raise ValueError("Object name not found in the input string.")
    object_name = name_match.group(1)
    print(object_name)
    abc = object_name.split("_")
    print(abc)


if __name__ == '__main__':
    main()
