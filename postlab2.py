import matplotlib.pyplot as plt
import functools

Kp: float = 1.6
beta: float = -0.677
gamma: float = 16.93
RPS: float = 15
delta_T: float = 1/RPS

a=15/16
b=1/16

w_d = 1

# iterator returning the next value of w given a starting value.
def w(start: float, iterations: int):
    # calculates the c[n] of this step.
    def c(w_n: float, w_n_prev: float):
        return Kp * (w_d - (a*w_n + b*w_n_prev))

    # The current value of w.
    w_n: float = start
    # The previous value of w.
    w_n_prev: float = start
    for _ in range(iterations):
        # Calculates the current value of w_n
        w_next = w_n + delta_T * (beta * w_n + gamma * c(w_n, w_n_prev))
        for i in range(3):
            yield w_n
        # Sets the previous value of w to the current value.
        w_n_prev = w_n
        # Sets the current value of w to the next value.
        w_n = w_next

# Draws a graph of the values of w for the first 2 seconds.
def draw_graph():
    # The number of values to draw.
    num_points = int(3 / delta_T)
    # The values of w to draw.
    w_values = [w_n - w_d for w_n in w(0, num_points)]
    # The time values to draw.
    time_values = [delta_T/3 * n for n in range(num_points * 3)]
    # Draws the graph.
    plt.plot(time_values, w_values)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (rad/s)")
    plt.title("Angular Velocity Deviation of the Motor Over Time")
    plt.show()

draw_graph()