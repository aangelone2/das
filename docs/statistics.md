# Statistical introduction


## Uncorrelated data

For an uncorrelated data set $[x_1, \ldots, x_n]$, the
arithmetic mean $m$ and the standard error of the mean
(SEM)[^1] are computed as

$$
m = \frac{1}{n} \sum_{i = 1}^n x_i
$$

$$
\operatorname{SEM} = \sqrt{\frac{1}{n(n - 1)} \sum_{i = 1}^n
\left( x_i - m \right)^2}
$$

where the sample standard deviation is estimated with the
Bessel correction[^2].


## Correlated data

We obtain an estimate for the SEM of correlated data using a
blocking procedure[^3], which goes as follows:

- The $n$ data points are binned in $n'$ blocks (where $n'$ is
  usually taken, as in our case, to be a power of $2$).

- The SEM is computed for the binned data.

- The procedure is repeated with $n' \leftarrow n'/2$ (i.e.,
  joining pairs of neighboring blocks from the previous stage)
  until a minimum amount of blocks (here, $64$) is reached.

The SEM as a function of the bin size (i.e., for decreasing
$n'$) is guaranteed to be a monotonously increasing
function[^3], with a fixed point which corresponds to the
uncorrelated SEM.

Decreasing $n'$ will thus result in the estimates for the SEM
to grow, either indefinitely (if not enough points are
available to obtain decorrelated estimates within the specified
$n'$) or until they remain constant within fluctuations
(reaching a plateau which extends for several consecutive
values of $n'$).

Such fluctuations can be gauged via the error on the SEM, which
can be estimated as[^3]:

$$
\operatorname{SE}(\operatorname{SEM}(n')) =
\operatorname{SEM}(n') \cdot \frac{1}{\sqrt{2 (n' - 1)}}
$$

If the plateau is reached, the obtained SEMs can be taken as
estimates for the actual error free from correlation effects.

Such a binning analysis can also be used to extract the
autocorrelation time for time-series data once error
convergence has been reached (and therefore an estimate for the
true SEM of the data is obtained as the binned SEM
$\operatorname{SEM}\_B$). The integrated autocorrelation time
then becomes[^4]

$$
\tau = \frac{1}{2} \left(
\frac{\operatorname{SEM}\_B}{\operatorname{SEM}\_0} \right)^2,
$$

where $\operatorname{SEM}\_0$ is the standard error of the
original, unbinned data.


## Jackknife analysis

The jackknife protocol[^5] is commonly used to estimate the
errors of complex functions of mean values, which may be
underestimated by simply applying error propagation techniques.

The prescription discussed here is used to compute the error on
an estimator $\widehat{\theta}$ for a parameter $\theta$, based
on the data set $[x_1, \ldots, x_n]$.

To begin, one groups the data in $n_b$ bins of size $b$ each.
This is necessary in the case of correlated data, in order to
attempt to obtain decorrelated estimates; a scaling on the bin
size may also be performed.

In terms of the binned data, one then defines
$\widehat{\theta}\_{-i}$ as the estimator for
$\widehat{\theta}$ where the $i$-th bin has been neglected
(e.g., a function of the mean of the $x_i$ computed on the
average where one of the blocks is removed from the dataset).

From this definition, one finally introduces the corresponding
$i$-th *pseudovalue* as

$$
\widetilde{\theta}\_i = n_b \cdot \widehat{\theta} - (n_b - 1)
\widehat{\theta}\_{-i}
$$

One can show that:

- The average of the pseudovalues is an estimator for $\theta$.

- The pseudovalues can be treated as a set of approximately
  independent and identically distributed random variables.

This allows to infer confidence intervals on the average of the
pseudovalues and their SEM, which bind the original parameter
$\theta$.




[^1]: https://en.wikipedia.org/wiki/Standard_error.
[^2]: https://en.wikipedia.org/wiki/Standard_deviation.
[^3]: Flyvbjerg *et al.*, J. Chem. Phys. **1**, 461 (1989), Sec. IV.
[^4]: Grotendorst *et al.*, *Quantum simulations of complex many-body systems: from theory to algorithms* Winter School Lecture Notes, Rolduc Conference Centre, Kerkrade, The Netherlands (2002).
[^5]: Miller, Biometrika **61**, 1 (1974).
