"""TP JWT : complete the TODOs. Use the same local educational environment."""
from datetime import datetime, timedelta, timezone
import jwt

KEY = "classroom-tp-key-only"
ALGORITHM = "HS256"

# TODO 1: Create a signed token for sub='student01', role='user', exp in 2 minutes.
token = None

# TODO 2: Print the three encoded segments separated by dots "." .

# TODO 3: Decode the header/payload without checking the signature. Explain the risk.
# Tip: use base64.urlsafe_b64decode and json.loads, or PyJWT with verification disabled.

# TODO 4: Verify the original JWT with the fixed algorithm and KEY.

# TODO 5: Modify only the payload role to 'admin', keeping the ORIGINAL signature.
# Verify the tampered token and catch jwt.InvalidSignatureError.

# TODO 6: Create a SIGNED token with exp 2 minutes in the past.
# Verify it and catch jwt.ExpiredSignatureError.

# BONUS: Print a summary ACCEPTED/REJECTED for all three tokens.
