from matplotlib import pyplot as plt
from matplotlib import patches
import numpy as np

if __name__ == "__main__":
    plt.figure(figsize=(3, 3))
    plt.plot([0], [0])
    plt.xticks([0, 1], ["0", "D"])
    plt.yticks([0, np.pi / 2], ["0", "$\\frac{\\pi}{2}$"])
    plt.xlim(0, 1.2)
    plt.ylim(0, np.pi * 1.2 / 2.0)
    plt.xlabel("Position $p$")
    plt.ylabel("Angle $\\theta$")
    ax = plt.gca()
    ax.add_patch(patches.Rectangle((0, 0), 1, np.pi / 2, fc="none", ec="k", alpha=0.1))
    plt.tight_layout()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))
    plt.savefig("fig_buffon_phase_space.png", dpi=300)

    ############################################################

    theta = np.linspace(0, np.pi / 2, 100)
    p = 1.0 - 0.75 * np.sin(theta)
    plt.figure(figsize=(3, 3))

    plt.plot(p, theta)
    plt.axvline(0.25, color="k", alpha=0.1, lw=1, ls="--")
    plt.text(0.9, np.pi / 2.0 * 0.9, "Crosses", ha="right", va="bottom")
    plt.text(0.1, np.pi / 2.0 * 0.1, "Doesn't cross", ha="left", va="top")

    plt.xticks([0, 0.25, 1], ["0", "$D-L$", "$D$"])
    plt.yticks([0, np.pi / 2], ["0", "$\\frac{\\pi}{2}$"])
    plt.xlim(0, 1.2)
    plt.ylim(0, np.pi * 1.2 / 2)
    plt.xlabel("Position $p$")
    plt.ylabel("Angle $\\theta$")
    ax = plt.gca()
    ax.add_patch(patches.Rectangle((0, 0), 1, np.pi / 2, fc="none", ec="k", alpha=0.1))
    plt.tight_layout()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))
    plt.savefig("fig_buffon_cross_no_cross_caseA.png", dpi=300)

    ############################################################

    theta = np.linspace(0, np.pi / 2, 100)
    p = 1.0 - 1.3 * np.sin(theta)
    theta = theta[p >= 0.0]
    p = p[p >= 0.0]
    plt.figure(figsize=(3, 3))

    thetac = np.max(theta)
    plt.plot(p, theta)
    # plt.axhline(thetac, color="k", alpha=0.1, lw=1, ls="--")
    plt.text(0.9, np.pi / 2.0 * 0.9, "Crosses", ha="right", va="bottom")
    plt.text(0.1, np.pi / 2.0 * 0.1, "Doesn't cross", ha="left", va="top")

    plt.xticks([0, 1], ["$0$", "$D$"])
    plt.yticks([0, thetac, np.pi / 2], ["0", "$\\theta_c$", "$\\frac{\\pi}{2}$"])
    plt.xlim(0, 1.2)
    plt.ylim(0, np.pi * 1.2 / 2)
    plt.xlabel("Position $p$")
    plt.ylabel("Angle $\\theta$")
    ax = plt.gca()
    ax.add_patch(patches.Rectangle((0, 0), 1, np.pi / 2, fc="none", ec="k", alpha=0.1))
    plt.tight_layout()
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["left"].set_position(("data", 0))
    ax.spines["bottom"].set_position(("data", 0))
    plt.savefig("fig_buffon_cross_no_cross_caseB.png", dpi=300)
