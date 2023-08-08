import shutil

from rest_framework import serializers
from .models import *


# class FileSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Files
#         fields = '__all__'

# class FileListSerializer(serializers.Serializer):
#     files = serializers.ListField(
#         child = serializers.FileField(max_length = 100000 , allow_empty_file = False , use_url = False)
#     )
#     folder = serializers.CharField(required = False)
    
#     def zip_files(self,folder):
#         shutil.make_archive(f'public/static/zip/{folder}' , 'zip' ,f'public/static/{folder}' )

#     def create(self , validated_data):
#         folder = Folder.objects.create()
#         files = validated_data.pop('files')      
#         files_objs = []
#         for file in files:
#             files_obj = Files.objects.create(folder = folder , file = file)
#             files_objs.append(files_obj)

        
#         self.zip_files(folder.uid)


#         return {'files' : {} , 'folder' : str(folder.uid)}

import os
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from rest_framework import serializers
from .models import Folder, Files

class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False)
    )
    folder = serializers.CharField(required=False)
    
    def zip_files(self, folder):
        shutil.make_archive(f'public/static/zip/{folder}', 'zip', f'public/static/{folder}')

    def create_pdf_from_folder(self, folder, output_file):
        # Get a list of files in the folder
        file_list = os.listdir(f'public/static/{folder}')

        # Create a new PDF document
        doc = SimpleDocTemplate(output_file, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Add a title to the PDF
        title_style = ParagraphStyle(name='TitleStyle', fontSize=20, textColor=colors.blue)
        title = Paragraph(f'Files in folder: {folder}', title_style)
        elements.append(title)

        # Add a list of files to the PDF
        list_style = ParagraphStyle(name='ListStyle', fontSize=12, textColor=colors.black)
        for filename in file_list:
            file_text = Paragraph(f'- {filename}', list_style)
            elements.append(file_text)

        # Build the PDF
        doc.build(elements)

    def create(self, validated_data):
        folder = Folder.objects.create()
        files = validated_data.pop('files')      
       
        for file in files:
            files_obj = Files.objects.create(folder=folder, file=file)
         

        self.zip_files(folder.uid)

        # Generate PDF
        pdf_output_file = f'public/static/pdf/{folder.uid}.pdf'
        self.create_pdf_from_folder(folder.uid, pdf_output_file)

        return {'files': {}, 'folder': str(folder.uid)}
