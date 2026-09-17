# Code for chapter 3

Fork of [maxpumperla/deep_learning_and_the_game_of_go](https://github.com/maxpumperla/deep_learning_and_the_game_of_go),
chapter 3 branch, updated for modern Python (3.9+).

## Quickstart

```sh
cd code
python3 -m venv .venv && source .venv/bin/activate
pip install -e .          # no third-party dependencies in chapter 3

python bot_v_bot.py       # two random bots play a 9x9 game
python human_v_bot.py     # you (black) vs a random bot; enter moves like D4
python -m unittest discover -p '*_test.py'
```

`dlgo/goboard_slow.py` is the naive board from the start of the chapter;
`dlgo/goboard.py` is the fast board with immutable strings and Zobrist hashing
that both scripts use.

## Changes against upstream

- `Board.__eq__` called `self._hash()` on an int, so comparing two boards raised
  `TypeError`; it now compares the Zobrist hashes and `Board` defines `__hash__`.
- `Board.place_stone` built the new `GoString` twice.
- `RandomBot` imported `Move` from `goboard_slow` while the scripts now run the
  fast board; both use `dlgo.goboard`.
- Dropped Python 2 leftovers: `six`, `from __future__ import ...`, unused
  `numpy` imports, and the committed `dlgo/goboard.pyc`.
- `human_v_bot.py` re-prompts on typos and illegal moves instead of dying on an
  assertion; both scripts print the winner.
- `goboard_slow.GameState` gained `winner()` so it stays swappable with the fast
  board.
- `generate_zobrist.py` emitted `Player.black` via `%s` on the enum object; it
  now writes the literal.
- Packaging: `setup.py` (which pulled in `gomill`, a Python 2-only package, plus
  TensorFlow/Keras that chapter 3 never imports) replaced by `pyproject.toml`
  with no dependencies.
- Tests: added regressions for board equality and for the ko rule.
