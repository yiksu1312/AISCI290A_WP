"""Create the initial exploration notebook once, without overwriting existing work."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
cells = []


def cell(kind, source):
    item = {"cell_type": kind, "metadata": {}, "source": source.splitlines(keepends=True)}
    if kind == "code":
        item.update(execution_count=None, outputs=[])
    cells.append(item)


cell("markdown", """# Weather near Irvine: initial data audit

**Research question:** Can recent local weather improve next-day temperature predictions near Irvine compared with persistence?

This notebook inspects the supplied ERA5 subset and generates 2009 exploratory figures. It does not fit models or evaluate the reserved future period. A grid point near Irvine is not a station observation.
""")
cell("code", """from pathlib import Path
import sys
ROOT = Path.cwd()
if ROOT.name == 'notebooks':
    ROOT = ROOT.parent
assert (ROOT / 'scripts/audit_data.py').exists(), 'Run from the project or notebooks folder'
sys.path.insert(0, str(ROOT / 'scripts'))
from audit_data import audit
from make_exploration import make_figures
print(sys.executable)
""")
cell("code", """report, daily = audit(ROOT / 'data/data', ROOT / 'data/processed')
report['summary']
""")
cell("code", """# Source units and processing attributes, not assumptions from filenames.
{name: meta['attributes'] for name, meta in report['files'][0]['variables'].items()}
""")
cell("code", """daily.loc['2009'].head()
""")
cell("markdown", """## Trailing features and maps

Daily continuity and variable alignment are checked before rolling windows.
Trailing 3-day and 7-day means include today, never future observations.
Temperature is converted from verified Kelvin units to Celsius. Precipitation stays in source units until its daily aggregation is resolved; it is not labeled mm/day.
""")
cell("code", """make_figures(ROOT)
from IPython.display import Image, display
for name in ['t2m_2009_first_day.png', 'tp_2009_first_day.png', 'irvine_2009_rolling.png']:
    display(Image(filename=str(ROOT / 'reports/figures' / name)))
""")
cell("markdown", """## Next steps

- Confirm precipitation aggregation and the selected point's land status.
- Define chronological train/validation/test boundaries by target date; discuss seasonal limitations with Daniel.
- Compare persistence, temperature-only regression, and expanded regression on identical validation dates using MAE and RMSE.
- Keep all learned preprocessing training-only and final test outcomes untouched.
- Predict after today's daily values are available. A shift(-1) target is safe only after the daily checks above.

No progress-report slot or duration has been confirmed; October 27, 2026 is the planned Tuesday.
""")
nb = {"cells": cells, "metadata": {
    "kernelspec": {"display_name": "Python (290A Weather)", "language": "python", "name": "aisci290a"},
    "language_info": {"name": "python", "version": "3.12"}}, "nbformat": 4, "nbformat_minor": 4}
target = root / 'notebooks/01_data_audit.ipynb'
with target.open('x', encoding='utf-8') as handle:
    json.dump(nb, handle, indent=2)
print(target)
