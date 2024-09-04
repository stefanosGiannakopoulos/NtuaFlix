from enum import Enum
from fastapi import Response
import io
import csv
import flatten_dict
from datetime import datetime


class CSVResponse(Response):
    media_type = "text/csv"

    def render(self, content: any) -> bytes:
        """Returns csv by converting dict to csv assuming that all dicts have the same keys."""
        output = io.StringIO()
        content = iter(content)
        first_row = next(content, None)
        if first_row is None:
            return b''
        writer = csv.DictWriter(output, fieldnames=flatten_dict.flatten(first_row.dict(), reducer='dot').keys())
        writer.writeheader()
        writer.writerow(flatten_dict.flatten(first_row.dict(), reducer='dot'))
        for row in content:
            writer.writerow(flatten_dict.flatten(row.dict(), reducer='dot')) #TODO what to do with fields that are lists?

        return output.getvalue().encode('utf-8')

class FormatType(str, Enum):
    json = 'json'
    csv = 'csv'


def check_is_adult(dob: str):
    ADULT_AGE = 18
    current_date = datetime.now()
    age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
    return age >= ADULT_AGE
