from flask_restful import abort
from models.db import DCategory
from marshmallow import Schema, fields, ValidationError, validate, types
import typing


class CategoryRequestSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(max=50))

    def handle_error(self, error: ValidationError, __, *, many: bool, **kwargs):
        abort(400, messages=error.messages)

    def validate(
        self,
        data: typing.Mapping,
        *,
        many: typing.Optional[bool] = None,
        partial: typing.Optional[typing.Union[bool, types.StrSequenceOrSet]] = None
    ) -> typing.Dict[str, typing.List[str]]:
        validation_errors = {}
        if DCategory.query.filter(DCategory.name == data["name"]).first():
            validation_errors.update(
                {
                    'name': [
                        'Already exist'
                    ]
                }
            )
        return validation_errors
