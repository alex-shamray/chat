from rest_framework import serializers
from rest_framework.fields import empty, SkipField, BooleanField


class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        parent = self.parent.parent if isinstance(self.parent, serializers.ListSerializer) else self.parent
        serializer = parent.__class__(instance, context=self.context)
        return serializer.data


class OneOffBooleanField(BooleanField):
    def get_attribute(self, instance):
        """
        Given the *outgoing* object instance, return the primitive value
        that should be used for this field.
        """
        value = super().get_attribute(instance)
        if value:
            self.read_only = True
        return value

    def validate_empty_values(self, data):
        """
        Validate empty values, and either:

        * Raise `ValidationError`, indicating invalid data.
        * Raise `SkipField`, indicating that the field should be ignored.
        * Return (True, data), indicating an empty value that should be
          returned without any further validation being applied.
        * Return (False, data), indicating a non-empty value, that should
          have validation applied as normal.
        """
        if not data or data is empty:
            raise SkipField()

        return super().validate_empty_values(data)
