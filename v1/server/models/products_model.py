#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :
# author: 'ACIOBANI'
from flask_jwt_auth.v1.server import db_sql
from flask_jwt_auth.v1.server.models import BaseModel
from flask_jwt_auth.v1.server.dtos.serializers import JsonEncodedDict


class Product(BaseModel):
    """
    Product Model for storing shopping products details.
    """
    a = {
        # "gtin": "05057753542276",
        # "tpnb": "085662618",
        # "tpnc": "301691890",
        # "description": "Plaza Prosecco Doc Brut 37.5 Cl",
        # "brand": "TESCO",
        # "qtyContents": {
        #   "quantity": 37.5,
        #   "totalQuantity": 37.5,
        #   "quantityUom": "cl",
        #   "unitQty": "75CL",
        #   "netContents": "37.5cl \u212e",
        #   "avgMeasure": "Average Measure (e)"
        # },
        # "productCharacteristics": {
        #   "isFood": false,
        #   "isDrink": true,
        #   "isHazardous": false,
        #   "storageType": "Ambient",
        #   "isAnalgesic": false,
        #   "containsLoperamide": false,
        #   "totalAlcoholUnits": 4.1
        # },
        "ingredients": [
          "<b>INGREDIENTS:</b> Preservative (Potassium <strong>Metabisulphite</strong>)."
        ],
        "gda": {
          "gdaRefs": [
            {
              "gdaDescription": "Guideline Amounts Per Serv",
              "footers": [
                "Typical values per 100ml: Energy 280kJ / 67kcal"
              ],
              "values": [
                {
                  "name": "Energy",
                  "values": [
                    "351kJ",
                    "84kcal"
                  ],
                  "percent": "4"
                },
                {
                  "name": "Fat",
                  "values": [
                    "0g"
                  ],
                  "percent": "0"
                },
                {
                  "name": "Sugars",
                  "values": [
                    "1.6g"
                  ],
                  "percent": "2"
                },
                {
                  "name": "Salt",
                  "values": [
                    "<0.01g"
                  ],
                  "percent": "0"
                }
              ]
            }
          ]
        },
        "calcNutrition": {
          "per100Header": "100ml contains",
          "perServingHeader": "A serving contains",
          "calcNutrients": [
            {
              "name": "Energy (kJ)",
              "valuePer100": "280",
              "valuePerServing": "351"
            },
            {
              "name": "Energy (kcal)",
              "valuePer100": "67",
              "valuePerServing": "84"
            }
          ]
        },
        "allergenAdvice": {
          "allergens": [
            {
              "allergenName": "Contains",
              "allergenValues": [
                "Contains sulphites.",
                ""
              ]
            }
          ],
          "allergenText": "Contains sulphites. "
        },
        "safety": {
          "safetyWarnings": [
            "Do not store at high temperatures or shake bottle. Open with care."
          ]
        },
        "storage": ["Store in a cool dry place. \n"],
        "marketingText": "A classic Italian sparkling wine made from the Glera grape grown in the rolling vineyards in north east Italy. Alively, refreshing wine ful of bright citrus fruit flavours with background floreal notes. Perfect, served chilled, for any occasion as an aperitif. Alternatively it can also be anjoyed with fish of shellfish. Store in a cool, dark place. Do not store at high temperature or shake bottle. Open with care.\nA classic Italian sparkling wine made from the Glera grape grown in the rolling vineyards in north east Italy. Alively, refreshing wine ful of bright citrus fruit flavours with background floreal notes. Perfect, served chilled, for any occasion as an aperitif. Alternatively it can also be anjoyed with fish of shellfish. Store in a cool, dark place. Do not store at high temperature or shake bottle. Open with care.",
        # "pkgDimensions": [
        #   {
        #     "no": 1,
        #     "height": 26.6,
        #     "width": 7.1,
        #     "depth": 7.1,
        #     "dimensionUom": "cm",
        #     "weight": 839.0,
        #     "weightUom": "g",
        #     "volume": 1340.906,
        #     "volumeUom": "cc"
        #   }
        # ],
        "productAttributes": [
          {
            "source": "BB",
            "category": [
              {
                "general_alcohol": {
                  "alcohol_type": {
                    "name": "Alcohol Type",
                    "value": "Wine"
                  },
                  "alcohol_volume_percentage": {
                    "name": "Alcohol Volume Percentage",
                    "value": "11"
                  },
                  "alcohol_content_units": {
                    "name": "Alcohol Content Units",
                    "value": "4.2"
                  },
                  "tasting_notes": {
                    "name": "Tasting Notes",
                    "value": "A lively, refreshing wine full of bright citrus fruit flavours with background floral notes"
                  },
                  "serving_suggestion": {
                    "name": "Serving Suggestion",
                    "value": "Perfect served chilled, for any occasion as an aperitif. Alternatively it can also be enjoyed with fish or shellfish"
                  },
                  "units_other_text": {
                    "name": "Alcohol Units Other Text",
                    "value": "4.2 UK Units per bottle\n1.4 UK Units per 125ml glass\nKnow Your Limits\nUK Chief Medical Officers recommend adults do not regularly drink more than 14 units a week\nDrink Responsibly\nFor more facts: drinkaware.co.uk"
                  }
                },
                "champagne_and_wine": {
                  "effervescence": {
                    "name": "Effervesence",
                    "value": "Sparkling"
                  },
                  "region_of_origin": {
                    "name": "Region of Origin",
                    "value": "Veneto"
                  },
                  "colour": {
                    "name": "Colour",
                    "value": "White"
                  },
                  "type_of_closure": {
                    "name": "Type of Closure",
                    "value": "Natural Cork"
                  },
                  "recommended_storage": {
                    "name": "Recommended Storage",
                    "value": "To ensure this wine is consumed at its best, please see best before date on: 1 year"
                  },
                  "current_vintage": {
                    "name": "Current Vintage",
                    "value": "Non Vintage"
                  },
                  "producer": {
                    "name": "Producer",
                    "value": "CR - Campegine in Vazzola (TV), Italy"
                  },
                  "grape_variety": {
                    "name": "Grape Variety",
                    "value": "Glera"
                  },
                  "winemaker": {
                    "name": "Winemaker",
                    "value": "CR - Campegine in Vazzola (TV), Italy"
                  },
                  "wine_agent": {
                    "name": "Wine Agent",
                    "value": "Cellars"
                  },
                  "vinification_details": {
                    "name": "Vinification Details",
                    "value": "Our winery produces sparkling wines and Proseccos directly from the must, which undergoes a prise de mousse with selected yeasts for a period of one month at a controlled temperature of 12-15\u00b0C. The prise de mousse is stopped by lowering the temperature of the pressurized tank to ensure the desired level of residual sugar."
                  },
                  "history": {
                    "name": "History",
                    "value": "For the production of our Prosecco D.O.C. we use the grapes from a larger cultivation zone, selecting the vineyards that can offer the best of the vast area in which Glera grapes are grown"
                  },
                  "regional_information": {
                    "name": "Regional Information",
                    "value": "For the production of our Prosecco D.O.C. we use the grapes from a larger cultivation zone, selecting the vineyards that can offer the best of the vast area in which Glera grapes are grown"
                  }
                },
                "storage_info": {
                  "storage_type": {
                    "name": "Storage Type",
                    "value": "Ambient"
                  },
                  "prep_and_usage": {
                    "name": "Preparation and Usage",
                    "value": "Perfect served chilled, for any occasion as an aperitif. Alternatively it can also be enjoyed with fish or shellfish."
                  }
                },
                "lifestyle": [
                  {
                    "lifestyle": {
                      "name": "Lifestyle",
                      "value": "Suitable for Vegetarians"
                    }
                  }
                ]
              }
            ]
          },
          {
            "category": [
              {
                "lifestyle": [
                  {
                    "lifestyle": {
                      "name": "Lifestyle",
                      "value": "Suitable for Vegetarians"
                    }
                  }
                ],
                "general_alcohol": {
                  "alcohol_type": {
                    "name": "Alcohol Type",
                    "value": "Wine"
                  },
                  "alcohol_volume_percentage": {
                    "name": "Alcohol Volume Percentage",
                    "value": "11"
                  },
                  "alcohol_content_units": {
                    "name": "Alcohol Content Units",
                    "value": "4.2"
                  },
                  "tasting_notes": {
                    "name": "Tasting Notes",
                    "value": "A lively, refreshing wine full of bright citrus fruit flavours with background floral notes"
                  },
                  "serving_suggestion": {
                    "name": "Serving Suggestion",
                    "value": "Perfect served chilled, for any occasion as an aperitif. Alternatively it can also be enjoyed with fish or shellfish"
                  },
                  "units_other_text": {
                    "name": "Alcohol Units Other Text",
                    "value": "4.2 UK Units per bottle\n1.4 UK Units per 125ml glass\nKnow Your Limits\nUK Chief Medical Officers recommend adults do not regularly drink more than 14 units a week\nDrink Responsibly\nFor more facts: drinkaware.co.uk"
                  }
                },
                "champagne_and_wine": {
                  "effervescence": {
                    "name": "Effervesence",
                    "value": "Sparkling"
                  },
                  "region_of_origin": {
                    "name": "Region of Origin",
                    "value": "Veneto"
                  },
                  "colour": {
                    "name": "Colour",
                    "value": "White"
                  },
                  "type_of_closure": {
                    "name": "Type of Closure",
                    "value": "Natural Cork"
                  },
                  "recommended_storage": {
                    "name": "Recommended Storage",
                    "value": "To ensure this wine is consumed at its best, please see best before date on: 1 year"
                  },
                  "current_vintage": {
                    "name": "Current Vintage",
                    "value": "Non Vintage"
                  },
                  "producer": {
                    "name": "Producer",
                    "value": "CR - Campegine in Vazzola (TV), Italy"
                  },
                  "grape_variety": {
                    "name": "Grape Variety",
                    "value": "Glera"
                  },
                  "winemaker": {
                    "name": "Winemaker",
                    "value": "CR - Campegine in Vazzola (TV), Italy"
                  },
                  "wine_agent": {
                    "name": "Wine Agent",
                    "value": "Cellars"
                  },
                  "vinification_details": {
                    "name": "Vinification Details",
                    "value": "Our winery produces sparkling wines and Proseccos directly from the must, which undergoes a prise de mousse with selected yeasts for a period of one month at a controlled temperature of 12-15\u00b0C. The prise de mousse is stopped by lowering the temperature of the pressurized tank to ensure the desired level of residual sugar."
                  },
                  "history": {
                    "name": "History",
                    "value": "For the production of our Prosecco D.O.C. we use the grapes from a larger cultivation zone, selecting the vineyards that can offer the best of the vast area in which Glera grapes are grown"
                  },
                  "regional_information": {
                    "name": "Regional Information",
                    "value": "For the production of our Prosecco D.O.C. we use the grapes from a larger cultivation zone, selecting the vineyards that can offer the best of the vast area in which Glera grapes are grown"
                  }
                },
                "storage_info": {
                  "storage_type": {
                    "name": "Storage Type",
                    "value": "Ambient"
                  },
                  "prep_and_usage": {
                    "name": "Preparation and Usage",
                    "value": "Perfect served chilled, for any occasion as an aperitif. Alternatively it can also be enjoyed with fish or shellfish."
                  }
                }
              }
            ]
          }
        ]
      }

    __tablename__ = 'products'
    __optional_params = ('gtin', 'tpnb', 'tpnc', 'brand', 'quantity_contents', 'product_characteristics', 'safety',
                         'package_dimensions', 'ingredients', 'gda', 'calculated_nutrition', 'allergen_advice',
                         'storage', 'marketing_text', 'product_attributes')

    name = db_sql.Column(db_sql.String(255), unique=True, nullable=False)
    description = db_sql.Column(db_sql.String(255), unique=False, nullable=True)

    gtin = db_sql.Column(db_sql.String(255), unique=False, nullable=True)
    tpnb = db_sql.Column(db_sql.String(255), unique=False, nullable=True)
    tpnc = db_sql.Column(db_sql.String(255), unique=False, nullable=True)
    brand = db_sql.Column(db_sql.String(255), unique=False, nullable=True)

    quantity_contents = db_sql.Column(JsonEncodedDict, unique=False, nullable=True)
    product_characteristics = db_sql.Column(JsonEncodedDict, unique=False, nullable=True)
    package_dimensions = db_sql.Column(JsonEncodedDict, unique=False, nullable=True)
    ingredients = db_sql.Column(JsonEncodedDict, unique=False, nullable=True)
    gda = db_sql.Column(JsonEncodedDict, unique=False, nullable=True)
    calculated_nutrition = db_sql.Column(JsonEncodedDict, unique=False, nullable=True)
    allergen_advice = db_sql.Column(JsonEncodedDict, unique=False, nullable=True)
    safety = db_sql.Column(JsonEncodedDict, unique=False, nullable=True)
    storage = db_sql.Column(JsonEncodedDict, unique=False, nullable=True)
    marketing_text = db_sql.Column(db_sql.String(255), unique=False, nullable=True)
    product_attributes = db_sql.Column(JsonEncodedDict, unique=False, nullable=True)

    def __init__(self, name, description, **kwargs):
        super().__init__()
        self.name = name
        self.description = description

        for received_param in set(kwargs).intersection(set(self.__optional_params)):
            setattr(self, received_param, kwargs.get(received_param))

        if self.auto_save:
            self.save()
