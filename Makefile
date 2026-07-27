# Thin wrapper around scripts/regen.py — same targets, available where `make` is.
# All target lists live in scripts/regen.py to keep one source of truth.
PY := python

.PHONY: all data reference reports reports-combat reports-economy reports-map \
        reports-nations tech derived simulations diff sanity help

all:
	$(PY) scripts/regen.py all

data:
	$(PY) scripts/regen.py data

reference:
	$(PY) scripts/regen.py reference

reports:
	$(PY) scripts/regen.py reports

reports-combat:
	$(PY) scripts/regen.py reports-combat

reports-economy:
	$(PY) scripts/regen.py reports-economy

reports-map:
	$(PY) scripts/regen.py reports-map

reports-nations:
	$(PY) scripts/regen.py reports-nations

tech:
	$(PY) scripts/regen.py tech

derived:
	$(PY) scripts/regen.py derived

simulations:
	$(PY) scripts/regen.py simulations

# Snapshot diff: keep current data.json as old, regen, diff against new.
diff:
	cp data.json /tmp/data_old.json
	$(PY) parser/build_data.py
	$(PY) writers/diff_snapshots.py /tmp/data_old.json data.json --out diff.md

# Run parser, fail if any sanity check regresses.
sanity:
	$(PY) scripts/regen.py sanity

help:
	$(PY) scripts/regen.py help
