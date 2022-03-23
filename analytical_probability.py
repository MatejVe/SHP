import matplotlib.pyplot as plt
import numpy as np

masses1 = np.linspace(0.1, 1, 100)
masses2 = np.linspace(0.1, 1, 100)

def probability(m1, m2, m3):
    try:
        K = 2/(1-m2/m1)
        alpha = 1/(4*m2**2) - 1/(m1*m2) - 1/m2**2 \
            - 1/(m1*m3) - 1/(m2*m3)
        beta = 1/(2*m2) + 1/(2*m3)
        gamma = 1/(np.sqrt(1/(2*m1) + 1/(8*m2) + 1/(8*m3)))
        A = K/(K+1)
        delta = 1 - A/(4*beta*m2)
        theta = A/(2*beta)*gamma
        C = theta/(np.sqrt(delta**2 - theta**2 * alpha/gamma**2))
        return 1/2 - 1/np.pi * np.arcsin(C)
    except ZeroDivisionError:
        return 0

probs = []
for m1 in masses1:
    row = []
    for m2 in masses2:
        row.append(probability(m1, m2, m3=1))
    probs.append(row)

fig, axes = plt.subplots(1, 1, figsize=(9, 6))
plot = axes.contourf(probs, extent=[0,1,0,1], origin='lower')
plt.colorbar(plot, ax=axes)
axes.set_title('Analytical probability of special collision')
axes.set_xlabel('$m_1/m_3$ ratio')
axes.set_ylabel('$m_2/m_3$ ratio')
plt.tight_layout()
plt.savefig('analytical_prob')
plt.close()