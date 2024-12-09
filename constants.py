import pygame
import math
# constants.py
Width = 1280
Height = 720
GRAVITY = 500
# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
class Helpers:
    @staticmethod
    def calculate_angle_and_speed(pos1, pos2):
        v1 = pygame.math.Vector2(pos1)
        v2 = pygame.math.Vector2(pos2)
        direction_vector = v1 - v2

        angle = direction_vector.angle_to(pygame.math.Vector2(1, 0))
        speed = direction_vector.length()
        return angle, speed

    @staticmethod
    def calculate_point_at_angle(start_pos, angle, distance):
        return pygame.math.Vector2(distance, 0).rotate(angle) + pygame.math.Vector2(start_pos)

    @staticmethod
    def compute_bezier_points(vertices, num_points=30):
        if len(vertices) != 4:
            return None

        result = []

        b0 = vertices[0]
        b1 = vertices[1]
        b2 = vertices[2]
        b3 = vertices[3]

        # Compute polynomial coefficients from Bezier points
        ax = -b0.x + 3 * b1.x + -3 * b2.x + b3.x
        ay = -b0.y + 3 * b1.y + -3 * b2.y + b3.y

        bx = 3 * b0.x + -6 * b1.x + 3 * b2.x
        by = 3 * b0.y + -6 * b1.y + 3 * b2.y

        cx = -3 * b0.x + 3 * b1.x
        cy = -3 * b0.y + 3 * b1.y

        dx = b0.x
        dy = b0.y

        # Set up the number of steps and step size
        num_steps = num_points - 1  # arbitrary choice
        h = 1.0 / num_steps  # compute our step size

        # Compute forward differences from Bezier points and "h"
        point_x = dx
        point_y = dy

        first_fd_x = ax * (h * h * h) + bx * (h * h) + cx * h
        first_fd_y = ay * (h * h * h) + by * (h * h) + cy * h

        second_fd_x = 6 * ax * (h * h * h) + 2 * bx * (h * h)
        second_fd_y = 6 * ay * (h * h * h) + 2 * by * (h * h)

        third_fd_x = 6 * ax * (h * h * h)
        third_fd_y = 6 * ay * (h * h * h)

        # Compute points at each step
        result.append((int(point_x), int(point_y)))

        for i in range(num_steps):
            point_x += first_fd_x
            point_y += first_fd_y

            first_fd_x += second_fd_x
            first_fd_y += second_fd_y

            second_fd_x += third_fd_x
            second_fd_y += third_fd_y

            result.append((int(point_x), int(point_y)))

        return result

    @staticmethod
    def draw_arc_between_points(screen, start_pos, end_pos, aim_point, color, thickness=2):
        # Use Vector2 for positions
        start = pygame.Vector2(start_pos)
        end = pygame.Vector2(end_pos)
        aim = pygame.Vector2(aim_point)

        # Create control points for the arc (using a midpoint to add curvature)
        control_point_1 = start + (end - start) * 0.3
        control_point_2 = end + (aim - end) * 0.3

        control_points = [start, control_point_1, control_point_2, aim]

        # Compute bezier points
        bezier_points = Helpers.compute_bezier_points(control_points, 50)

        # Draw the arc (Bezier curve)
        if bezier_points:
            #pygame.draw.lines(screen, color, False, bezier_points, thickness)
            Helpers.draw_dashed_lines(screen, color, bezier_points, 4)

    @staticmethod
    def draw_dashed_line(surf, color, p1, p2, prev_line_len, dash_length=8):
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        if dx == 0 and dy == 0:
            return
        dist = math.hypot(dx, dy)
        dx /= dist
        dy /= dist

        step = dash_length * 2
        start = (int(prev_line_len) // step) * step
        end = (int(prev_line_len + dist) // step + 1) * step
        for i in range(start, end, dash_length * 2):
            s = max(0, start - prev_line_len)
            e = min(start - prev_line_len + dash_length, dist)
            if s < e:
                ps = p1[0] + dx * s, p1[1] + dy * s
                pe = p1[0] + dx * e, p1[1] + dy * e
                #pygame.draw.aaline(surf, color, pe, ps, 3)
                pygame.draw.circle(surf, color, (int(pe[0]), int(pe[1])), 2)

    @staticmethod
    def draw_dashed_lines(surf, color, points, dash_length=8):
        line_len = 0
        for i in range(1, len(points)):
            p1, p2 = points[i - 1], points[i]
            dist = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            Helpers.draw_dashed_line(surf, color, p1, p2, line_len, dash_length)
            line_len += dist

    @staticmethod
    def map_range(value: float, from_min, from_max, to_min, to_max):
        # Calculate the proportion of the value within the original range
        proportion = (value - from_min) / (from_max - from_min)
        # Map the proportion to the new range
        mapped_value = to_min + (proportion * (to_max - to_min))
        return mapped_value

    @staticmethod
    def calculate_orbital_velocity(self, other):
        G = 6.6743
        r = self.position.distance_to(other.position)
        velocity_magnitude = math.sqrt(G * other.mass / r) * 8.5
        direction = pygame.Vector2(-(other.position.y - self.position.y), other.position.x - self.position.x)
        direction.normalize_ip()
        return direction * velocity_magnitude