from rest_framework import serializers
from ..models import Offer, OfferDetail
from profile_app.api.serializers import ProfileDetailSerializer
from profile_app.models import Profile

class DetailSerializer(serializers.ModelSerializer):
    offer_type = serializers.ChoiceField(choices=[('basic', 'Basic'), ('standard', 'Standard'), ('premium', 'Premium')], required=True)
    class Meta:
        model = OfferDetail
        fields = ['id','title','revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

class DetailHyperSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='offerdetails-detail', lookup_field='pk')
    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

class UserDetailSerializer(ProfileDetailSerializer):
    class Meta:
        model= Profile
        fields = ['first_name', 'last_name', 'username']

class OfferCreateSerializer(serializers.ModelSerializer): 
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    details = DetailSerializer(many=True)
    
    class Meta:
        model = Offer
        fields = ['id','user', 'title', 'image', 'description', 'details']
    
    def validate_details(self, value):
        """
        Ensure that all three types (basic, standard, premium) are present.
        """
        required_types = {'basic', 'standard', 'premium'}
        
        provided_types = {d['offer_type'] for d in value}
        

        missing = required_types - provided_types
        extra = provided_types - required_types

        if missing:
            raise serializers.ValidationError(f"Missing OfferDetail types: {', '.join(missing)}")
        if extra:
            raise serializers.ValidationError(f"Unexpected OfferDetail types: {', '.join(extra)}")

        return value

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)
        if offer.user.type != 'business':
            raise serializers.ValidationError("Only business users can create offers.")
        for detail_data in details_data:
            OfferDetail.objects.create(offer=offer, **detail_data)
        return offer
    
class OfferListSerializer(serializers.ModelSerializer): 
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    user_details = UserDetailSerializer(source='user.profile', read_only=True)
    details = DetailHyperSerializer(many=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Offer
        fields = ['id','user', 'title', 'image', 'description','created_at','updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']

    def get_min_price(self, obj):
        details = obj.details.all()
        if not details:
            return None
        return min(detail.price for detail in details)

    def get_min_delivery_time(self, obj):
        details = obj.details.all()
        if not details:
            return None
        return min(detail.delivery_time_in_days for detail in details)

class OffersDetailSerializer(OfferListSerializer):
    class Meta:
        model = Offer
        fields = ['id','user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']

class OfferUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    details = DetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id','user', 'title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        request_user = self.context['request'].user
        if instance.user != request_user:
            raise serializers.ValidationError("Only the creator can update this offer.")

        for attr, value in validated_data.items():
            if attr != 'details':  
                setattr(instance, attr, value)
        instance.save()

        details_data = validated_data.get('details', [])
        for detail_data in details_data:
            offer_type = detail_data['offer_type']
            try:
                offer_detail = instance.details.get(offer_type=offer_type)
            except OfferDetail.DoesNotExist:
                raise serializers.ValidationError(f"OfferDetail with type '{offer_type}' does not exist.")
            for attr, value in detail_data.items():
                setattr(offer_detail, attr, value)
            if instance.details.count() < 3:
                raise serializers.ValidationError("An offer must always have 3 details.")                
            offer_detail.save()
        return instance