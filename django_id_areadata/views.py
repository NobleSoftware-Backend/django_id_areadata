from typing import List, Type, Optional, TYPE_CHECKING, TypeVar

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_id_areadata.area import AreaData
from django_id_areadata.models import Area, District, Province, Regency, SubDistrict
from django_id_areadata.serializers import (
    DistrictSerializer,
    ProvinceSerializer,
    RegencySerializer,
    SubDistrictSerializer,
)

if TYPE_CHECKING:
    from rest_framework.request import Request

# Create a type variable matching Area types
AreaType = TypeVar("AreaType", bound=Area)

class AreaListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    search_fields = ["name"]
    model: Optional[AreaType] = None

    def get_and_filter_model(self, request: "Request") -> tuple[List[Area], int]:
        """
        Get and filter area data based on request parameters.

        Returns:
            Tuple of (filtered_data, count)
        """
        if not self.model:
            raise AttributeError("model is required")

        query_params = request.query_params
        filter_id: Optional[str] = (
            query_params.get("province_id")
            or query_params.get("regency_id")
            or query_params.get("district_id")
        )

        search_query = query_params.get("search")

        area_data: AreaData = AreaData(area_type=self.model)

        # Get base data
        if filter_id:
            data = area_data.filter_by_parent_id(filter_id)
        else:
            data = area_data.get_all()

        # Apply search if present
        if search_query:
            data = [item for item in data if search_query.lower() in item.name.lower()]

        return data, len(data)

    def list(self, request, *args, **kwargs):
        # Return empty result for non-Province views without query params
        view_name = self.__class__.__name__
        if view_name != "ProvinceList" and not request.query_params:
            return Response({"results": [], "count": 0})

        data, count = self.get_and_filter_model(request)
        serializer = self.get_serializer(data, many=True)
        response_data = {"results": serializer.data, "count": count}
        return Response(response_data)


@extend_schema_view(
    get=extend_schema(
        responses={
            200: OpenApiResponse(
                response=ProvinceSerializer,
                description="List of provinces",
                examples=[
                    OpenApiExample(
                        "Result with data",
                        value={
                            "results": [
                                {
                                    "id": "31",
                                    "name": "DKI Jakarta",
                                },
                            ],
                            "count": 1,
                        },
                    ),
                ],
            ),
            403: OpenApiResponse(
                description="You do not have a permission to access this page",
            ),
        },
    ),
)
class ProvinceList(AreaListView):
    filter_backends = [SearchFilter]
    serializer_class = ProvinceSerializer
    model = Province


@extend_schema_view(
    get=extend_schema(
        parameters=[OpenApiParameter("province_id", OpenApiTypes.STR, required=True)],
        responses={
            200: OpenApiResponse(
                response=RegencySerializer,
                description="List of regencies/cities",
                examples=[
                    OpenApiExample(
                        "Result with data",
                        value={
                            "results": [
                                {
                                    "id": "31.01",
                                    "name": "Kabupaten Administrasi Kepulauan Seribu",
                                },
                            ],
                            "count": 1,
                        },
                    ),
                ],
            ),
            403: OpenApiResponse(
                description="You do not have a permission to access this page",
            ),
        },
    ),
)
class RegencyList(AreaListView):
    serializer_class = RegencySerializer
    model = Regency


@extend_schema_view(
    get=extend_schema(
        parameters=[OpenApiParameter("regency_id", OpenApiTypes.STR, required=True)],
        responses={
            200: OpenApiResponse(
                response=DistrictSerializer,
                description="List of districts",
                examples=[
                    OpenApiExample(
                        "Result with data",
                        value={
                            "results": [
                                {"id": "31.01.01", "name": "Kepulauan Seribu Utara"},
                                {"id": "31.01.02", "name": "Kepulauan Seribu Selatan"},
                            ],
                            "count": 2,
                        },
                    ),
                ],
            ),
            403: OpenApiResponse(
                description="You do not have a permission to access this page",
            ),
        },
    ),
)
class DistrictList(AreaListView):
    serializer_class = DistrictSerializer
    model = District


@extend_schema_view(
    get=extend_schema(
        parameters=[OpenApiParameter("district_id", OpenApiTypes.STR, required=True)],
        responses={
            200: OpenApiResponse(
                response=SubDistrictSerializer,
                description="List of sub-districts",
                examples=[
                    OpenApiExample(
                        "Result with data",
                        value={
                            "results": [
                                {"id": "31.01.01.1001", "name": "Pulau Panggang"},
                                {"id": "31.01.01.1002", "name": "Pulau Kelapa"},
                                {"id": "31.01.01.1003", "name": "Pulau Harapan"},
                            ],
                            "count": 3,
                        },
                    ),
                ],
            ),
            403: OpenApiResponse(
                description="You do not have a permission to access this page",
            ),
        },
    ),
)
class SubDistrictList(AreaListView):
    serializer_class = SubDistrictSerializer
    model = SubDistrict
