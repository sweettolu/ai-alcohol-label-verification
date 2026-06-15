import re

SPIRIT_KEYWORDS = [
    "whiskey", "bourbon", "vodka", "gin", "rum", "tequila",
    "mezcal", "brandy", "cognac", "liqueur", "scotch", "reposado",
    "anejo", "blanco"
]

GOV_WARNING_PHRASE = "GOVERNMENT WARNING"


def parse_label(text_list):
    result = {
        "brand": None,
        "class": None,
        "alcohol": None,
        "net_contents": None,
        "government_warning": False
    }

    cleaned = [t.strip() for t in text_list if t and t.strip()]
    full_text = " ".join(cleaned)
    full_text_lower = full_text.lower()

    alcohol_match = re.search(
        r"(\d+(\.\d+)?)\s*%|(\d+(\.\d+)?)\s*proof",
        full_text,
        re.IGNORECASE
    )
    if alcohol_match:
        result["alcohol"] = alcohol_match.group(1) + "%" if alcohol_match.group(1) else alcohol_match.group(3) + " proof"

    net_match = re.search(
        r"(\d+(\.\d+)?)\s*(ml|mL|ML|l|L|oz|OZ|fl oz)",
        full_text,
        re.IGNORECASE
    )
    if net_match:
        result["net_contents"] = net_match.group(0)

    result["government_warning"] = GOV_WARNING_PHRASE.lower() in full_text_lower

    class_candidates = []
    for line in cleaned:
        if any(keyword in line.lower() for keyword in SPIRIT_KEYWORDS):
            class_candidates.append(line)

    if class_candidates:
        result["class"] = " ".join(class_candidates)

    brand_candidates = []
    for line in cleaned:
        lower = line.lower()

        if result["class"] and line in result["class"]:
            continue
        if "%" in line or "proof" in lower:
            continue
        if re.search(r"\d+\s*(ml|mL|ML|l|L|oz|OZ)", line):
            continue
        if "government warning" in lower:
            continue

        brand_candidates.append(line)

    if brand_candidates:
        result["brand"] = brand_candidates[0]
    elif cleaned:
        result["brand"] = cleaned[0]

    if not result["class"] and len(cleaned) > 1:
        result["class"] = cleaned[1]

    return result