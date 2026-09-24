from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Batch
from .serializers import BatchSerializer


class BatchListCreateView(APIView):

    def get(self, request):
        batches = Batch.objects.all().order_by('-id')
        serializer = BatchSerializer(batches, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BatchSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class BatchDetailView(APIView):

    def get_object(self, pk):
        try:
            return Batch.objects.get(pk=pk)
        except Batch.DoesNotExist:
            return None

    def get(self, request, pk):
        batch = self.get_object(pk)

        if not batch:
            return Response(
                {'detail': 'Batch not found'},
                status=404
            )

        serializer = BatchSerializer(batch)
        return Response(serializer.data)

    def put(self, request, pk):
        batch = self.get_object(pk)

        if not batch:
            return Response(
                {'detail': 'Batch not found'},
                status=404
            )

        serializer = BatchSerializer(
            batch,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=400
        )

    def delete(self, request, pk):
        batch = self.get_object(pk)

        if not batch:
            return Response(
                {'detail': 'Batch not found'},
                status=404
            )

        batch.delete()

        return Response(
            {'message': 'Batch deleted successfully'}
        )