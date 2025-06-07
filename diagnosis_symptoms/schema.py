import json

Initial_Response = json.dumps({
        "HealthQuery": "true/false",
        "LifeThreatening": "true/false",
        "EmergencyLevel": "High/Moderate/Low",
        "Consult": "Emergency Room/Primary Care Physician/Specialist",
        "Note": "string"
    })


Question_Response = json.dumps({
    
    "health_query": {
        "type": "boolean"
    },
    "query": {
        "type": {
            "type": "string"
        },
        "question": {
            "type": "string"
        },
        "options": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "required": ["type", "question", "options"]
    },
    "required": ["health_query", "query"]
})


Diagnosis_Response = json.dumps({
    "type": "object",
    
    "healthQuery": {
        "type": "boolean"
    },
    "diagnosis": {
        "type": "array",
        "items": {
            "type": "string"
        }
    },
    "diagnosis_description": {
        "type": "array",
        "items": {
            "type": "string"
        }
    },
    "serious": {
        "type": "array",
        "items": {
            "type": "boolean"
        }
    },
    "consult_specialties": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 1,
            "maxItems": 3
        },
    "chances": {
        "type": "array",
        "items": {
            "type": "string"
        }
    },
    "required": ["healthQuery", "diagnosis","diagnosis_description," "serious","consult_specialties", "chances"]
})
