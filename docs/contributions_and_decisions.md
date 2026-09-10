# Contribution and decision record

Scope: Maximus Turner, GitHub vfbmdcccxciii. The starting repository commit was 31df8502da9303334809647af27369c3b0842c93. Git history attributes the revised source scripts, original result CSVs and README content to Max Turner. This revision changes only those contributions and adds new supporting files. Other contributors' code, uploaded data and presentation are unchanged.

## Decisions on 10 September 2026

- Follow the user-reported agreement of two questions per person. Retain the running comparison and replace the other three active prototypes with one pressing-composition question.
- Preserve the original eight numerical output CSVs unchanged under archive/2026-08-31. Original scripts remain accessible in Git history at the starting commit. Archived results refer to the earlier, incomplete minutes capture and are superseded, not current evidence.
- Repair 281 missing minute records from the visible official table without modifying the original dated snapshot. The new sample outputs therefore differ from the original running sample even though the positional seeds remain 2026 and 2027.
- Prefer the Week 4 conservative degrees of freedom for the primary test. Keep software Welch results as a labelled sensitivity check.
- Retain unsuccessful exploratory comparisons in the record. Old shooting p=0.5090, passing p=0.2443, forced-turnovers-per-90 p=0.5607 (Welch). An explored turnovers-per-100-pressures alternative had course p about 0.6347 before the source repair. Direct-pressure share was selected after exploration. No p-values are described as prespecified confirmatory findings.
- Provide a four-slide narrated segment and two optional reference slides. Use Python for all data visualisations, with editable PowerPoint text. Include discussion notes and source references.

This is a record of decisions made during this revision, not evidence that group discussions or peer reviews occurred. The user reported communicating the two-question allocation. Actual collaboration evidence belongs in the required Teams space. No messages were posted on the user's behalf.

## Reproduction and checks

Run python src/run_max_analysis.py, then python -m unittest discover -s tests -v. Tests independently check the t statistic against SciPy, conservative degrees of freedom and p-value, confidence-interval behaviour, invalid input, source-key uniqueness, seed reproducibility and required sampling counts. Coverage outputs expose unmatched records. Git diff checks protect other contributors' tracked files.

Tested analysis environment: Python 3.12, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.1, seaborn 0.13.2. requirements.txt records the directly used libraries. Jupyter remains optional rather than a required dependency.
