import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random
import time
import threading


class SmartTrafficLight:
    def __init__(self, lanes):
        self.lanes = lanes
        self.green_light_time = 10
        self.current_lane = None
        self.light_colors = {lane: 'red' for lane in lanes}

    def detect_traffic(self):
        left_right_traffic = sum([self.lanes["left"], self.lanes["right"]])
        top_bottom_traffic = sum([self.lanes["top"], self.lanes["bottom"]])

        if left_right_traffic > top_bottom_traffic:
            return "left_right"
        else:
            return "top_bottom"

    def update_lights(self):
        while True:
            side_to_give_green = self.detect_traffic()

            self.light_colors = {lane: 'red' for lane in self.lanes}

            if side_to_give_green == "left_right":
                self.light_colors["left"] = 'green'
                self.light_colors["right"] = 'green'
            else:
                self.light_colors["top"] = 'green'
                self.light_colors["bottom"] = 'green'

            print(f"\n--- Green light is now on for: {side_to_give_green} lanes ---")
            self.green_light(side_to_give_green)

            cars_leaving = random.randint(1, 5)
            if side_to_give_green == "left_right":
                self.lanes["left"] = max(0, self.lanes["left"] - cars_leaving)
                self.lanes["right"] = max(0, self.lanes["right"] - cars_leaving)
                print(f"{cars_leaving} cars left from left and right lanes.")
            else:
                self.lanes["top"] = max(0, self.lanes["top"] - cars_leaving)
                self.lanes["bottom"] = max(0, self.lanes["bottom"] - cars_leaving)
                print(f"{cars_leaving} cars left from top and bottom lanes.")

            for lane in self.lanes:
                if lane != "left" and lane != "right" and lane != "top" and lane != "bottom":
                    continue
                new_cars = random.randint(0, 3)
                self.lanes[lane] += new_cars
                if new_cars > 0:
                    print(f"{new_cars} cars arrived in {lane} lane.")

            time.sleep(2)

    def green_light(self, side):
        start_time = time.time()
        print(f"Green light is ON for the {side} side.")
        while time.time() - start_time < self.green_light_time:
            if sum([self.lanes["left"], self.lanes["right"]]) < 5 or sum([self.lanes["top"], self.lanes["bottom"]]) < 5:
                print(f"Traffic cleared, switching light.")
                break
            time.sleep(1)
        print(f"Switching light for {side}.")


lanes = {
    "left": random.randint(0, 10),
    "right": random.randint(0, 10),
    "top": random.randint(0, 10),
    "bottom": random.randint(0, 10)
}

traffic_light = SmartTrafficLight(lanes)

thread = threading.Thread(target=traffic_light.update_lights)
thread.daemon = True
thread.start()

fig, ax = plt.subplots()
lanes_pos = {"left": (-2, 0), "right": (2, 0), "top": (0, 2), "bottom": (0, -2)}
car_positions = {
    "left": [[-2, 0.3], [-2, -0.3]],
    "right": [[2, 0.3], [2, -0.3]],
    "top": [[0.3, 2], [-0.3, 2]],
    "bottom": [[0.3, -2], [-0.3, -2]]
}
ax.plot([-2.5, 2.5], [0.25, 0.25], color='gray', linewidth=20)
ax.plot([-2.5, 2.5], [-0.25, -0.25], color='gray', linewidth=20)
ax.plot([0.5, 0.5], [-2.5, 2.5], color='gray', linewidth=20)
ax.plot([-0.5, -0.5], [-2.5, 2.5], color='gray', linewidth=20)

ax.plot([-2.5, 2.5], [0, 0], color='white', linewidth=2, linestyle='--')
ax.plot([0, 0], [-2.5, 2.5], color='white', linewidth=2, linestyle='--')

rectangles = {}
for lane, pos in lanes_pos.items():
    if lane == "left":
        rect = plt.Rectangle((pos[0] + 0.5, pos[1] + 0.4), 0.15, 0.3, color=traffic_light.light_colors[lane])
    elif lane == "right":
        rect = plt.Rectangle((pos[0] - 0.65, pos[1] - 0.7), 0.15, 0.3, color=traffic_light.light_colors[lane])
    elif lane == "top":
        rect = plt.Rectangle((pos[0] - 0.7, pos[1] - 0.65), 0.3, 0.15, color=traffic_light.light_colors[lane])
    elif lane == "bottom":
        rect = plt.Rectangle((pos[0] + 0.4, pos[1] + 0.5), 0.3, 0.15, color=traffic_light.light_colors[lane])
    ax.add_patch(rect)
    rectangles[lane] = rect

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.axis('off')

car_patches = []
for lane in lanes_pos:
    for pos in car_positions[lane]:
        car_patch = plt.Rectangle((pos[0] - 0.15, pos[1] - 0.075), 0.3, 0.15, color='blue')
        ax.add_patch(car_patch)
        car_patches.append((lane, car_patch, pos))

car_count_texts = {}
for lane, pos in lanes_pos.items():
    car_count_text = ax.text(pos[0], pos[1] + 0.8, f"{lanes[lane]} cars", ha='center', va='center', fontsize=10,
                             color="black")
    car_count_texts[lane] = car_count_text


def update_visual(frame):
    for lane in lanes_pos:
        rectangles[lane].set_color(traffic_light.light_colors[lane])

    for lane, car_patch, pos in car_patches:
        if traffic_light.light_colors[lane] == 'green':
            if lane == "left":
                pos[0] += 0.1 if pos[0] < 2 else -4
            elif lane == "right":
                pos[0] -= 0.1 if pos[0] > -2 else 4
            elif lane == "top":
                pos[1] -= 0.1 if pos[1] > -2 else 4
            elif lane == "bottom":
                pos[1] += 0.1 if pos[1] < 2 else -4

            car_patch.set_xy([pos[0] - 0.15, pos[1] - 0.075])

    for lane in lanes_pos:
        car_count_texts[lane].set_text(f"{lanes[lane]} cars")

    return [car_patch for _, car_patch, _ in car_patches] + list(rectangles.values())


ani = animation.FuncAnimation(fig, update_visual, interval=100, blit=True)

plt.show()
