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




[^1]: https://en.wikipedia.org/wiki/Standard_error
[^2]: https://en.wikipedia.org/wiki/Standard_deviation
[^3]: Flyvbjerg *et al.*, J. Chem. Phys. **1**, 461 (1989).
