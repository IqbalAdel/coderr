from rest_framework import serializers
from ..models import Order
from profile_app.api.serializers import ProfileDetailSerializer
from profile_app.models import Profile
from offer_app.models import OfferDetail  

class OrderSerializer(serializers.ModelSerializer):
    customer_user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    business_user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    offer_detail_id = serializers.IntegerField(write_only=True)
    title = serializers.CharField(source='offer_detail.title', read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    price = serializers.DecimalField(source='offer_detail.price', max_digits=10, decimal_places=0, read_only=True)
    features = serializers.JSONField(source='offer_detail.features', read_only=True)
    offer_type = serializers.CharField(source='offer_detail.offer_type', read_only=True)
    status = serializers.ChoiceField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')
    class Meta:
        model = Order
        fields = ['id', 
                  'customer_user', 
                  'business_user',
                  'offer_detail_id',
                  'title',
                  'revisions',
                  'delivery_time_in_days',
                  'price',
                  'features',
                  'offer_type', 
                  'status', 
                  'created_at', 
                  'updated_at']

    def create(self, validated_data):
        request = self.context['request']
        offer_detail_id = validated_data.pop('offer_detail_id')

        offer_detail = OfferDetail.objects.select_related('offer__user').get(id=offer_detail_id)

        order = Order.objects.create(
            customer_user=request.user,
            business_user=offer_detail.offer.user,  
            offer_detail=offer_detail,
            **validated_data
        )
        return order
    
    def update(self, instance, validated_data):
        if 'status' not in validated_data:
            raise serializers.ValidationError({"status": "Only the status field can be updated."})

        instance.status = validated_data['status']
        instance.save(update_fields=['status', 'updated_at'])
        return instance