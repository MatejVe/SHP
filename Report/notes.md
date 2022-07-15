# Senior Honours Project Notes

## 24/01/2022 Initial meeting with Graeme

- worked on collision dynamics before the meeting
- started reading through the suggested paper
- started working on the simulation itself

## 29/01/2022 code updates

- progress on finding the next collision within the simulation
- simultaneous collisions remain to be fixed
- issue of particles 'phasing' through remains

## 31/01/2022 meeting with Graeme

- issue of particles phasing through was fixed by forcing the particles to be ordered left to right (index the particles, after any number of collisions the indexes must follow a certain ordering)
- simultaneous collisions issue needs to be fixed
- discussion of the code with Graeme and how to fix the problems

## 04/02/2022 update

- no particles phasing through, 3 particles colliding simultaneously works
- both of these issues solved by using the "decimal" module, it helps with float numbers calculations
- logger is established - user provides what data is to be written down in a file (to be analysed later)
- an animation is created

## 07/02/2022 meeting with Graeme

- created a literature review - explored all the papers cited in the suggested paper
- discussed where to take the project next - settled on binary strings generation
- online research doesn't indicate this has been done before so should be a good project to undertake
- came up with possible outlines of the final project report

## 14/02/2022 meeting with Graeme

- first plots - momentum distributions and position space distributions (they follow the expected distributions: momentum - arcsine distribution, position - triangular distribution)
- started the collisions string generation and tested their entropy - entropy stabilizes at 1 bit fairly early, already for strings of length $\sim 100$
- random generated strings also have entropy of 1 bit
- discussed the preliminary version report to be sent for feedback - settled on overleaf

## 23/02/2022 feedback received

- improved the report based on feedback

## 26/02/2022 code updates

- conducted more particle experiments, increased the number of collisions to $100000$
- tested out their resulting velocity and position distributions, the distributions become more convergent for a bigger number of collisions
- further testing of string entropy

## 27/02/2022 code update

- zlib compression algorithm comparison of efficiency on collision generated strings and numpy random strings, for differing string lengths (logspace, from $10^2$ to $10^7$)
- entropy comparisson of collision generated strings and numpy random strings, for differing string lengths (logspace)

## 28/02/2022 code update

- bz2 algorithm added, compression comparison on differing strings lengths (logspace, from $10^2$ to $10^7$)
- bz2 and zlib algorithms have a compression limit on random strings of $\sim 16\%$, collision generated strings compress much better
- added error calculations
- switched from calculating the uncompressed/compressed ratio to compressed/uncompressed - it is more intuitive to understand
- added a custom run-length encoding compression algorithm to the comparisons (it works as follows: $aabbbcbb$ compressed to $2a3bc2b$)

## 05/03/2022 code update

- added the unbiased error estimation - jackknife error estimation
- code refactoring

## 07/03/2022 meeting with Graeme

- discussed current results
- started using the runs test of randomness

## 10/03/2022 code update

- runs test vs mass ratio done, areas of low Z scores observed (some lower than $Z=1.96$ which is the threshold for $95\%$ confidence of randomness, these areas are around $\frac{m_1}{m_3} \in [0.05, 0.2], \frac{m_2}{m_3} \in [0.3, 1]$ and vice versa since the plot is symmetric around the y=x axis)
- cut through the $\frac{m_2}{m_3} = 0.87, m_3 = 1$ is made, minimum average (average of 10 different strings for a given mass ratio) runs test Z score found to be $Z=2.08$
- figures updates
- main body of the report is written by now

## 14/03/2022 meeting with Graeme

- discussion about some new ideas, nothing significant
- discussion of various parts of the report
- polishing of the figures
- creation of compression percentages for differing mass ratios (2d space of mass ratios, color shows the compression percentage, used zlib, bz2 and the custom compression algorithm)

## 21/03/2022 meeting with Graeme

- discussed the possibility of analytical calculation of probability of obtaining a particular digit in the next collision
- discussed the new ideas of using FFT or autocorrelation function to represent some results
- discussion about the discrepancies of the results between different compression algorithms (especially bz2, better compression of strings that pass the runs test)
- discussed minor questions about the report

## 28/03/2022 meeting with Graeme

- discussion of minor report questions and mathematical details
- finished a sample calculation of analytical probability, full treatment requires a lot more work

## Code is on github, resulting progress can be seen in the commit history
