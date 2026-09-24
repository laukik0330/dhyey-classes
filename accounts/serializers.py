from rest_framework import serializers

from students.models import Student


class StudentProfileSerializer(serializers.ModelSerializer):

    profile_image = serializers.SerializerMethodField()

    class Meta:

        model = Student

        fields = [
            'id',
            'name',
            'email',
            'phone',
            'parent_name',
            'parent_phone',
            'profile_image',
        ]

        read_only_fields = [
            'id',
            'name',
            'parent_name',
            'parent_phone',
        ]


    def get_profile_image(self, obj):

        if not obj.profile_image:
            return None

        request = self.context.get('request')

        if request:
            return request.build_absolute_uri(
                obj.profile_image.url
            )

        return obj.profile_image.url