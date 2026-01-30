import json
import pandas as pd
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from django.http import HttpResponse
from .models import Dataset
from .serializers import DatasetSerializer, UserSerializer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        if not file.name.endswith('.csv'):
            return Response({'error': 'Invalid file format. Please upload a CSV.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(file)
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            
            if not all(col in df.columns for col in required_columns):
                return Response({'error': f'Missing columns. Required: {required_columns}'}, status=status.HTTP_400_BAD_REQUEST)

            total_count = len(df)
            avg_flowrate = df['Flowrate'].mean()
            avg_pressure = df['Pressure'].mean()
            avg_temperature = df['Temperature'].mean()
            type_distribution = df['Type'].value_counts().to_dict()

            dataset = Dataset.objects.create(
                file_name=file.name,
                total_count=total_count,
                avg_flowrate=round(avg_flowrate, 2),
                avg_pressure=round(avg_pressure, 2),
                avg_temperature=round(avg_temperature, 2),
                type_distribution=type_distribution
            )

            # Maintain only last 5
            all_datasets = Dataset.objects.order_by('-uploaded_at')
            if all_datasets.count() > 5:
                ids_to_keep = all_datasets.values_list('id', flat=True)[:5]
                Dataset.objects.exclude(id__in=ids_to_keep).delete()

            return Response(DatasetSerializer(dataset).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LatestSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest = Dataset.objects.order_by('-uploaded_at').first()
        if not latest:
            return Response({'error': 'No data available'}, status=status.HTTP_404_NOT_FOUND)
        return Response(DatasetSerializer(latest).data)

class HistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DatasetSerializer
    
    def get_queryset(self):
        return Dataset.objects.order_by('-uploaded_at')[:5]

class ReportPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        latest = Dataset.objects.order_by('-uploaded_at').first()
        if not latest:
            return Response({'error': 'No data to report'}, status=status.HTTP_404_NOT_FOUND)

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, height - 50, "Chemical Equipment Parameter Report")

        p.setFont("Helvetica", 12)
        y = height - 100
        p.drawString(50, y, f"File Name: {latest.file_name}")
        y -= 25
        p.drawString(50, y, f"Upload Date: {latest.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}")
        y -= 25
        p.drawString(50, y, f"Total Equipment Count: {latest.total_count}")
        y -= 25
        p.drawString(50, y, f"Average Flowrate: {latest.avg_flowrate}")
        y -= 25
        p.drawString(50, y, f"Average Pressure: {latest.avg_pressure}")
        y -= 25
        p.drawString(50, y, f"Average Temperature: {latest.avg_temperature}")

        y -= 40
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y, "Equipment Type Distribution:")
        y -= 30
        p.setFont("Helvetica", 12)
        
        for eq_type, count in latest.type_distribution.items():
            p.drawString(70, y, f"- {eq_type}: {count}")
            y -= 20

        p.showPage()
        p.save()
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{latest.id}.pdf"'
        return response
