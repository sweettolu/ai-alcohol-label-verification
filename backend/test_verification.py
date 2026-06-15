from app.services.verification_service import verify_label

expected = {
    "brand": "OLD TOM DISTILLERY",
    "class": "Kentucky Straight Bourbon Whiskey",
    "alcohol": "45%",
    "net_contents": "750 mL"
}

actual = {
    "brand": "Old Tom Distillery",
    "class": "Kentucky Straight Bourbon Whiskey",
    "alcohol": "45%",
    "net_contents": "750 mL"
}

result = verify_label(expected, actual)

print(result)