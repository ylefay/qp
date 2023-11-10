import jax
import jax.numpy as jnp
from lasso import solve_lasso, lasso_objective
from timeit import timeit
import matplotlib.pyplot as plt
from scipy.optimize import minimize

N = 100
OP_key = jax.random.PRNGKey(0)
keys = jax.random.split(OP_key, N)

shape = (40, 10)
mus = jnp.array([2, 10, 15, 50, 100])
penalization = 10
distrib = jax.random.uniform

for mu in mus:
    @timeit
    @jax.vmap
    def wrapper_lasso_barr_method(key):
        X, y = distrib(key, shape=shape), distrib(key, shape=(shape[0],))
        return solve_lasso(X, y, penalization=penalization, mu=mu, eps=1e-6)


    n_iters, n_iters_centering, _, _, values_for_dual_objective, lasso_objective_values = wrapper_lasso_barr_method(keys)
    for i in range(N):
        iteration = n_iters[i]
        n_iters_centering[i]
        reconstructed_values_for_dual_objective = jnp.concatenate(
            [values_for_dual_objective[i][:iteration][j][1:n_iters_centering[i][j]] for j in range(iteration)])
        min = jnp.min(reconstructed_values_for_dual_objective)
        plt.semilogy(range(len(reconstructed_values_for_dual_objective)), reconstructed_values_for_dual_objective - min)

    plt.title(f"{N} lasso problems w/ shape {shape[0], shape[1]}, semilog error, mu={mu}")
    plt.savefig(f"lasso_qp_{mu}", dpi=500)
    plt.close()

import numpy as np

shape = (40, 10)
X = np.zeros(shape)
y = np.zeros(shape[0])
X[:shape[0] // 2, 0] = 0
X[shape[0] // 2:, 0] = 2.5
y[:shape[0] // 2] = 0.5
y[shape[0] // 2:] = 1
X = jnp.array(X)
y = jnp.array(y)

lasso_minimize = minimize(lasso_objective, jnp.zeros(shape[-1]), args=(X, y, penalization), method='L-BFGS-B')
n_iter, _, _, _, _, objective = solve_lasso(X, y, penalization=penalization, mu=2)
print(lasso_minimize)
print(objective[:n_iter])
X = jnp.array([[1, 2], [3, 4]])
y = jnp.array([1, 2])
X = jnp.ones(shape)
y = jnp.ones(shape[0])

lasso_minimize = minimize(lasso_objective, jnp.zeros(shape[-1]), args=(X, y, penalization), method='L-BFGS-B')
n_iter, _, _, _, _, objective = solve_lasso(X, y, penalization=penalization, mu=2)
print(lasso_minimize)
print(objective[:n_iter])
