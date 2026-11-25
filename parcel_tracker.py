"""Courier and parcel tracking system."""

import secrets
import shutil
import subprocess  # nosec B404 - only used in ping_hub, no shell, list args
import tempfile
from datetime import date

STATUS_FLOW = ["Booked", "Picked Up", "In Transit",
               "Out for Delivery", "Delivered"]
parcels = {}


def book_parcel(sender, receiver, weight_kg, history=None):
    """Book a parcel and return its tracking id."""
    tracking_id = "TRK" + str(10001 + len(parcels))
    parcels[tracking_id] = {"sender": sender, "receiver": receiver,
                            "weight": weight_kg, "status": 0,
                            "booked": str(date.today())}
    if history is not None:
        history.append(tracking_id)
    return tracking_id


def advance_status(tracking_id):
    """Move a parcel to the next delivery stage and return that stage."""
    parcel = parcels[tracking_id]
    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1
    return STATUS_FLOW[parcel["status"]]


def shipping_cost(weight_kg):
    """Return the shipping cost for a parcel of the given weight."""
    cost = 50
    if weight_kg > 1:
        cost += (weight_kg - 1) * 30
    return round(cost, 2)


def track_parcel(tracking_id):
    """Return the route and current status of a parcel."""
    try:
        parcel = parcels[tracking_id]
    except KeyError:
        return "Unknown tracking id " + tracking_id
    route = parcel["sender"] + " -> " + parcel["receiver"]
    return route + ": " + STATUS_FLOW[parcel["status"]]


def is_with_courier(tracking_id):
    """Return True if the parcel is picked up or in transit."""
    status = STATUS_FLOW[parcels[tracking_id]["status"]]
    return status in ("Picked Up", "In Transit")


def label_path():
    """Create an empty label file and return its path."""
    # Helper kept for the lab: not called by the demo
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as label:
        return label.name


def ping_hub(hub_address):
    """Ping a hub once and return the ping output."""
    # Helper kept for the lab: not called by the demo
    ping = shutil.which("ping")
    if ping is None:
        raise FileNotFoundError("ping command not found")
    if hub_address.startswith("-"):
        raise ValueError("Invalid hub address: " + hub_address)
    # Absolute path, list of arguments and no shell, so the address can
    # never be run as a command.
    command = [ping, "-c", "1", hub_address]
    return subprocess.check_output(command)  # nosec B603


def main():
    """Run a short demonstration of the parcel tracker."""
    first = book_parcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = book_parcel("Gadget Hub", "Sneha Rao", 0.8)
    third = book_parcel("Spice Store", "Imran Khan", 4)
    advance_status(first)
    advance_status(first)
    advance_status(second)
    for _ in range(6):
        advance_status(third)
    for tracking_id in (first, second, third):
        print(track_parcel(tracking_id))
        print("  with courier:", is_with_courier(tracking_id))
        print("  cost:", shipping_cost(parcels[tracking_id]["weight"]))
    print(track_parcel("TRK00000"))  # unknown id
    delivery_otp = secrets.randbelow(9000) + 1000
    print("Delivery OTP for", third, "is", delivery_otp)
    print("Parcels booked today:", len(parcels))


if __name__ == "__main__":
    main()
