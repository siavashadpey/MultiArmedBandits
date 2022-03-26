import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt

truth_probs = np.array([0.85, 0.6, 0.75])
Ngroups = truth_probs.shape[0]

def query(i):
	# TODO: replace by actual data
	return np.random.rand() < truth_probs[i]

xx = np.linspace(0.001,.999,200)

dists = np.random.beta

Ntrials = np.zeros(Ngroups)
Nconversions = np.zeros(Ngroups)

Nqueries = 5000
Queries = np.zeros(Nqueries)
plot_dist = True
for query_i in range(Nqueries):

	# sample from all distributions
	X = dists(1 + Nconversions, 1 + Ntrials - Nconversions)

	# choose group with largest sample
	grp_idx = np.argmax(X)

	# query from this group
	r = query(grp_idx)

	# update this group's distribution
	Ntrials[grp_idx] += 1
	Nconversions[grp_idx] += r
	Queries[query_i] = grp_idx

	if plot_dist and query_i % 300 == 0:
		print(query_i)
		for igrp in range(Ngroups):
			yy = stats.beta(1 + Nconversions[igrp], 1 + Ntrials[igrp] - Nconversions[igrp])
			p = plt.plot(xx, yy.pdf(xx), label='Group {0:d}'.format(igrp))
			c = p[0].get_markeredgecolor()
			plt.vlines(truth_probs[igrp], 0, yy.pdf(truth_probs[igrp]),
                       colors = c, linestyles = "--")

		plt.legend()
		plt.autoscale(tight = True)
		plt.show()
		
fig, (ax,ax2) = plt.subplots(nrows=2, sharex=True)

#extent = [Nqueries[0]-(Nqueries[1]-Nqueries[0])/2., Nqueries[-1]+(Nqueries[1]-Nqueries[0])/2.,0,1]
ax.imshow(Queries[np.newaxis,:], cmap="plasma", aspect="auto")
ax.set_yticks([])
#ax.set_xlim(extent[0], extent[1])

ax2.plot(range(Nqueries),Queries)

plt.tight_layout()
plt.show()



# plot chosen group vs. query index
# 1d plot where colors indicate group 
