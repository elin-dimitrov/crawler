from django.shortcuts import render
from . import models, serializers
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from . import models
from .serializers import MinisterSerializer
import ast
import json
from jsonschema import validate
import re
import os, sys


class Politician(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        """This method allow to request the exracted data ministers by key word or without.
           It will bring back obejct based on the filter search. In case key word is not used
           it will return json format object containing inormation for each minister
        """
        minister_id = request.GET.get('id', None)
        minister_name = request.GET.get('minister_name', None)
        party = request.GET.get('party', None)
        date_of_birth = request.GET.get('date_of_birth', None)
        place_of_birth = request.GET.get('place_of_birth', None)
        languages = request.GET.get('languages', None)
        proffesion = request.GET.get('proffesion', None)
        
        try:
            if minister_id:
                minister = models.Politic.objects.get(id=minister_id)
                serialized = serializers.MinisterSerializer(minister, many=False)
                return Response(data=serialized.data, status=status.HTTP_200_OK)

            elif minister_name:
                minister = models.Politic.objects.filter(minister_name__contains=minister_name.upper()).order_by('minister_name')
                paginator = Paginator(minister, 10)
                page_obj = paginator.page(paginator.num_pages)
                serialized = serializers.MinisterSerializer(page_obj, many=True)
                return Response(data=serialized.data, status=status.HTTP_200_OK)

            elif party:
                minister = models.Politic.objects.filter(party__contains=party.upper()).order_by('minister_name')
                paginator = Paginator(minister, 10)
                page_obj = paginator.page(paginator.num_pages)
                serialized = serializers.MinisterSerializer(page_obj, many=True)
                return Response(data=serialized.data, status=status.HTTP_200_OK)

            elif date_of_birth:
                minister = models.Politic.objects.filter(date_of_birth=date_of_birth).order_by('minister_name')
                paginator = Paginator(minister, 10)
                page_obj = paginator.page(paginator.num_pages)
                serialized = serializers.MinisterSerializer(page_obj, many=True)
                return Response(data=serialized.data, status=status.HTTP_200_OK)

            elif place_of_birth:
                minister = models.Politic.objects.filter(place_of_birth__contains=place_of_birth.capitalize()).order_by('minister_name')
                paginator = Paginator(minister, 10)
                page_obj = paginator.page(paginator.num_pages)
                serialized = serializers.MinisterSerializer(page_obj, many=True)
                return Response(data=serialized.data, status=status.HTTP_200_OK)

            elif languages:
                minister = models.Politic.objects.filter(languages__contains=languages).order_by('minister_name')
                paginator = Paginator(minister, 10)
                page_obj = paginator.page(paginator.num_pages)
                serialized = serializers.MinisterSerializer(page_obj, many=True)
                return Response(data=serialized.data, status=status.HTTP_200_OK)

            elif proffesion:
                minister = models.Politic.objects.filter(proffesion__contains=proffesion).order_by('proffesion')
                paginator = Paginator(minister, 10)
                page_obj = paginator.page(paginator.num_pages)
                serialized = serializers.MinisterSerializer(page_obj, many=True)
                return Response(data=serialized.data, status=status.HTTP_200_OK)

            else:
                minister = models.Politic.objects.all().order_by('minister_name')
                paginator = Paginator(minister, 10)
                page_obj = paginator.page(paginator.num_pages)
                serialized = serializers.MinisterSerializer(page_obj, many=True)
                return Response(data=serialized.data, status=status.HTTP_200_OK)
        except Exception as er:
            return Response(data={f"error: {er}"}, status=status.HTTP_404_NOT_FOUND)


class ImportData(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):

        """This method includes the following features:
            - validate the extracted data form the spider
            - match the approopriate data to the key table
            - import all data in the databse
        """

        models.Politic.objects.all().delete()
        path = os.getcwd()
        dir_name = os.path.dirname(path)
        path = f"{dir_name}/data_pro/data_pro/spiders/ministers.json"
        schema={
        "title": "Ministers",
        "description": "Information minister details",
        "type": "object",
        "required": [
            "Name",
            "date of birth",
            "place of birth",
            "Languages",
            "Political party",
            "Proffesion",
            "e-mail",
        ],
        "properties": {
            "Name": {
            "type": "string",
            "title": "First name",
            "default": "None"
            },
            "Proffesion": {
            "type": "string",
            "title": "Proffesion",            
            },
            "Languages":{
                "type": "string",
                "title": "Language",
                "default": "Bulgarian",
            },
            "date of birth":{
                "type": "string",
                "title": "birth date",
                "format": "date",
            },
            "place of birth":{
                "type": "string",
                "title": "place of birth",
            },    
            "Political party":{
                "type": "string",
                "title": "Political party",
                "default": "independent",
            },
            "e-mail":{
                "type": "string",
                "title": "e-mail",
                "format": "email",
            }
            
        }
        }
        date_of_birth = ''
        place_of_birth = '' 
        proffesion = ''
        languages = ''
        party = ''
        with open(path, encoding='ascii') as ri:
            data_json = json.load(ri)
            for data in list(data_json):
                minister_name = data.get('Minister name')
                if minister_name:
                    minister_name = f"{minister_name[0]} {minister_name[1]}"
                minister_email = data.get('Minister email')
                if minister_email: 
                    minister_email = re.findall(r'[\w\.-]+@[\w\.-]+', str(minister_email))
                    minister_email = minister_email[0]
                minister_info = data.get('Minister Info')
                if minister_info:
                    for info in minister_info:
                        if 'Дата на раждане : ' in info:
                            temp = info.strip('Дата на раждане : ').strip('')
                            date_of_birth = temp[0:10]
                            place_of_birth = temp[11:]
                        elif 'Професия' in info:
                            proffesion = info.strip('Професия:').strip(';')
                        elif 'Езици' in info:
                            languages = info.strip('Езици: ')
                        elif 'Избран(а)' in info:
                            party = info.strip('Избран(а) с политическа сила: ')
                            party = ''.join(i for i in party if not i.isdigit())
                            party = party.strip("%;").strip('.')
                        try:
                            validate(instance={"Name" : minister_name, "date of birth" : date_of_birth, "place of birth" : place_of_birth,
                            "Languages" : languages,"Political party" : party, "Proffesion" : proffesion, "e-mail" : str(minister_email)}, schema=schema)
                             
                            minister = models.Politic.objects.filter(date_of_birth=date_of_birth).filter(minister_name=minister_name)
                            if len(minister) == 0: 
                                models.Politic.objects.create(
                                minister_name=minister_name,
                                email=minister_email,
                                proffesion=proffesion,
                                date_of_birth=date_of_birth,
                                place_of_birth=place_of_birth,
                                languages=languages,
                                party=party
                                )
                        except Exception as ValidationError:
                             return Response(data={'message': f'{ValidationError}'}, status=status.HTTP_406_NOT_ACCEPTABLE)
                                                      
            return Response(data={'message': 'Data imported successfully'}, status=status.HTTP_200_OK)