from pydantic import BaseModel, Field
from typing import List, Optional


class Suggestion(BaseModel):
    suggestion: str = Field(description="General suggestion related to the user's query")

class WhomToConsult(BaseModel):
    specialist: str = Field(description="Specialist to consult for the user's condition")
    description: str = Field(description="Description of the specialist")

class ClinicalGuidance(BaseModel):
    guidance: str = Field(description="Clinical guidance for the user's condition")
    description: str = Field(description="Description of the clinical guidance")

class Treatment(BaseModel):
    treatment: str = Field(description="Treatment options for the user's condition")
    description: str = Field(description="Description of the treatment options")

class DietAndNutrition(BaseModel):
    diet: str = Field(description="Diet and nutrition advice for the user's condition")
    description: str = Field(description="Description of the diet and nutrition advice")

class Monitoring(BaseModel):
    monitoring: str = Field(description="Monitoring advice for the user's condition")
    description: str = Field(description="Description of the monitoring advice")

class Dos(BaseModel):
    dos: List[str] = Field(description="Things the user should do")

class Donts(BaseModel):
    donts: List[str] = Field(description="Things the user should not do")

class HomeRemedies(BaseModel):
    remedies: str = Field(description="Home remedies for the user's condition")
    description: str = Field(description="Description of the home remedies")

class MentalHealthAndWellBeing(BaseModel):
    mental_health: str = Field(description="Mental health and well-being advice")
    description: str = Field(description="Description of the mental health and well-being advice")

class FirstAids(BaseModel):
    first_aid: str = Field(description="First aid advice for the user's condition")
    description: str = Field(description="Description of the first aid advice")

class Precautions(BaseModel):
    precautions: str = Field(description="Precautions to take for the user's condition")
    description: str = Field(description="Description of the precautions")

class Warnings(BaseModel):
    warnings: str = Field(description="Warnings related to the user's condition")
    description: str = Field(description="Description of the warnings")

class Emergency(BaseModel):
    emergency: str = Field(description="Emergency information related to the user's condition")
    description: str = Field(description="Description of the emergency information")

class InstantAnswer(BaseModel):
    emergency: Optional[Emergency] = Field(None, description="Emergency information related to the user's condition")
    suggestion: Suggestion = Field(description="General suggestion related to the user's query")
    whom_to_consult: Optional[WhomToConsult] = Field(None, description="Specialist to consult for the user's condition")
    clinical_guidance: Optional[ClinicalGuidance] = Field(None, description="Clinical guidance for the user's condition")
    treatment: Optional[Treatment] = Field(None, description="Treatment options for the user's condition")
    diet_and_nutrition: Optional[DietAndNutrition] = Field(None, description="Diet and nutrition advice for the user's condition")
    monitoring: Optional[Monitoring] = Field(None, description="Monitoring advice for the user's condition")
    dos: Optional[Dos] = Field(None, description="Things the user should do")
    donts: Optional[Donts] = Field(None, description="Things the user should not do")
    home_remedies: Optional[HomeRemedies] = Field(None, description="Home remedies for the user's condition")
    mental_health_and_well_being: Optional[MentalHealthAndWellBeing] = Field(None, description="Mental health and well-being advice")
    first_aids: Optional[FirstAids] = Field(None, description="First aid advice for the user's condition")
    precautions: Optional[Precautions] = Field(None, description="Precautions to take for the user's condition")
    warnings: Optional[Warnings] = Field(None, description="Warnings related to the user's condition")