from app.services.parser_service import parse_label

sample = [
    "OLD TOM DISTILLERY",
    "Kentucky Straight Bourbon Whiskey",
    "45% Alc./Vol.",
    "750 mL"
]

print(parse_label(sample))