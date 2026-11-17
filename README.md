# chartproof

A FHIR patient-record agent that answers clinical questions, cites the exact records it used, and has a verifier that rejects any answer the cited records don't support. It is evaluated on FHIR-AgentBench using free-tier models and a local on-device model.

Status: work in progress.

## Attribution

- Questions and the reference agent come from FHIR-AgentBench (Lee et al., 2025), https://github.com/glee4810/FHIR-AgentBench, licensed CC BY 4.0. The benchmark is cloned into `vendor/` at a pinned commit by `scripts/fetch_benchmark.sh` and is never modified or redistributed here. Only question IDs are saved in `results/splits/`.
- Patient data is the MIMIC-IV Clinical Database Demo on FHIR v2.1.0 (Bennett et al., 2025, PhysioNet), licensed ODbL v1.0. It is downloaded locally and never committed. See `docs/data.md`.

Citation for the benchmark:

> Gyubok Lee, Elea Bach, Eric Yang, Tom Pollard, Alistair Johnson, Edward Choi, Yugang Jia, Jong Ha Lee. FHIR-AgentBench: Benchmarking LLM Agents for Realistic Interoperable EHR Question Answering. arXiv:2509.19319, 2025.
