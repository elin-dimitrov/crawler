import json
from jsonschema import validate
import os
import re


def schema():
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

        proffesion = ''
        if os.path.exists("valid_data.json"):
            os.remove("valid_data.json")
        path = os.getcwd()
        abs_path = os.path.abspath(path)
        for file_name in os.listdir(abs_path):
            if file_name.endswith('.json'):
                with open(file_name, encoding='ascii') as ri:
                    data_json = json.load(ri)
                    for data in data_json:
                        minister_name = data.get('Minister name')
                        if len(minister_name):
                            minister_name = f"{minister_name[0]} {minister_name[1]}"
                        minister_email = data.get('Minister email')
                        if len(minister_email): 
                            minister_email = re.findall(r'[\w\.-]+@[\w\.-]+', str(minister_email))
                            minister_email = minister_email[0]
                        minister_info = data.get('Minister Info')
                        if len(minister_info):
                            for info in minister_info:
                                if 'Професия' in info:
                                    proffesion = info.strip('Професия:').strip(';')
                                elif 'Дата на раждане : ' in info:
                                    temp = info.strip('Дата на раждане : ').strip('')
                                    date_of_birth = temp[0:10]
                                    place_of_birth = temp[11:]
                                elif 'Езици' in info:
                                    languages = info.strip('Езици: ')
                                elif 'Избран(а)' in info:
                                    party = info.strip('Избран(а) с политическа сила: ')
                                    party = ''.join(i for i in party if not i.isdigit())
                                    party = party.strip("%;").strip('.')
                                    validate(instance={"Name" : minister_name, "date of birth" : date_of_birth, "place of birth" : place_of_birth,
                                    "Languages" : languages,"Political party" : party, "Proffesion" : proffesion, "e-mail" : str(minister_email)}, schema=schema)
                                    data = {"Name" : minister_name, "date of birth" : date_of_birth, "place of birth" : place_of_birth,
                                        "Languages" : languages,"Political party" : party, "Proffesion" : proffesion, "e-mail" : minister_email}
                                    with open("valid_data.json", 'a', encoding="ascii") as vd:
                                        json.dump((data,), vd)


schema()