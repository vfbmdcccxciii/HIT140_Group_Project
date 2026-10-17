"""Reproduce everything: python src/run_all.py  (add --fetch to re-download raw sources first;
by default the committed snapshots in data/raw are used so results are reproducible)."""
import sys
import prepare_data, eda, model_2_1, model_2_2, compare_models
if "--fetch" in sys.argv:
    import fetch_sources; fetch_sources.main()
prepare_data.main(); model_2_1.main(); model_2_2.main(); eda.main(); compare_models.main()
