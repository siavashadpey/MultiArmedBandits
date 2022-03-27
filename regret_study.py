import numpy as np 
import matplotlib.pyplot as plt
import os 

from multi_armed_bandits import Simulation, Bayesian

Ntrials = 500
Ndraws = 10000
ExpRegretBay = np.zeros((Ndraws))
ExpRegretTheory = np.zeros((Ndraws))
truth_probs = np.array([0.85, 0.6, 0.75])

def regret(Choices, truth_probs):
	Nchoices = Choices.shape[0]
	best_outcome_prob = truth_probs.max()
	regret = (truth_probs.max() - truth_probs[Choices.astype(int)]).cumsum()
	return regret

class TheoreticalUpperBound():
	def __init(self):
		pass

	def lb(a, b):
		return a/(a+b) - 1.65*np.sqrt((a*b)/( (a+b)**2*(a+b+1)))

	def choose(self, Ntrials, Nwins):
		X = TheoreticalUpperBound.lb(1 + Nwins, 1 + Ntrials - Nwins)

		# choose group with largest sample
		return np.argmax(X)


for i in range(Ntrials):
	sim = Simulation(Ndraws, truth_probs)
	bay_strat = Bayesian()
	sim.simulate(bay_strat)
	QueriesBay_i = sim.get_queries()
	RegretBay_i = regret(QueriesBay_i, truth_probs)
	ExpRegretBay += RegretBay_i

	sim.reset()
	theo_UB = TheoreticalUpperBound()
	sim.simulate(theo_UB)
	QueriesTheory_i = sim.get_queries()
	RegretTheory_i = regret(QueriesTheory_i, truth_probs)
	ExpRegretTheory += RegretTheory_i

ExpRegretBay /= Ntrials
ExpRegretTheory /= Ntrials


plt.plot(ExpRegretBay, label="Bayesian")
plt.plot(ExpRegretTheory, label="Theoretical bound")
plt.xlabel("Number of draws")
plt.ylabel("Cumulative expected regret")
plt.title("Cumulative expected regret vs. number of draws")
plt.tight_layout()
plt.ylim(ymin=0) 
plt.xlim(xmin=0) 
plt.legend()
plt.savefig(os.path.join("figs", "regret.png"), format="png")
