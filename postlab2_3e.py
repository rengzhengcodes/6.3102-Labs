# Remix of https://colab.research.google.com/drive/1sBG-LTzw0AmxWcTKHPF_CQIOwtzwytMg#scrollTo=_AmNBZsdZQQ-
import cmath
import numpy as np
import matplotlib.pyplot as plt

Kp: float = 1.6
beta: float = -0.677
gamma: float = 16.93
RPS: float = 15
dT: float = 1/RPS

## Plot paths of natural frequencies
def plot_lams_evolution(lams_lists):
  # Plot natural frequencies as continuous series
  for lams in lams_lists:
    plt.plot(lams.real, lams.imag, alpha=0.8);
  ax = plt.gca();

  # Plot unit circle
  circle = plt.Circle((0,0), 1, color='lightgray', alpha=0.5, fill=True,
                      zorder=-1);
  ax.add_patch(circle);
  ax.set_aspect('equal');

  # Axis labels
  ax.set_xlabel('Re($\lambda$)');
  ax.set_ylabel('Im($\lambda$)');

## Plot computed natural freqs over list of Kp values
def plot_zoomed_lams_for_ab_pairs(lams_lists, ab_list, tol=1e-12):
  fig, axes = plt.subplots(1, len(lams_lists), figsize=(10,3));
  for i, (ax, lams) in enumerate(zip(axes, lams_lists)):
    # Plot natural freqs with Kp labels and color coding (green if mag < 1, red otherwise)
    get_color = lambda val: 'b' if np.abs(val) + tol < 1 else 'r'
    ax.scatter(lams.real, lams.imag, c = [get_color(lam) for lam in lams]);
    for k, ab in enumerate(ab_list):
      ax.annotate("  $(a, b)$ = {}".format(ab), (lams[k].real, lams[k].imag));

    # Plot unit circle
    _ = ax.get_xlim(), ax.get_ylim()  # Trick to keep axis limits fixed
    circle = plt.Circle((0,0), 1, color='lightgray', alpha=0.3, fill=True,
                        clip_on=True, zorder=-1);
    ax.add_patch(circle);

    # Title and axis
    ax.set_title('$\lambda_{}$'.format(i+1));
    ax.set_xlabel('Re($\lambda$)');
    ax.set_ylabel('Im($\lambda$)');

  plt.tight_layout()

# Global a,b lam correlation
global_ab_lam = None
# Compute natural freqs for a list of ab values (for fixed Ktheta)
def calc_lams_ab_for_abs(ab_list):
  global global_ab_lam 
  global_ab_lam = [(np.linalg.eig(np.array([[1+ dT*beta - dT*gamma*Kp*a, -dT*gamma*Kp*b],
                                  [1, 0]]))[0], (a, b)) for a, b in ab_list];
  lams = [lam for lam, ab in global_ab_lam]
  lams1, lams2 = list(zip(*lams));
  return np.array(lams1), np.array(lams2)

ab_list = []
for a in np.linspace(0, 1, 1000):
  for b in np.linspace(0, 1, 1000):
    if a + b == 1:
        ab_list.append((a, b))
ab_list = tuple(ab_list)
lams = calc_lams_ab_for_abs(ab_list)
plot_lams_evolution(lams)

# Finds and prints the values of a and b that give the smallest natural frequency pairs.
min_ab = None
min_mag_tot = 2
for i, lam_ab in enumerate(global_ab_lam):
    lam, ab = lam_ab
    if (mag_tot := abs(lam[0]) + abs(lam[1])) < min_mag_tot:
        min_ab = ab
        min_mag_tot = mag_tot

print(f"Freq Mag: {min_mag_tot}, (a, b): {min_ab}")

plt.show()