from bonds.models import Bond
from rest_framework import permissions, status
from .serializers import BondSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


class BondViewset(APIView):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        legal_name = request.GET.get('legal_name', '')
        if legal_name != "":
            bonds = request.user.bonds.filter(legal_name=legal_name).all()
        else:
            bonds = request.user.bonds.all()

        serializer = BondSerializer(bonds, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if 'lei' in request.data:
            r = requests.get(
                f"https://leilookup.gleif.org/api/v2/leirecords?lei={request.data['lei']}")
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                return Response(r.json()["message"], status=r.status_code)
            request.data["legal_name"] = r.json(
            )[0]["Entity"]["LegalName"]["$"].replace(" ", "")
        else:
            # prevent error below saying it's missing legal name
            request.data["legal_name"] = "NA"

        serializer = BondSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
