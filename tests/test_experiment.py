import math
import pytest
from research_core import Experiment, ExperimentRegistry, EvidenceLevel

def sample():
    return Experiment("e1","Does the toy model remain bounded?","deterministic sweep",7,(0.1,0.2))

def test_preregister_then_record():
    r=ExperimentRegistry(); h=r.preregister(sample())
    result=r.record("e1",preregistration_hash=h,outputs=(1.0,),evidence=EvidenceLevel.SIMULATION)
    assert result["claim"] == "simulation result; not empirical or physical validation"

def test_wrong_hash_denied():
    r=ExperimentRegistry(); r.preregister(sample())
    with pytest.raises(PermissionError):
        r.record("e1",preregistration_hash="wrong",outputs=(1,),evidence=EvidenceLevel.SIMULATION)

def test_duplicate_id_rejected():
    r=ExperimentRegistry(); r.preregister(sample())
    with pytest.raises(ValueError): r.preregister(sample())

@pytest.mark.parametrize("value",[math.nan,math.inf,-math.inf])
def test_nonfinite_inputs_and_outputs_rejected(value):
    r=ExperimentRegistry()
    with pytest.raises(ValueError):
        r.preregister(Experiment("bad","q","m",1,(value,)))
    h=r.preregister(sample())
    with pytest.raises(ValueError):
        r.record("e1",preregistration_hash=h,outputs=(value,),evidence=EvidenceLevel.SIMULATION)
