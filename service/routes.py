"""Controller for the Account REST API Service."""
from flask import jsonify, url_for, abort, request
from service import app
from service.common import status

COUNTER = {}
ACCOUNTS = {}
NEXT_ACCOUNT_ID = 1


@app.route("/health")
def health():
    """Health status."""
    return jsonify(status="OK"), status.HTTP_200_OK


@app.route("/")
def index():
    """Service information."""
    return jsonify(name="Account REST API Service", version="1.0")


@app.route("/counters", methods=["GET"])
def list_counters():
    """List counters."""
    return jsonify([
        dict(name=name, counter=value)
        for name, value in COUNTER.items()
    ]), status.HTTP_200_OK


@app.route("/counters/<name>", methods=["POST"])
def create_counters(name):
    """Create a counter."""
    if name in COUNTER:
        abort(status.HTTP_409_CONFLICT, f"Counter {name} already exists")
    COUNTER[name] = 0
    return (
        jsonify(name=name, counter=0),
        status.HTTP_201_CREATED,
        {"Location": url_for("read_counters", name=name, _external=True)},
    )


@app.route("/counters/<name>", methods=["GET"])
def read_counters(name):
    """Read a counter."""
    if name not in COUNTER:
        abort(status.HTTP_404_NOT_FOUND, f"Counter {name} does not exist")
    return jsonify(name=name, counter=COUNTER[name]), status.HTTP_200_OK


@app.route("/counters/<name>", methods=["PUT"])
def update_counters(name):
    """Update a counter."""
    if name not in COUNTER:
        abort(status.HTTP_404_NOT_FOUND, f"Counter {name} does not exist")
    COUNTER[name] += 1
    return jsonify(name=name, counter=COUNTER[name]), status.HTTP_200_OK


@app.route("/counters/<name>", methods=["DELETE"])
def delete_counters(name):
    """Delete a counter."""
    COUNTER.pop(name, None)
    return "", status.HTTP_204_NO_CONTENT


@app.route("/accounts", methods=["POST"])
def create_account():
    """Create an account."""
    global NEXT_ACCOUNT_ID
    data = request.get_json(silent=True) or {}
    required = ("name", "email", "address", "phone_number")
    if any(not data.get(field) for field in required):
        return jsonify(error="Missing required account fields"), 400

    account_id = NEXT_ACCOUNT_ID
    NEXT_ACCOUNT_ID += 1
    account = {"id": account_id}
    account.update({field: data[field] for field in required})
    ACCOUNTS[account_id] = account
    return (
        jsonify(account),
        status.HTTP_201_CREATED,
        {"Location": url_for("read_account", account_id=account_id, _external=True)},
    )


@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all accounts."""
    return jsonify(list(ACCOUNTS.values())), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Read one account."""
    account = ACCOUNTS.get(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND, "Account not found")
    return jsonify(account), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):
    """Update an account."""
    account = ACCOUNTS.get(account_id)
    if account is None:
        abort(status.HTTP_404_NOT_FOUND, "Account not found")

    data = request.get_json(silent=True) or {}
    for field in ("name", "email", "address", "phone_number"):
        if field in data:
            account[field] = data[field]
    return jsonify(account), status.HTTP_200_OK


@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an account."""
    if account_id not in ACCOUNTS:
        abort(status.HTTP_404_NOT_FOUND, "Account not found")
    del ACCOUNTS[account_id]
    return "", status.HTTP_204_NO_CONTENT


def reset_counters():
    """Reset counters and accounts during tests."""
    global COUNTER, ACCOUNTS, NEXT_ACCOUNT_ID
    if app.testing:
        COUNTER = {}
        ACCOUNTS = {}
        NEXT_ACCOUNT_ID = 1
