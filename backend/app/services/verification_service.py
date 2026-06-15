from rapidfuzz import fuzz


def compare(expected, actual, threshold=90):
    if expected is None or actual is None:
        return {
            "expected": expected,
            "actual": actual,
            "score": 0,
            "status": "FAIL"
        }

    score = fuzz.ratio(expected.lower(), actual.lower())

    return {
        "expected": expected,
        "actual": actual,
        "score": score,
        "status": "PASS" if score >= threshold else "FAIL"
    }


def verify_boolean(field_name, actual):
    return {
        "expected": "Present",
        "actual": "Present" if actual else "Missing",
        "score": 100 if actual else 0,
        "status": "PASS" if actual else "FAIL"
    }


def verify_label(expected_data, extracted_data):
    results = {
        "brand": compare(expected_data.get("brand"), extracted_data.get("brand")),
        "class": compare(expected_data.get("class"), extracted_data.get("class")),
        "alcohol": compare(expected_data.get("alcohol"), extracted_data.get("alcohol")),
        "net_contents": compare(expected_data.get("net_contents"), extracted_data.get("net_contents")),
        "government_warning": verify_boolean(
            "government_warning",
            extracted_data.get("government_warning")
        )
    }

    overall = "PASS"
    for value in results.values():
        if value["status"] == "FAIL":
            overall = "MANUAL_REVIEW"

    return {
        "overall": overall,
        "results": results
    }