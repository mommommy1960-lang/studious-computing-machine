# Studious Computing Machine

## Navigation-constrained hypothetical superluminal research

This repository is a **simulation-only research prototype** for studying navigation precision, control stability, and survivability in hypothetical curved-spacetime models.

It does not claim that faster-than-light travel is achievable. It supplies no propulsion design, hardware control, experimental-physics result, or evidence of physical feasibility. Negative-energy requirements and other foundational physics questions remain unresolved.

## What is implemented

The `research_core` package provides an authority-free experiment registry that:

- preregisters a question, method, seed, and finite input set;
- binds each registration to a deterministic SHA-256 digest;
- rejects duplicate experiment identifiers;
- rejects results that do not match the preregistration;
- rejects non-finite inputs and outputs;
- distinguishes hypothesis, simulation, and replicated-simulation evidence;
- labels every result as simulation rather than empirical validation.

## Verification

The packaged tests cover successful preregistration and recording, wrong-hash denial, duplicate-ID rejection, and NaN/infinity rejection.

Local dependency-free smoke/adversarial verification passed on 2026-09-07. Hosted GitHub verification has not run because the account-level Actions runner is blocked by a billing lock. This draft must remain unmerged until hosted jobs execute and provide replayable logs.

## Research and release boundary

See [RESEARCH_BOUNDARY.md](RESEARCH_BOUNDARY.md) for the claim boundary. This repository is **pre-release**, **not production-ready**, and **not approved for sale or deployment**.
