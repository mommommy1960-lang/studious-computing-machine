"""Simulation-only preregistered experiment records."""
from __future__ import annotations
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from enum import Enum

class EvidenceLevel(str, Enum):
    HYPOTHESIS = "hypothesis"
    SIMULATION = "simulation"
    REPLICATED_SIMULATION = "replicated-simulation"

@dataclass(frozen=True)
class Experiment:
    experiment_id: str
    question: str
    method: str
    seed: int
    inputs: tuple[float, ...]
    evidence: EvidenceLevel = EvidenceLevel.HYPOTHESIS

class ExperimentRegistry:
    def __init__(self):
        self._registered: dict[str, tuple[Experiment, str]] = {}
        self._results: dict[str, dict] = {}

    def preregister(self, experiment: Experiment) -> str:
        if not experiment.experiment_id or not experiment.question or not experiment.method:
            raise ValueError("identity, question, and method are required")
        if experiment.experiment_id in self._registered:
            raise ValueError("duplicate experiment identifier")
        if not all(math.isfinite(value) for value in experiment.inputs):
            raise ValueError("inputs must be finite")
        canonical=json.dumps(asdict(experiment),sort_keys=True,separators=(",",":"),default=str)
        digest=hashlib.sha256(canonical.encode()).hexdigest()
        self._registered[experiment.experiment_id]=(experiment,digest)
        return digest

    def record(self, experiment_id: str, *, preregistration_hash: str,
               outputs: tuple[float, ...], evidence: EvidenceLevel) -> dict:
        entry=self._registered.get(experiment_id)
        if entry is None or entry[1] != preregistration_hash:
            raise PermissionError("result does not match preregistration")
        if evidence is EvidenceLevel.HYPOTHESIS:
            raise ValueError("results require simulation evidence")
        if not outputs or not all(math.isfinite(value) for value in outputs):
            raise ValueError("outputs must be nonempty and finite")
        record={"experiment_id":experiment_id,"preregistration_hash":preregistration_hash,
                "outputs":outputs,"evidence":evidence.value,
                "claim":"simulation result; not empirical or physical validation"}
        self._results[experiment_id]=record
        return record

    def result(self, experiment_id: str):
        return self._results.get(experiment_id)
