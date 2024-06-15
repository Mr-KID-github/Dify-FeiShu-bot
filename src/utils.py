# utils.py
import uuid

class Utils:
    @staticmethod
    def convert_to_uuid(original_id):
        try:
            # Create a UUID from the original string (only works if the original string is a valid UUID format)
            new_uuid = uuid.UUID(original_id)
            return str(new_uuid)
        except ValueError:
            # If the original string is not a valid UUID format, generate a new UUID
            return str(uuid.uuid4())
