<a id="тестовый-реплей"></a>
# Replay fixture

**English** · [Русский](README.md)

`real_anonymized.rep` is a complete replay created by Cossacks 3 build
2.0.0.1199, not an artificial binary sample. Player names and account
identifiers were replaced with same-length placeholders by
[`scripts/anonymize_replay_fixture.py`](../../../scripts/anonymize_replay_fixture.py).
The offsets and event bytes therefore retain the structure of a real file.

The replay contains a short two-player match on a tiny map. Its expected
metadata and event summary are asserted in `tests/test_replay_metadata.py`.
