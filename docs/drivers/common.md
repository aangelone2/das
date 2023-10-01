# Common features

All the drivers offered by `das` share the common arguments and
options discussed below.


## Positional arguments

All drivers accept a `file` argument. This should be the path
to a plain text or `.gz` file with the following features:

- Single-space-separated columns. All rows should have the same
  column number.
- Lines beginning with `#` will be considered as comments and
  ignored. The file may have empty lines.


## Options guide

- `-f, --fields` accepts a comma-separated list of integers,
  representing the fields to parse within the file. *The fields
  are indexed starting from 1 in the option.* If not specified,
  *all* the fields will be parsed.

- `-s, --skip` accepts an integer (between 1 and 100), which
  corresponds to the percentage of rows to discard at the
  beginning of the file. Rounding may occur to obtain an
  integer number of rows.

- `-b, --basic` will toggle a basic output mode, without
  special characters (more friendly to automatic parsing
  tools). If the option is absent, the default output mode
  (using `rich`-based formatting) will be used.

- `-q, --quick` will make the parser skip the integrity check
  on the file rows (i.e., the verification that all rows have
  the same number of columns).

    If a field value is missing *in* (e.g., 3rd field for `--f
    1,2,3`) or *between* (e.g., 3rd field for `-f 1,2,4`) the
    specified fields, an error will still be raised.

- `-v, --verbose` will print additional information in the
  output: specifically, `<analyzed>/<total> rows`, where the
  two numbers are the number of rows employed in the analysis
  and the total number of rows.
