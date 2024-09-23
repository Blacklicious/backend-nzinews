from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Member, Employee, Business, Badge, BusinessImage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user
    
class MemberSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, required=False)

    class Meta:
        model = Member
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }
        
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data.setdefault('role', 'member')
        validated_data.setdefault('status', 'inactive')

        member = super().create(validated_data)
        return member

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data.setdefault('role', 'job_hunter')
        return super().create(validated_data)

class BusinessImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessImage
        fields = '__all__'
        

class BusinessSerializer(serializers.ModelSerializer):
    owners = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    managers = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    supervisors = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    fulltime_employees = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    parttime_employees = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    consultants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    interns = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    images = BusinessImageSerializer(many=True, required=False)

    class Meta:
        model = Business
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'read_only': True},
        }

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        validated_data['created_by'] = self.context['request'].user
        validated_data.setdefault('status', 'incomplete')
        business = super().create(validated_data)
        for image_data in images_data:
            BusinessImage.objects.create(business=business, **image_data)
        return business

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        instance = super().update(instance, validated_data)
        
        # Handle images update
        instance.images.all().delete()
        for image_data in images_data:
            BusinessImage.objects.create(business=instance, **image_data)
        
        return instance

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'