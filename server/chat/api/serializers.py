from rest_framework import serializers

from ..models import Person, Channel, Message


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):
    members = PersonSerializer(many=True, allow_empty=False)
    message = serializers.CharField(write_only=True)

    class Meta:
        model = Channel
        fields = '__all__'
        read_only_fields = ('messages_count',)

    def create(self, validated_data):
        return Channel.objects.create_channel(self.context['request'].user, **validated_data)


class MessageSerializer(serializers.ModelSerializer):
    author = PersonSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('author', 'body', 'date_created')
        read_only_fields = ('author', 'date_created')

    def create(self, validated_data):
        validated_data['channel'] = self.context['channel']
        validated_data['author'] = self.context['request'].user
        return super(MessageSerializer, self).create(validated_data)
