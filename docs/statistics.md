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




[^1]: https://en.wikipedia.org/wiki/Standard_error
[^2]: https://en.wikipedia.org/wiki/Standard_deviation
