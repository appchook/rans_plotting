# rans_plotting

```
wget https://raw.githubusercontent.com/appchook/rans_plotting/main/rans_table.py
wget https://raw.githubusercontent.com/appchook/rans_plotting/main/rans_plot.py
```
```
pip install plotext
pip install tabulate
```

run `python rans_table.py` to get:

```
Volume_Algorithm                 Training     AVG           change      cur                 total
                                 remaining    encryption    in trend    encryption         blocks
                                              ratio                     ratio           processed
-------------------------------  -----------  ------------  ----------  ------------  -----------
1777774654639749081_CU_SUM                    0             0           0.0                    22
1777774654639749081_AVG_ENTROPY               6             230         0.0                    22
1777774654639749090_CU_SUM       00:01:00     0             0           0.0                   205
1777774654639749090_AVG_ENTROPY  00:01:00     0             0           0.0                   205
1777774654639749092_CU_SUM                    0             0           0.0                    29
1777774654639749092_AVG_ENTROPY               38            600         0.0                    29
```

run `python rans_plot.py 7779661018273837374_CU_SUM` to get:

```
     ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
35.00┤ L RR enc ratio (left Axis)        TTT                        T                       T            RRRRRRRRRRRRR├24000.0
     │ ⅃ TT change in trend (right Axis)    TTTTTT            TTTTTT TTTTTT           TTTTTT TTTT       R             │
     │          T                                 TTTTTTTTTTTT             TTTTTTTTTTT           TTTT RR              │
     │          T                                                                                    TTTTT            │
34.50┤         T                                                                                   RR     TTTTTT      ├23926.8
     │         T                                                                                 RR             TTTTTT│
     │        T                                                                                 R                     │
     │        T                                                                               RR                      │
34.00┤       T                             RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR                        ├23853.7
     │       T                            R                                                                           │
     │      T                           RR                                                                            │
33.50┤      T                         RR                                                                              ├23780.5
     │     T                         R                                                                                │
     │     T                       RR                                                                                 │
     │    T                      RR                                                                                   │
33.00┤    T       RRRRRRRRRRRRRRR                                                                                     ├23707.3
     │   T       R                                                                                                    │
     │   T     RR                                                                                                     │
     │  T     R                                                                                                       │
32.50┤  T   RR                                                                                                        ├23634.2
     │ T   R                                                                                                          │
     │ T RR                                                                                                           │
     │T R                                                                                                             │
32.00┤TR                                                                                                              ├23561.0
     └┬───────────────────────────┬───────────────────────────┬──────────────────────────┬───────────────────────────┬┘
     1.0                         3.2                         5.5                        7.8                        10.0
```
- (note 1: The graph would automatically refresh as new data gets in)
- (note 2: Use ZVM tweak "t_ransomwareEngLogFreqSec" with value of "10" to refresh the graph faster)

