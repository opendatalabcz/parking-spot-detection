"""
Class representing basic 2D rectangle
"""


class Rect(object):

    @classmethod
    def from_array(cls, arr):
        assert len(arr) == 4
        return Rect(arr[0], arr[1], arr[2], arr[3])

    def to_array(self):
        return self.coords

    def to_native_array(self):
        return [int(coord) for coord in self.coords]

    def __init__(self, left, top, right, bottom):
        self.coords = [left, top, right, bottom]
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def width(self):
        return self.right - self.left

    def height(self):
        return self.bottom - self.top

    def area(self) -> int:
        return (self.bottom - self.top) * (self.right - self.left)

    def center(self):
        return self.left + self.width() / 2, self.top + self.height() / 2

    def iou(self, other) -> float:
        if not self.intersect(other):
            return 0.0

        if self.is_inside(other) or other.is_inside(self):
            return 1

        points = [
            max(self.left, other.left),
            max(self.top, other.top),
            min(self.right, other.right),
            min(self.bottom, other.bottom)
        ]
        inter_rect_area = Rect.from_array(points).area()
        assert inter_rect_area >= 0
        return inter_rect_area / (self.area() + other.area() - inter_rect_area)

    def is_inside(self, other):
        return self.left > other.left and self.top > other.top and self.right < other.right and self.bottom < other.bottom

    def intersect(self, other):
        this_center_x, this_center_y = self.center()
        other_center_x, other_center_y = other.center()
        return (abs(this_center_x - other_center_x) < (abs(self.width() + other.width()) / 2)) \
               and (abs(this_center_y - other_center_y) < (abs(self.height() + other.height()) / 2))
