"""Test practice_dwh.handler module."""

import logging

from practice_dwh.handler import PracticeDwhHandler


def test_run(caplog):
    """Test `run()` method in PracticeDwhHandler."""
    caplog.set_level(logging.INFO)
    name = "E. Dijkstra"
    handler = PracticeDwhHandler(name)
    handler.run()

    assert name in caplog.text
