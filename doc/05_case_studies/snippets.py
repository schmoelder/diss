
```{code-cell} python3
import numpy as np
import matplotlib.pyplot as plt
x = np.arange(0,10)
y = np.arange(0,10)
fig, ax = plt.subplots()
ax.plot(x, y)
```

```{code-cell} python3
import ipywidgets as widgets
tab_contents = ['P0', 'P1', 'P2', 'P3', 'P4']
children = [widgets.Text(description=name) for name in tab_contents]
tab = widgets.Tab()
tab.children = children
for ii in range(len(children)):
    tab.set_title(ii, f"tab_{ii}")
tab
```


```{code-cell} python3
from myst_nb import glue
import numpy as np
import matplotlib.pyplot as plt
x = np.arange(0,10)
y = np.arange(0,10)
fig, ax = plt.subplots()
ax.plot(x, y)
glue("fun-fish", fig, display=False)
```


```{glue:figure} fun-fish
:figwidth: 300px
:name: "fun-fish"

This is a **caption** about linear fish.
```

This works:
```md
- {ref}`fun-fish`
- [Alternative caption](fun-fish)
```
output:
- {ref}`fun-fish`
- [Alternative caption](fun-fish)

This does not work:
```md
- {numref}`fun-fish`
```
output:
- {numref}`fun-fish`

...
