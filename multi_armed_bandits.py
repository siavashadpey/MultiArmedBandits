import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt
import os 

xx = np.linspace(0.001,.999,200) # used for plotting distribution

class Bayesian():
	def __init__(self):
		self._dists = np.random.beta

	def choose(self, Ntrials, Nwins):
		X = self._dists(1 + Nwins, 1 + Ntrials - Nwins)

		# choose group with largest sample
		return np.argmax(X)

	def plot(self, i, Nwins, Ntrials):
		for igrp in range(Nwins.shape[0]):
			yy = stats.beta(1 + Nwins[igrp], 1 + Ntrials[igrp] - Nwins[igrp])
			p = plt.plot(xx, yy.pdf(xx), label='Group {0:d}'.format(igrp))
			c = p[0].get_markeredgecolor()
			plt.vlines(truth_probs[igrp], 0, yy.pdf(truth_probs[igrp]),
            	       colors = c, linestyles = "--")
		plt.title("Posteriori distribution after {:d} draws".format(i))

		plt.legend()
		plt.autoscale(tight = True)
		#plt.show()
		path = os.path.join("figs", "draws_{:d}.png".format(i))
		plt.savefig(path,format="png")
		plt.close()


class Simulation():
	def __init__(self, Nqueries, truth_probs):
		self._Nqueries = Nqueries
		self._truth_probs = truth_probs # this is the underlying probability. In reality we do not know it so we can't use it directly.
		self._Nchoices = truth_probs.shape[0]
		self._Ntrials = np.zeros(self._Nchoices)
		self._Nwins = np.zeros(self._Nchoices)
		self._Queries = np.zeros(self._Nqueries)

	def reset(self):
		self._Ntrials = np.zeros(self._Nchoices)
		self._Nwins = np.zeros(self._Nchoices)
		self._Queries = np.zeros(self._Nqueries)

	def query(self, i):
		# TODO: replace by actual data
		return np.random.rand() < self._truth_probs[i]

	def simulate(self, choice_strategy, to_plot = False):
		for query_i in range(self._Nqueries):

			chosen_grp = choice_strategy.choose(self._Ntrials, self._Nwins)

			# query from this group's
			r = self.query(chosen_grp)

			# update this group's stats
			self._Ntrials[chosen_grp] += 1
			self._Nwins[chosen_grp] += r

			self._Queries[query_i] = chosen_grp

			if to_plot and query_i % (self._Nqueries/10.0) == 0:
				choice_strategy.plot(query_i, self._Nwins, self._Ntrials)

		if to_plot:
			fig, ax = plt.subplots()
			plt.title("Draw history")
			ax.imshow(self._Queries[np.newaxis,:], cmap="plasma", aspect="auto")
			ax.set_yticks([])
			ax.set_xlabel("Draw number")
			plt.tight_layout()
			plt.savefig(os.path.join("figs", "draw_history.png"), format="png")
			plt.close()

	def get_queries(self):
		return self._Queries

if __name__ == '__main__':
	Ndraws = 5000
	truth_probs = np.array([0.85, 0.6, 0.75])
	to_plot = True
	sim = Simulation(Ndraws, truth_probs)
	bay_strat = Bayesian()
	sim.simulate(bay_strat, to_plot)
