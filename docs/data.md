# Data: MIMIC-IV Clinical Database Demo on FHIR

## Source and licence

- Dataset: MIMIC-IV Clinical Database Demo on FHIR, version 2.1.0, on PhysioNet: https://physionet.org/content/mimic-iv-fhir-demo/2.1.0/
- Content: 100 randomly selected patients from MIMIC-IV, plus the MIMIC-IV-ED demo data, converted to HL7 FHIR R4. Dates are shifted by the dataset authors (so years such as 2133 are normal).
- Licence: ODC Open Database License v1.0 (ODbL). The demo is open, with no credentialing. The raw files are not committed to this repo (`data/` is gitignored); `scripts/download_data.sh` fetches them and checks every file against the published `SHA256SUMS.txt`.
- This is real, de-identified patient data (it is not synthetic). This project is for research only and is not for clinical use.

Citation (as given on the PhysioNet page):

> Bennett, A., Ulrich, H., Wiedekopf, J., Szul, P., Grimes, J., & Johnson, A. (2025). MIMIC-IV Clinical Database Demo on FHIR (version 2.1.0). PhysioNet. RRID:SCR_007345.

## Format

Each file is NDJSON (newline-delimited JSON): one complete FHIR resource per line, gzip-compressed on the server. `scripts/download_data.sh` unzips them into `data/raw/fhir/`.

## Counts

Everything below is printed by `python -m chartproof.store.inspect` (run after the download). Re-run it to regenerate.

| resourceType | Count |
|---|---|
| Condition | 5051 |
| Encounter | 637 |
| Location | 31 |
| Medication | 1794 |
| MedicationAdministration | 56535 |
| MedicationDispense | 15375 |
| MedicationRequest | 17552 |
| MedicationStatement | 2411 |
| Observation | 813540 |
| Organization | 1 |
| Patient | 100 |
| Procedure | 3450 |
| Specimen | 12458 |
| **Total** | **928935** |

| File | Lines | resourceType |
|---|---|---|
| MimicCondition.ndjson | 4506 | Condition |
| MimicConditionED.ndjson | 545 | Condition |
| MimicEncounter.ndjson | 275 | Encounter |
| MimicEncounterED.ndjson | 222 | Encounter |
| MimicEncounterICU.ndjson | 140 | Encounter |
| MimicLocation.ndjson | 31 | Location |
| MimicMedication.ndjson | 1480 | Medication |
| MimicMedicationAdministration.ndjson | 36131 | MedicationAdministration |
| MimicMedicationAdministrationICU.ndjson | 20404 | MedicationAdministration |
| MimicMedicationDispense.ndjson | 14293 | MedicationDispense |
| MimicMedicationDispenseED.ndjson | 1082 | MedicationDispense |
| MimicMedicationMix.ndjson | 314 | Medication |
| MimicMedicationRequest.ndjson | 17552 | MedicationRequest |
| MimicMedicationStatementED.ndjson | 2411 | MedicationStatement |
| MimicObservationChartevents.ndjson | 668862 | Observation |
| MimicObservationDatetimeevents.ndjson | 15280 | Observation |
| MimicObservationED.ndjson | 2742 | Observation |
| MimicObservationLabevents.ndjson | 107727 | Observation |
| MimicObservationMicroOrg.ndjson | 338 | Observation |
| MimicObservationMicroSusc.ndjson | 1036 | Observation |
| MimicObservationMicroTest.ndjson | 1893 | Observation |
| MimicObservationOutputevents.ndjson | 9362 | Observation |
| MimicObservationVitalSignsED.ndjson | 6300 | Observation |
| MimicOrganization.ndjson | 1 | Organization |
| MimicPatient.ndjson | 100 | Patient |
| MimicProcedure.ndjson | 722 | Procedure |
| MimicProcedureED.ndjson | 1260 | Procedure |
| MimicProcedureICU.ndjson | 1468 | Procedure |
| MimicSpecimen.ndjson | 1336 | Specimen |
| MimicSpecimenLab.ndjson | 11122 | Specimen |

| File | Reference field | Points to |
|---|---|---|
| MimicCondition.ndjson | encounter | Encounter |
| MimicCondition.ndjson | subject | Patient |
| MimicConditionED.ndjson | encounter | Encounter |
| MimicConditionED.ndjson | subject | Patient |
| MimicEncounter.ndjson | identifier.assigner | Organization |
| MimicEncounter.ndjson | location.location | Location |
| MimicEncounter.ndjson | serviceProvider | Organization |
| MimicEncounter.ndjson | subject | Patient |
| MimicEncounterED.ndjson | identifier.assigner | Organization |
| MimicEncounterED.ndjson | partOf | Encounter |
| MimicEncounterED.ndjson | serviceProvider | Organization |
| MimicEncounterED.ndjson | subject | Patient |
| MimicEncounterICU.ndjson | location.location | Location |
| MimicEncounterICU.ndjson | partOf | Encounter |
| MimicEncounterICU.ndjson | subject | Patient |
| MimicLocation.ndjson | managingOrganization | Organization |
| MimicMedicationAdministration.ndjson | context | Encounter |
| MimicMedicationAdministration.ndjson | request | MedicationRequest |
| MimicMedicationAdministration.ndjson | subject | Patient |
| MimicMedicationAdministrationICU.ndjson | context | Encounter |
| MimicMedicationAdministrationICU.ndjson | subject | Patient |
| MimicMedicationDispense.ndjson | authorizingPrescription | MedicationRequest |
| MimicMedicationDispense.ndjson | context | Encounter |
| MimicMedicationDispense.ndjson | subject | Patient |
| MimicMedicationDispenseED.ndjson | context | Encounter |
| MimicMedicationDispenseED.ndjson | subject | Patient |
| MimicMedicationMix.ndjson | ingredient.itemReference | Medication |
| MimicMedicationRequest.ndjson | encounter | Encounter |
| MimicMedicationRequest.ndjson | medicationReference | Medication |
| MimicMedicationRequest.ndjson | subject | Patient |
| MimicMedicationStatementED.ndjson | context | Encounter |
| MimicMedicationStatementED.ndjson | subject | Patient |
| MimicObservationChartevents.ndjson | encounter | Encounter |
| MimicObservationChartevents.ndjson | subject | Patient |
| MimicObservationDatetimeevents.ndjson | encounter | Encounter |
| MimicObservationDatetimeevents.ndjson | subject | Patient |
| MimicObservationED.ndjson | encounter | Encounter |
| MimicObservationED.ndjson | partOf | Procedure |
| MimicObservationED.ndjson | subject | Patient |
| MimicObservationLabevents.ndjson | encounter | Encounter |
| MimicObservationLabevents.ndjson | specimen | Specimen |
| MimicObservationLabevents.ndjson | subject | Patient |
| MimicObservationMicroOrg.ndjson | derivedFrom | Observation |
| MimicObservationMicroOrg.ndjson | hasMember | Observation |
| MimicObservationMicroOrg.ndjson | subject | Patient |
| MimicObservationMicroSusc.ndjson | derivedFrom | Observation |
| MimicObservationMicroSusc.ndjson | subject | Patient |
| MimicObservationMicroTest.ndjson | encounter | Encounter |
| MimicObservationMicroTest.ndjson | hasMember | Observation |
| MimicObservationMicroTest.ndjson | specimen | Specimen |
| MimicObservationMicroTest.ndjson | subject | Patient |
| MimicObservationOutputevents.ndjson | encounter | Encounter |
| MimicObservationOutputevents.ndjson | subject | Patient |
| MimicObservationVitalSignsED.ndjson | encounter | Encounter |
| MimicObservationVitalSignsED.ndjson | partOf | Procedure |
| MimicObservationVitalSignsED.ndjson | subject | Patient |
| MimicPatient.ndjson | managingOrganization | Organization |
| MimicProcedure.ndjson | encounter | Encounter |
| MimicProcedure.ndjson | subject | Patient |
| MimicProcedureED.ndjson | encounter | Encounter |
| MimicProcedureED.ndjson | subject | Patient |
| MimicProcedureICU.ndjson | encounter | Encounter |
| MimicProcedureICU.ndjson | subject | Patient |
| MimicSpecimen.ndjson | subject | Patient |
| MimicSpecimenLab.ndjson | subject | Patient |

Patients: 100

## How resources link to a patient

Almost every resource points to its patient with a `subject` reference (`Patient/<id>`). Some links go through other resources:

- **Encounter**: most clinical resources also point to an Encounter. Observation, Condition, Procedure and MedicationRequest use `encounter`. MedicationAdministration, MedicationDispense and MedicationStatement use `context` for the same thing.
- **Medication has no patient link.** `Medication` (and `MedicationMix`, whose `ingredient.itemReference` points to other Medications) has no `subject`. It is reached from a patient through `MedicationRequest.medicationReference`.
- **MedicationRequest chain**: MedicationAdministration `request` and MedicationDispense `authorizingPrescription` both point back to a MedicationRequest.
- **Microbiology chain**: `MimicObservationMicroTest` (has `subject`, `encounter`, `specimen`) points to other Observations through `hasMember`. `MicroOrg` and `MicroSusc` use `hasMember` and `derivedFrom` to point to other Observations. Both have a `subject` but no `encounter`.
- **Lab results**: `MimicObservationLabevents` points to a Specimen through `specimen`.
- **ED observations** (`MimicObservationED`, `MimicObservationVitalSignsED`) can point to a Procedure through `partOf`.
- **Not patient-specific**: `Organization` (1 resource) and `Location` (31 resources) are shared across patients.

A patient's data can be found by searching `subject = Patient/<id>`, except for Medication, MedicationMix, Organization and Location, which need a reference hop.

## Notes for later phases

- The nine "Observation" files hold different kinds of data (chart events, datetime events, lab events, output events, microbiology, ED). They all share `resourceType` Observation. The source table is recorded in `meta.profile` (for example `.../mimic-observation-chartevents`), which the benchmark's `main_table_name` likely corresponds to. Phase 4 keeps `meta` in the stored JSON for that reason, even though the client strips it from results.
- Several files hold the same `resourceType` (for example Condition and ConditionED), so a resource is identified by `(type, id)` and not by file.

## Local SQLite store

`make db` (or `python -m chartproof.store.build`) loads every resource into `data/fhir.sqlite`, which is gitignored. It takes under a minute and the per-type counts match the table above.

- `resources(id, type, patient_id, encounter_id, effective_time, effective_field, json)`, primary key `(type, id)`. `json` is the original line, unchanged, so `meta` is kept.
- `refs(src_type, src_id, field, dst_type, dst_id)` holds every reference found anywhere in a resource, using the same field paths as the inspect script. Every reference in the demo resolves to a stored resource.
- Indexes: `(type, patient_id)`, `(encounter_id)`, `(effective_time)` on `resources`, and `(src_type, src_id)` and `(dst_type, dst_id)` on `refs`.
- `patient_id` comes from `subject` or `patient`. A Patient is its own patient. `Medication`, `Location` and `Organization` have none.
- `encounter_id` comes from `encounter` or `context`.
- `effective_time` is the first present of: `effectiveDateTime`, `issued`, `authoredOn`, `period.start`, `effectivePeriod.start` (the plan's five), then `performedDateTime`, `performedPeriod.start`, `collection.collectedDateTime`, `whenHandedOver`, `dateAsserted` (added because Procedure, Specimen, MedicationDispense and MedicationStatement have none of the first five). `effective_field` records which one was used.
- `Condition` resources have no time of their own, so `effective_time` is NULL. Their time has to come from their encounter. Most `MedicationDispense` resources are the same.
