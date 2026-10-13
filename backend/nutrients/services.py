from django.utils import timezone

from labs.models import LabResult
from profiles.models import HealthProfile, Symptom
from .models import Nutrient, NutrientStatus

RULES = {
    "Ferritin": "Iron",
    "Iron": "Iron",
    "Vitamin B12": "Vitamin B12",
    "Vitamin D": "Vitamin D",
    "Folate": "Folate",
}
GENERAL_LIMITATIONS = [
    "This is a preliminary comparison using the reference range recorded for this laboratory report.",
    "This is not a medical diagnosis. Discuss concerning results with a qualified healthcare professional.",
]


def assess_user_nutrients(user):
    profile_exists = HealthProfile.objects.filter(user=user).exists()
    symptoms = list(Symptom.objects.filter(user=user).values("name", "severity", "frequency"))
    results = LabResult.objects.filter(lab_report__user=user, biomarker__in=RULES).select_related("lab_report").order_by("-lab_report__test_date", "-created_at")
    grouped = {name: [] for name in set(RULES.values())}
    for result in results:
        grouped[RULES[result.biomarker]].append(result)

    response = []
    for nutrient_name, nutrient_results in grouped.items():
        nutrient, _ = Nutrient.objects.get_or_create(name=nutrient_name)
        evidence = []
        has_range = False
        outside_range = False
        for result in nutrient_results:
            low, high = result.reference_low, result.reference_high
            observation = {"type": "lab_result", "biomarker": result.biomarker, "value": str(result.value), "unit": result.unit, "reference_low": str(low) if low is not None else None, "reference_high": str(high) if high is not None else None, "test_date": result.lab_report.test_date.isoformat()}
            if low is not None or high is not None:
                has_range = True
                if low is not None and result.value < low:
                    observation["comparison"] = "below_recorded_reference_range"; outside_range = True
                elif high is not None and result.value > high:
                    observation["comparison"] = "above_recorded_reference_range"; outside_range = True
                else:
                    observation["comparison"] = "within_recorded_reference_range"
            evidence.append(observation)
        if outside_range:
            status = NutrientStatus.Status.POTENTIAL_CONCERN
            limitations = GENERAL_LIMITATIONS
        elif has_range:
            status = NutrientStatus.Status.NO_FLAG
            limitations = ["No flag was found from the available laboratory reference ranges. This does not confirm adequacy or rule out other health concerns."] + GENERAL_LIMITATIONS[1:]
        else:
            status = NutrientStatus.Status.INSUFFICIENT_DATA
            limitations = ["No usable laboratory reference range was available for this nutrient mapping."] + GENERAL_LIMITATIONS[1:]
        if not nutrient_results:
            limitations = ["No relevant laboratory result is available for this assessment.", GENERAL_LIMITATIONS[1:]]
        if symptoms:
            limitations.append("Recorded symptoms are shown as context only and are not used to diagnose a nutrient condition.")
        status_record, _ = NutrientStatus.objects.update_or_create(user=user, nutrient=nutrient, defaults={"status": status, "evidence": evidence, "limitations": limitations})
        response.append({"nutrient": nutrient.name, "status": status_record.status, "evidence": evidence, "limitations": limitations})
    return {"assessed_at": timezone.now(), "profile_available": profile_exists, "symptoms_recorded": len(symptoms), "results": response}
