"""
网络重构算法 DWCM，基于 density corrected 版本。#HACK 这个方案还没有完成实现，也没有进行检测。暂时不能使用。后续需要的话再继续开发。

References:
    - Squartini T, Caldarelli G, Cimini G, 等, 2018. Reconstruction Methods for Networks: The Case of Economic and Financial Systems[J]. Physics Reports, 757: 1–47. DOI:10/gg86sz.
    - P. Mazzarisi, F. Lillo, Methods for reconstructing interbank networks from limited information: A comparison, Springer International Publishing, 2017, pp. 201–215. doi:10.1007/ 978-3-319-47705-3_15.
"""




import numpy as np
from scipy.optimize import minimize


def dwcm_density_corrected(N, gamma, delta, target_L):
    # Step 1: Calculate total number of links
    L = sum(gamma) + sum(delta)

    # Step 2: Calculate weight probability distribution
    def weight_prob(w, gamma, delta, z):
        p = z * gamma * delta / (1 + z * gamma * delta - gamma * delta)
        return p * ((gamma * delta) ** (w - 1)) * (1 - gamma * delta)

    # Step 3: Calculate Lagrange multipliers
    def lagrange_multipliers(gamma, delta, z):
        p = z * gamma * delta / (1 + z * gamma * delta - gamma * delta)
        return (gamma / (1 - gamma * delta), delta / (1 - gamma * delta), p)

    # Step 4: Calculate zeta to achieve target_L
    def objective(z, gamma, delta, target_L):
        p = z * gamma * delta / (1 + z * gamma * delta - gamma * delta)
        L_hat = np.sum(p)
        return (L_hat - target_L) ** 2

    result = minimize(objective, x0=0.1, args=(gamma, delta, target_L))
    zeta = result.x[0]

    return L, zeta, lagrange_multipliers(gamma, delta, zeta)

if __name__ == "__main__":
    # Example usage
    N = 10
    gamma = np.random.rand(N)
    delta = np.random.rand(N)
    target_L = 25

    L, zeta, (lambda_out, lambda_in, p) = dwcm_density_corrected(N, gamma, delta, target_L)
    print("Total number of links:", L)
    print("Zeta:", zeta)
    print("Lagrange multipliers for out-strength:", lambda_out)
    print("Lagrange multipliers for in-strength:", lambda_in)
    print("Weight probability distribution:", p)



    pass











# import numpy as np
#
#
# def density_corrected_DWCM(s_out, s_in, L_hat):
#     """
#     Implements the density-corrected Directed Weighted Configuration Model (dcDWCM)
#
#     Args:
#         s_out (np.ndarray): Out-strength sequence of the network
#         s_in (np.ndarray): In-strength sequence of the network
#         L_hat (float): Observed total number of links in the network
#
#     Returns:
#         p_ij (np.ndarray): Link probability matrix
#         w_ij (np.ndarray): Expected weight matrix
#     """
#     N = len(s_out)
#
#     # Compute the DWCM parameters
#     y_out = np.exp(-np.array([gamma_i for gamma_i in s_out]))
#     y_in = np.exp(-np.array([delta_i for delta_i in s_in]))
#
#     # Compute the dcDWCM link probability
#     p_ij = (z * y_out[:, None] * y_in[None, :]) / (1 + z * y_out[:, None] * y_in[None, :] - y_out[:, None] * y_in[None, :])
#
#     # Compute the expected weights
#     w_ij = p_ij / (1 - y_out[:, None] * y_in[None, :])
#
#     # Solve for the density correction parameter z
#     z = np.exp(-zeta)
#     zeta = fsolve(lambda x: np.sum(p_ij) - L_hat, 0)[0]
#
#     return p_ij, w_ij
#
# if __name__ == "__main__":
#     import numpy as np
#     from scipy.optimize import fsolve
#
#
#     def density_corrected_DWCM(s_out, s_in, L_hat):
#         """
#         Implements the density-corrected Directed Weighted Configuration Model (dcDWCM)
#
#         Args:
#             s_out (np.ndarray): Out-strength sequence of the network
#             s_in (np.ndarray): In-strength sequence of the network
#             L_hat (float): Observed total number of links in the network
#
#         Returns:
#             p_ij (np.ndarray): Link probability matrix
#             w_ij (np.ndarray): Expected weight matrix
#         """
#         N = len(s_out)
#
#         # Compute the DWCM parameters
#         y_out = np.exp(-np.array(s_out))
#         y_in = np.exp(-np.array(s_in))
#
#         # Compute the dcDWCM link probability
#         p_ij = (z * y_out[:, None] * y_in[None, :]) / (1 + z * y_out[:, None] * y_in[None, :] - y_out[:, None] * y_in[None, :])
#
#         # Compute the expected weights
#         w_ij = p_ij / (1 - y_out[:, None] * y_in[None, :])
#
#         # Solve for the density correction parameter z
#         z = np.exp(-zeta)
#         zeta = fsolve(lambda x: np.sum(p_ij) - L_hat, 0)[0]
#
#         return p_ij, w_ij
#
#
#     # Example usage with N=5
#     s_out = [10, 15, 20, 25, 30]
#     s_in = [12, 18, 22, 28, 35]
#     L_hat = 100
#
#     p_ij, w_ij = density_corrected_DWCM(s_out, s_in, L_hat)
#
#     print("Link probability matrix:")
#     print(p_ij)
#     print("\nExpected weight matrix:")
#     print(w_ij)

