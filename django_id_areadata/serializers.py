from rest_framework import serializers

class AreaSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        abstract = True

class ProvinceSerializer(AreaSerializer):
    pass

class RegencySerializer(AreaSerializer):
    pass

class DistrictSerializer(AreaSerializer):
    pass

class SubDistrictSerializer(AreaSerializer):
    pass