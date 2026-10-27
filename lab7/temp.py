from math import sqrt
from typing import Iterable, Tuple

def _normalize(v: Iterable[float]) -> Tuple[float, float, float]:
    x, y, z = map(float, v)
    n = sqrt(x*x + y*y + z*z)
    return (x/n, y/n, z/n) if n else (x, y, z)

def _dot(a: Iterable[float], b: Iterable[float]) -> float:
    ax, ay, az = a
    bx, by, bz = b
    return ax*bx + ay*by + az*bz

def _clamp01(x: float) -> float:
    return 0.0 if x < 0 else (1.0 if x > 1 else x)

def _round_rgb(rgb, decimals=3):
    return tuple(round(float(c), decimals) for c in rgb)

def phong_diffuse(n, l, Ip, kd, Od, decimals=3):
    """
    I_d = Ip * kd * Od * max(0, n·l)
    """
    n = _normalize(n)
    l = _normalize(l)
    ndotl = _clamp01(_dot(n, l))
    r = [c * kd * ndotl for c in Od]                  # scale by kd*Od
    out = [Ip[i] * r[i] for i in range(3)]            # then by light color
    return _round_rgb(out, decimals)

def phong_specular(n, l, v, Ip, ks, Os, kgls, decimals=3):
    """
    r = 2(n·l)n − l
    I_s = Ip * ks * Os * max(0, r·v)^kgls
    """
    n = _normalize(n)
    l = _normalize(l)
    v = _normalize(v)
    ndotl = _clamp01(_dot(n, l))
    # reflection vector
    r = (2*ndotl*n[0] - l[0], 2*ndotl*n[1] - l[1], 2*ndotl*n[2] - l[2])
    # normalize r (helps numerical stability)
    r = _normalize(r)
    rdotv = _clamp01(_dot(r, v))
    spec_factor = (rdotv ** kgls) * ks
    out = [Ip[i] * Os[i] * spec_factor for i in range(3)]
    return _round_rgb(out, decimals)

def phong_ambient(Ia, ka, Od, decimals=3):
    """
    I_a = Ia * ka * Od
    """
    out = [Ia[i] * ka * Od[i] for i in range(3)]
    return _round_rgb(out, decimals)

def phong_total(n, l, v, Ip, Ia, ka, kd, ks, kgls, Od, Os, decimals=3):
    """
    I = I_d + I_s + I_a
    """
    Id = phong_diffuse(n, l, Ip, kd, Od, decimals=10)   # higher precision internally
    Is = phong_specular(n, l, v, Ip, ks, Os, kgls, decimals=10)
    Ia_comp = phong_ambient(Ia, ka, Od, decimals=10)
    out = [float(Id[i]) + float(Is[i]) + float(Ia_comp[i]) for i in range(3)]
    return _round_rgb(out, decimals)


n  = (0.58, 0.58, -0.58)
l  = (0.53, 0.80, -0.27)
v  = (0.0, 0.0, -1.0)

Ip = (0.9, 0.9, 0.72)
Ia = (0.1, 0.1, 0.08)

ka = 0.1
kd = 0.1
ks = 0.8
kgls = 4

Od = (0.2, 0.4, 1.0)
Os = (1.0, 1.0, 1.0)

print("Diffuse :", phong_diffuse(n, l, Ip, kd, Od))
print("Specular:", phong_specular(n, l, v, Ip, ks, Os, kgls))
print("Ambient :", phong_ambient(Ia, ka, Od))
print("Total   :", phong_total(n, l, v, Ip, Ia, ka, kd, ks, kgls, Od, Os))
