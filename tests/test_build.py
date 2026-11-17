from chartproof.store.build import to_rows


def row(resource: dict):
    return to_rows(resource, "{}")


def test_observation_gets_patient_encounter_time_and_refs():
    obs = {
        "resourceType": "Observation",
        "id": "o1",
        "subject": {"reference": "Patient/p1"},
        "encounter": {"reference": "Encounter/e1"},
        "specimen": {"reference": "Specimen/s1"},
        "issued": "2180-01-02T00:00:00",
        "effectiveDateTime": "2180-01-01T10:00:00",
    }
    (rid, rtype, patient, encounter, when, field, _), refs = row(obs)
    assert (rid, rtype, patient, encounter) == ("o1", "Observation", "p1", "e1")
    assert (when, field) == ("2180-01-01T10:00:00", "effectiveDateTime")  # not `issued`
    assert ("Observation", "o1", "specimen", "Specimen", "s1") in refs
    assert len(refs) == 3


def test_patient_is_its_own_patient():
    (_, _, patient, encounter, when, _, _), refs = row({"resourceType": "Patient", "id": "p1"})
    assert (patient, encounter, when, refs) == ("p1", None, None, [])


def test_context_counts_as_encounter_and_nested_time_fields_work():
    admin = {
        "resourceType": "MedicationAdministration",
        "id": "m1",
        "subject": {"reference": "Patient/p1"},
        "context": {"reference": "Encounter/e1"},
        "effectivePeriod": {"start": "2180-03-01T00:00:00"},
    }
    (_, _, _, encounter, when, field, _), _ = row(admin)
    assert (encounter, when, field) == ("e1", "2180-03-01T00:00:00", "effectivePeriod.start")


def test_medication_has_no_patient_and_keeps_its_own_references():
    med = {
        "resourceType": "Medication",
        "id": "d1",
        "ingredient": [{"itemReference": {"reference": "Medication/d2"}}],
    }
    (_, _, patient, _, when, _, _), refs = row(med)
    assert patient is None and when is None
    assert refs == [("Medication", "d1", "ingredient.itemReference", "Medication", "d2")]
