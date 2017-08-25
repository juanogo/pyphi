import pytest
import numpy as np

from pyphi.constants import Direction
from pyphi.compute import concept_cuts, ConceptStyleSystem
from pyphi.models import KCut, KPartition, Part


@pytest.fixture()
def kcut():
    return KCut(KPartition(Part((0, 2), (0,)), Part((), (2,)), Part((3,), (3,))))


def test_cut_indices(kcut):
    assert kcut.indices == (0, 2, 3)


def test_apply_cut(kcut):
    cm = np.ones((4, 4))
    cut_cm = np.array([
        [1, 1, 1, 0],
        [1, 1, 1, 1],
        [0, 1, 0, 0],
        [0, 1, 0, 1]])
    assert np.array_equal(kcut.apply_cut(cm), cut_cm)


def test_cut_matrix(kcut):
    assert np.array_equal(kcut.cut_matrix(4), np.array([
        [0, 0, 0, 1],
        [0, 0, 0, 0],
        [1, 0, 1, 1],
        [1, 0, 1, 0]]))


def test_splits_mechanism(kcut):
    assert kcut.splits_mechanism((0, 3))
    assert kcut.splits_mechanism((2, 3))
    assert not kcut.splits_mechanism((0,))
    assert not kcut.splits_mechanism((3,))


def test_all_cut_mechanisms(kcut):
    assert kcut.all_cut_mechanisms() == (
        (2,), (0, 2), (0, 3), (2, 3), (0, 2, 3))


def test_system_accessors(s):
    cut = KCut(KPartition(Part((0, 2), (0, 1)), Part((1,), (2,))))

    cs_past = ConceptStyleSystem(s, Direction.PAST, cut)
    assert cs_past.cause_system.cut == cut
    assert cs_past.effect_system.cut == s.null_cut

    cs_future = ConceptStyleSystem(s, Direction.FUTURE, cut)
    assert cs_future.cause_system.cut == s.null_cut
    assert cs_future.effect_system.cut == cut
