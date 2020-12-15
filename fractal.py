# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 17:14:22 2016

@author: Harts
"""


# Need to Fix Dragon Fractals (See todo list)
# N.B. I used flatten and segment in the HeighwayDragon code
#   Under the @staticmethod decorator (currently broken)
# All fractals requiring segmentation should use HeighwayDragon as parent

import cmath
import math

import gif
import matplotlib.pyplot as plt
import numpy as np


class Fractal:
    def __init__(self, S0, func_list):
        self.S0 = S0
        self.S = S0
        self.func_list = func_list
        self.plot_list = []
        self.angle = [0]
        # self.i = 0

    # TODO Optimize iterate
    def iterate(self, i):
        # self.plot_list.clear()
        for _ in range(i):
            S = []
            for func in self.func_list:
                S.extend(list(map(func, self.S)))
            self.S = S
        self.plot_list.append(S)
        # TODO: Get this code Usable for gif_plot()

    # Rotate and translate (in that order)
    def translate(self, offset, angle):
        S_trans = [i * cmath.exp(angle * 1j) +
                   offset for i in self.plot_list[0]]
        self.S = S_trans
        self.plot_list.append(S_trans)

    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        self.plot_handle = [ax.plot(np.real(s), np.imag(
            s), color='tab:blue') for s in self.plot_list]
        plt.axis('equal')
        plt.show()

    # Not intended for Call except through save_gif method
    @gif.frame
    def gif_plot(self):
        [plt.plot(np.real(s), np.imag(s), color='tab:blue')
         for s in self.plot_list]
        plt.ylim((-1, 1))
        plt.xlim((-1.5, 1.5))
        plt.axis('equal')

    def save_gif(self, iterations, duration=1000):
        frames = []
        for _ in range(iterations):
            self.iterate(1)
            frame = self.gif_plot()
            frames.append(frame)
        gif.save(frames, '{0}_{1}.gif'.format(
            type(self).__name__, iterations), duration)


# Another option for making the code cleaner...
class HeighwayDragon(Fractal):
    def __init__(self):
        super().__init__(S0=[0, 1],
                         func_list=[lambda z:  0.5 * (1 + 1j) * z,
                                    lambda z: 1 - 0.5 * (1 - 1j) * z])

    @staticmethod
    def flatten(t):
        return [item for sublist in t for item in sublist]

    def segment(self, points):
        len_ = len(self.S0)
        lines = [[*points[i:i+len_], np.nan]
                 for i in range(len(points)-len_+1) if i % len_ == 0]
        S_ = self.flatten(lines)
        return S_

    def plot(self):
        self.plot_list = [self.segment(s) for s in self.plot_list]
        super().plot()


# Vars used in twindragon
S0_twin = [0, 1, 1 - 1j]
def twin1(z): return 0.5 * (1 + 1j) * z
def twin2(z): return 1 - 0.5 * (1 + 1j) * z


class TwinDragon(HeighwayDragon):
    def __init__(self):
        super(HeighwayDragon, self).__init__(S0=S0_twin,
                                             func_list=[
                                                 twin1,
                                                 twin2])


# Vars Used in terdragon
lamda = .5 - 1j / 2 / math.sqrt(3)
lamdaconj = .5 + 1j / 2 / math.sqrt(3)


class Terdragon(Fractal):
    def __init__(self):
        super().__init__(S0=[0, 1],
                         func_list=[lambda z:  lamda * z,
                                    lambda z: 1j / math.sqrt(3) * z + lamda,
                                    lambda z: lamda * z + lamdaconj])


class FudgeFlake(Terdragon):
    def plot(self):
        self.translate(0, math.pi/3)
        self.translate(1, 2*math.pi/3)
        super().plot()


class LevyC(Fractal):
    def __init__(self):
        super().__init__(S0=[0, 1],
                         func_list=[lambda z: 0.5 * (1 - 1j) * z,
                                    lambda z: 1 + 0.5 * (1 + 1j) * (z - 1)])


class LevyTapestryOutside(LevyC):
    # TODO Get this to be able to iterate, then re-plot
    def plot(self):
        self.translate(1, math.pi)
        super().plot()


class LevyTapestryInside(LevyC):
    def plot(self):
        translations = [(-1j, math.pi*.5),
                        (1, -math.pi*.5),
                        (1-1j, math.pi)]
        [self.translate(off, theta) for off, theta in translations]
        super().plot()


# Vars used in koch snowflake
K0 = (0 + 1j)
Ka = (.5 + .5 * 1j * math.sqrt(3))
Kna = (.5 - .5 * 1j * math.sqrt(3))
kr = 1 / 3
SK = [-1, 0]


class KochFlake(Fractal):
    def __init__(self):
        super().__init__(S0=[0, 1],
                         func_list=[lambda z: kr * (z),
                                    lambda z: kr * (Ka * z + 1),
                                    lambda z: kr * (Kna * z + 1 + Ka),
                                    lambda z: kr * (z + 2)])
        self.translations = [
            (cmath.rect(-1, 2*math.pi/3), 2*math.pi/3),
            (1, -2*math.pi/3)]

    def plot(self):
        [self.translate(off, theta) for off, theta in self.translations]
        super().plot()


SF = []
S0i = [0, 1]


# Vars used in golden dragon
phi = (1 + math.sqrt(5)) * .5
r = (1 / phi)**(1 / phi)
A = math.acos((1 + r**2 - r**4) / 2 / r)
B = math.acos((1 - r**2 + r**4) / 2 / r**2)

# Vars used in Pentigree
P_r = (3 - math.sqrt(5)) * .5
P_a1 = (math.cos(.2 * math.pi) + 1j * math.sin(.2 * math.pi))
P_a2 = (math.cos(.6 * math.pi) + 1j * math.sin(.6 * math.pi))
P_na1 = (1 * math.cos(.2 * math.pi) + -1j * math.sin(.2 * math.pi))
P_na2 = (1 * math.cos(.6 * math.pi) + -1j * math.sin(.6 * math.pi))

# Vars used in pentadendrite
Dr = math.sqrt((6 - math.sqrt(5)) / 31)
RA = 0.20627323391771757578747269015392
PA = (1 * math.cos(RA) + 1j * math.sin(RA))
SA = (math.pi * 0.4)
BA = (1 * math.cos(RA + SA) + 1j * math.sin(RA + SA))
CA = (1 * math.cos(RA - SA) + 1j * math.sin(RA - SA))
DA = (1 * math.cos(RA - 2 * SA) + 1j * math.sin(RA - 2 * SA))
star = np.exp(1j * np.arange(0, 361, 72) * math.pi / 180)
pentagon = np.cumsum(star)


class Pentadendrite(Fractal):
    pass


# This seems like a cleaner way to make the IFS functions... Probably as
# members of the class
IFS_function = dict()
# Plain Ole' Dragon Curve
IFS_function['dragon'] = [
    lambda z:  0.5 * (1 + 1j) * z,
    lambda z: 1 - 0.5 * (1 - 1j) * z]
# z2 dragon curve
IFS_function['z2_dragon'] = [
    lambda z:  0.5 * (1 + 1j) * z,
    lambda z: -(1 - 0.5 * (1 - 1j) * z),
    lambda z: 1 - 0.5 * (1 - 1j) * z,
    lambda z: -(0.5 * (1 + 1j) * z)]

# Levy C


def func1(z): return 0.5 * (1 - 1j) * z


def func2(z): return 1 + 0.5 * (1 + 1j) * (z - 1)

# Twin Dragon


# Terdragon xtreme


def ter1(z): return lamda * z


def ter2(z): return 1j / math.sqrt(3) * z + lamda


def ter3(z): return lamda * z + lamdaconj

# golden dragon


def gd1(z): return r * z * cmath.exp(A * 1j)


def gd2(z): return r**2 * z * cmath.exp((math.pi - B) * 1j) + 1

# z2 golden dragon


def z2gd1(z): return gd1(z)


def z2gd2(z): return r * z * cmath.exp((A - math.pi) * 1j)


def z2gd3(z): return gd2(z)


def z2gd4(z): return r**2 * z * cmath.exp(-B * 1j) - 1

# z2 levy curve


def z2levy1(z): return func1(z)


def z2levy2(z): return -(1 + 0.5 * (1 + 1j) * (z - 1))


def z2levy3(z): return func2(z)


def z2levy4(z): return -(0.5 * (1 - 1j) * z)


# Pentigree

def pent1(z): return P_r * P_a1 * z


def pent2(z): return P_r * P_a2 * z + P_r * (P_a1)


def pent3(z): return P_r * P_na1 * z + P_r * (P_a1 + P_a2)


def pent4(z): return P_r * P_na2 * z + P_r * (P_a1 + P_a2 + P_na1)


def pent5(z): return P_r * P_na1 * z + P_r * (P_a1 + P_a2 + P_na1 + P_na2)


def pent6(z): return P_r * P_a1 * z + P_r * \
    (P_a1 + P_a2 + P_na1 + P_na2 + P_na1)

# Pentadendrite


def pend1(z): return Dr * (PA * z)


def pend2(z): return Dr * (BA * z + PA)


def pend3(z): return Dr * (PA * z + PA + BA)


def pend4(z): return Dr * (DA * z + 2 * PA + BA)


def pend5(z): return Dr * (CA * z + DA + 2 * PA + BA)


def pend6(z): return Dr * (PA * z + 2 * PA + BA + CA + DA)


if __name__ == "__main__":
    # heighway = TwinDragon()
    # heighway.iterate(10)
    # heighway.plot()
    # heighway.iterate(1)
    # heighway.plot()
    # levy = LevyC()
    # levy.save_gif(5)
    # z2_dragon = Fractal(S0i,IFS_function['z2_dragon'])
    # z2_dragon.save_gif('z2_dragon',10)
    # z2_dragon.iterate(10)
    # z2_dragon.plot()
    # z2levy = Fractal([0,1],[func1,z2levy2,func2,z2levy4])
    # z2levy.save_gif('z2levy', 10)
    # z2levy.iterate(10)
    # z2levy.plot()
    # twin_dragon = Fractal(S0_twin,[twin1,twin2])
    # twin_dragon.save_gif('Twin dragon', 17)
    # twin_dragon.iterate(1)
    # twin_dragon.plot()
    # terdragon = Fractal(S0i,[ter1,ter2,ter3])
    # terdragon.save_gif('terdragon',12)
    # terdragon.rotate([math.pi/3,2*math.pi/3])
    # terdragon.plot()
    # golden_dragon = Fractal(S0i,[gd1,gd2])
    # golden_dragon.save_gif('Golden_Dragon', 21)
    # golden_dragon.iterate(21)
    # golden_dragon.plot()
    # z2_golden_dragon = Fractal(S0i,[z2gd1,z2gd2,z2gd3,z2gd4])
    # z2_golden_dragon.save_gif('z2_golden_dragon',10)
    # z2_golden_dragon.iterate(10)
    # z2_golden_dragon.plot()
    # pentigree = Fractal(S0i,[pent1,pent2,pent3,pent4,pent5,pent6])
    # pentigree.save_gif('Pentigree', 8)
    # pentigree.iterate(8)
    # pentigree.plot()
    # pentadentrite = Fractal([0,1],[pend1,pend2,pend3,pend4,pend5,pend6])
    # pentadentrite.save_gif('Pentadentrite', 8)
    # pentadentrite.iterate(8)
    # pentadentrite.plot()
    # koch = KochFlake()
    # koch.iterate(9)
    # koch.plot()
    # fudge = FudgeFlake()
    # fudge.iterate(9)
    # fudge.plot()
    tap_outside = LevyTapestryOutside()
    # tap_outside.save_gif(5)
    tap_outside.iterate(11)
    tap_outside.plot()
    # tap_outside.iterate(4)
    # tap_outside.plot()
    pass
