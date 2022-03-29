import matplotlib.pyplot as plt
import numpy as np

masses1 = np.linspace(0, 1, 1000)
masses2 = np.linspace(0, 1, 1000)

def probability(m1, m2, m3):
    a = m1/m3
    b = m2/m3
    numerator = a*b*((b+1)**2+a*b+a)
    denominator = (b+1)*((a*b+2*a+b**2+b)**2+a*(3*a+4*b+4*b**2+4*a*b))
    const = 1/2 * np.sqrt(numerator/denominator)
    if m1 > m2:
        return 1/4 - 1/(2*np.pi) * np.arcsin(1-2*const)
    elif m1 < m2:
        return 1/4 + 1/(2*np.pi) * np.arcsin(1-2*const)
    elif m1 == m2:
        return 0

probs = []
for m1 in masses1:
    row = []
    for m2 in masses2:
        prob = probability(m1, m2, m3=1)
        row.append(prob)
    probs.append(row)

fig, axes = plt.subplots(1, 1, figsize=(9, 6))
plot = axes.contourf(probs, extent=[0,1,0,1], origin='lower', cmap='magma')
plt.colorbar(plot, ax=axes)
axes.set_title('Analytical probability of a collision in which both particles \n travel in the same direction after colliding')
axes.set_xlabel('$m_1/m_3$ ratio')
axes.set_ylabel('$m_2/m_3$ ratio')
plt.tight_layout()
plt.savefig('analytical_prob')
plt.close()