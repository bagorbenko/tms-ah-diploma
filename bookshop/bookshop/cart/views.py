from rest_framework import mixins, viewsets
from .models import CartItem, Cart
from .serializers import CartItemSerializer, CartSerializer
from .permissions import IsOwnerOrReadOnly


class CartAPIView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = Cart.objects.all()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class CartItemAPIView(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
