FORMAT: 1A
HOST: https://query-stage.copyrighthub.org

# Open Permissions Platform Query Service
The Query Service allows read access of entity information across multiple repositories.

## Standard error output
On endpoint failure there is a standard way to report errors.
The output should be of the form

| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| errors   | A list of errors          | array  |

### Error
| Property         | Description                                 | Type   | Mandatory |
| :-------         | :----------                                 | :---   | :-------  |
| source           | The name of the service producing the error | string | yes       |
| source_id_type   | The type of the source identity             | string | no        |
| source_id        | The source id                               | string | no        |
| message          | A description of the error                  | string | yes       |

# Group Query Service Information

## Query service information [/v1/query]

### Retrieve service information [GET]

#### Output
| Property | Description               | Type   |
| :------- | :----------               | :---   |
| status   | The status of the request | number |
| data     | The service information   | object |

##### Service information
| Property     | Description                    | Type   |
| :-------     | :----------                    | :---   |
| service_name | The name of the api service    | string |
| service_id   | The id of the api service      | string |
| version      | The version of the api service | string |


+ Request
    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)
    + Headers

            Access-Control-Allow-Origin: *

    + Body

            {
                "status": 200,
                "data": {
                    "service_name": "Open Permissions Platform Query Service",
                    "service_id": "d8936d2ae20f11e597309a79f06e9478",
                    "version": "0.1.0"
                }
            }

# Group Entities

## Entity Id Query [/v1/query/entities/{repository_id}/{entity_type}/{entity_id}/]

+ Parameters
    + repository_id (required, string)  ... The repository where the entity is stored
    + entity_type (required, enum[string])
        The type of entity that is being queried (offer, agreement, asset)
        + Members
            + `offer`
            + `agreement`
            + `asset`
    + entity_id (required, string)  ... The id of the entity in the repository


### Get an entity using an entity ID [GET]

#### Output
| Property | Description                  | Type   |
| :------- | :----------                  | :---   |
| status   | The status of the request    | number |
| data     | The entity in JSON-LD format | object |


+ Request Entity (application/json)

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "@context": {
                        "duty": {
                            "type": "@id",
                            "@container": "@set"
                        },
                        "owl": "http://www.w3.org/2002/07/owl#",
                        "@vocab": "http://www.w3.org/ns/odrl/2/",
                        "hub": "http://openpermissions.org/ns/hub/",
                        "constraint": {
                            "type": "@id",
                            "@container": "@set"
                        },
                        "dct": "http://purl.org/dc/terms/",
                        "@language": "en",
                        "dc": "http://purl.org/dc/elements/1.1/",
                        "olex": "http://openpermissions.org/ns/olex/1.0/",
                        "ol:alsoIdentifiedBy": {
                            "type": "@id",
                            "@container": "@set"
                        },
                        "odrl": "http://www.w3.org/ns/odrl/2/",
                        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                        "prohibition": {
                            "type": "@id",
                            "@container": "@set"
                        },
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "ol": "http://openpermissions.org/ns/ol/1.1/",
                        "id": "http://openpermissions.org/ns/id/",
                        "permission": {
                            "type": "@id",
                            "@container": "@set"
                        },
                        "ol:sharedDuties": {
                            "type": "@id",
                            "@container": "@set"
                        }
                    },
                    "@graph": [{
                        "duty": [
                            {
                                "@id": "id:dae3ca88c9ab4550bbcee20d9190fd3d"
                            }
                        ],
                        "profile": "http://openpermissions.org/ns/ol/1.1/",
                        "undefined": {
                            "@id": "odrl:invalid"
                        },
                        "permission": [
                            {
                                "@id": "id:4c079952d508457fa648193a02dc87d8"
                            }
                        ],
                        "dct:created": {
                            "@type": "xsd:dateTime",
                            "@value": "2016-03-03T16:28:00+00:00"
                        },
                        "dct:modified": {
                            "@type": "xsd:dateTime",
                            "@value": "2016-03-03T16:29:00+00:00"
                        },
                        "inheritAllowed": false,
                        "@id": "id:d56e6acc5f1d458c9baf4eae8db9a967",
                        "uid": "4c493369e9d44b478fec697eab190a5d",
                        "ol:policyDescription": "This Licence Offer is for the display of a single photograph as 'wallpaper' or similar background on a personal digital device such as a mobile phone, laptop computer or camera roll. The Licence Holder must be an individual (not an organization).",
                        "type": "offer",
                        "@type": [
                            "Policy",
                            "ol:Policy",
                            "Asset",
                            "Offer"
                        ],
                        "conflict": {
                            "@id": "odrl:invalid"
                        },
                        "target": {
                            "@id": "id:3f9811703d374504b2c4f9b931998240"
                        }
                    },
                    {
                        "action": {
                            "@id": "odrl:compensate"
                        },
                        "@id": "id:dae3ca88c9ab4550bbcee20d9190fd3d",
                        "@type": [
                            "Rule",
                            "Duty"
                        ],
                        "assigner": {
                            "@id": "id:7195cf0ddf314f5cbc92da72b40ffadc"
                        },
                        "constraint": [
                            {
                                "@id": "id:79f9e44a36bd4170b4e266cd0e7d7d98"
                            }
                        ]
                    },
                    {
                        "action": {
                            "@id": "odrl:attribute"
                        },
                        "@id": "id:463c5eb7b43f48eb8adad32ba65c6314",
                        "@type": [
                            "Duty",
                            "Rule"
                        ],
                        "target": {
                            "@id": "id:fc6ea20a8ce4447f98d1e0b75b506c0e"
                        }
                    },
                    {
                        "operator": {
                            "@id": "odrl:lteq"
                        },
                        "post": 1,
                        "@id": "id:5241a13af23e414c9bc62b955e517b9d",
                        "@type": "Constraint"
                    },
                    {
                        "duty": [
                            {
                                "@id": "id:463c5eb7b43f48eb8adad32ba65c6314"
                            }
                        ],
                        "assigner": {
                            "@id": "id:7195cf0ddf314f5cbc92da72b40ffadc"
                        },
                        "constraint": [
                            {
                                "@id": "id:4fe82052163549a4993c9623e5dbff37"
                            },
                            {
                                "@id": "id:c3ece0a29b4c4ab6841616c289490260"
                            },
                            {
                                "@id": "id:5241a13af23e414c9bc62b955e517b9d"
                            },
                            {
                                "@id": "id:186c1f0fa06f4198a9e2f007c7c5b716"
                            }
                        ],
                        "action": {
                            "@id": "odrl:display"
                        },
                        "@id": "id:4c079952d508457fa648193a02dc87d8",
                        "@type": [
                            "Rule",
                            "Permission"
                        ]
                    },
                    {
                        "operator": {
                            "@id": "odrl:isPartOf"
                        },
                        "@id": "id:4fe82052163549a4993c9623e5dbff37",
                        "@type": "Constraint",
                        "spatial": {
                            "@id": "http://sws.geonames.org/6295630/"
                        }
                    },
                    {
                        "operator": {
                            "@id": "odrl:eq"
                        },
                        "@id": "id:79f9e44a36bd4170b4e266cd0e7d7d98",
                        "@type": "Constraint",
                        "unit": {
                            "@id": "http://cvx.iptc.org/iso4217a/GBP"
                        },
                        "payAmount": {
                            "@type": "xsd:decimal",
                            "@value": "10"
                        }
                    },
                    {
                        "operator": {
                            "@id": "odrl:lteq"
                        },
                        "@id": "id:186c1f0fa06f4198a9e2f007c7c5b716",
                        "@type": "Constraint",
                        "unit": {
                            "@id": "olex:pixel"
                        },
                        "height": 400
                    }]
                }
            }



+ Request an entity that does not exist (application/json)

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": "404",
                "errors": [
                    {
                        "source": "query",
                        "message": "Not found"
                    }
                ]
            }



## Hub key Query [/v1/query/entities{?hub_key}]

+ Parameters
    + hub_key (required, string)  ... A hub key (schema >= s1)

### Get an entity using a hub key [GET]

#### Output
| Property | Description                  | Type   |
| :------- | :----------                  | :---   |
| status   | The status of the request    | number |
| data     | The entity in JSON-LD format | object |


+ Request Entity (application/json)

+ Response 200 (application/json; charset=UTF-8)

    + Body

            {
                "status": 200,
                "data": {
                    "@context": {
                        "duty": {
                            "type": "@id",
                            "@container": "@set"
                        },
                        "owl": "http://www.w3.org/2002/07/owl#",
                        "@vocab": "http://www.w3.org/ns/odrl/2/",
                        "hub": "http://openpermissions.org/ns/hub/",
                        "constraint": {
                            "type": "@id",
                            "@container": "@set"
                        },
                        "dct": "http://purl.org/dc/terms/",
                        "@language": "en",
                        "dc": "http://purl.org/dc/elements/1.1/",
                        "olex": "http://openpermissions.org/ns/olex/1.0/",
                        "ol:alsoIdentifiedBy": {
                            "type": "@id",
                            "@container": "@set"
                        },
                        "odrl": "http://www.w3.org/ns/odrl/2/",
                        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                        "prohibition": {
                            "type": "@id",
                            "@container": "@set"
                        },
                        "xsd": "http://www.w3.org/2001/XMLSchema#",
                        "ol": "http://openpermissions.org/ns/ol/1.1/",
                        "id": "http://openpermissions.org/ns/id/",
                        "permission": {
                            "type": "@id",
                            "@container": "@set"
                        },
                        "ol:sharedDuties": {
                            "type": "@id",
                            "@container": "@set"
                        }
                    },
                    "@graph": [{
                        "duty": [
                            {
                                "@id": "id:dae3ca88c9ab4550bbcee20d9190fd3d"
                            }
                        ],
                        "profile": "http://openpermissions.org/ns/ol/1.1/",
                        "undefined": {
                            "@id": "odrl:invalid"
                        },
                        "permission": [
                            {
                                "@id": "id:4c079952d508457fa648193a02dc87d8"
                            }
                        ],
                        "dct:created": {
                            "@type": "xsd:dateTime",
                            "@value": "2016-03-03T16:28:00+00:00"
                        },
                        "dct:modified": {
                            "@type": "xsd:dateTime",
                            "@value": "2016-03-03T16:29:00+00:00"
                        },
                        "inheritAllowed": false,
                        "@id": "id:d56e6acc5f1d458c9baf4eae8db9a967",
                        "uid": "4c493369e9d44b478fec697eab190a5d",
                        "ol:policyDescription": "This Licence Offer is for the display of a single photograph as 'wallpaper' or similar background on a personal digital device such as a mobile phone, laptop computer or camera roll. The Licence Holder must be an individual (not an organization).",
                        "type": "offer",
                        "@type": [
                            "Policy",
                            "ol:Policy",
                            "Asset",
                            "Offer"
                        ],
                        "conflict": {
                            "@id": "odrl:invalid"
                        },
                        "target": {
                            "@id": "id:3f9811703d374504b2c4f9b931998240"
                        }
                    },
                    {
                        "action": {
                            "@id": "odrl:compensate"
                        },
                        "@id": "id:dae3ca88c9ab4550bbcee20d9190fd3d",
                        "@type": [
                            "Rule",
                            "Duty"
                        ],
                        "assigner": {
                            "@id": "id:7195cf0ddf314f5cbc92da72b40ffadc"
                        },
                        "constraint": [
                            {
                                "@id": "id:79f9e44a36bd4170b4e266cd0e7d7d98"
                            }
                        ]
                    },
                    {
                        "action": {
                            "@id": "odrl:attribute"
                        },
                        "@id": "id:463c5eb7b43f48eb8adad32ba65c6314",
                        "@type": [
                            "Duty",
                            "Rule"
                        ],
                        "target": {
                            "@id": "id:fc6ea20a8ce4447f98d1e0b75b506c0e"
                        }
                    },
                    {
                        "operator": {
                            "@id": "odrl:lteq"
                        },
                        "post": 1,
                        "@id": "id:5241a13af23e414c9bc62b955e517b9d",
                        "@type": "Constraint"
                    },
                    {
                        "duty": [
                            {
                                "@id": "id:463c5eb7b43f48eb8adad32ba65c6314"
                            }
                        ],
                        "assigner": {
                            "@id": "id:7195cf0ddf314f5cbc92da72b40ffadc"
                        },
                        "constraint": [
                            {
                                "@id": "id:4fe82052163549a4993c9623e5dbff37"
                            },
                            {
                                "@id": "id:c3ece0a29b4c4ab6841616c289490260"
                            },
                            {
                                "@id": "id:5241a13af23e414c9bc62b955e517b9d"
                            },
                            {
                                "@id": "id:186c1f0fa06f4198a9e2f007c7c5b716"
                            }
                        ],
                        "action": {
                            "@id": "odrl:display"
                        },
                        "@id": "id:4c079952d508457fa648193a02dc87d8",
                        "@type": [
                            "Rule",
                            "Permission"
                        ]
                    },
                    {
                        "operator": {
                            "@id": "odrl:isPartOf"
                        },
                        "@id": "id:4fe82052163549a4993c9623e5dbff37",
                        "@type": "Constraint",
                        "spatial": {
                            "@id": "http://sws.geonames.org/6295630/"
                        }
                    },
                    {
                        "operator": {
                            "@id": "odrl:eq"
                        },
                        "@id": "id:79f9e44a36bd4170b4e266cd0e7d7d98",
                        "@type": "Constraint",
                        "unit": {
                            "@id": "http://cvx.iptc.org/iso4217a/GBP"
                        },
                        "payAmount": {
                            "@type": "xsd:decimal",
                            "@value": "10"
                        }
                    },
                    {
                        "operator": {
                            "@id": "odrl:lteq"
                        },
                        "@id": "id:186c1f0fa06f4198a9e2f007c7c5b716",
                        "@type": "Constraint",
                        "unit": {
                            "@id": "olex:pixel"
                        },
                        "height": 400
                    }]
                }
            }


+ Request an entity without providing a hub key (application/json)

+ Response 400 (application/json; charset=UTF-8)

    + Body

            {
                "status": "400",
                "errors": [
                    {
                        "source": "query",
                        "message": "hub_key parameter is required"
                    }
                ]
            }

+ Request an entity with invalid hub key (application/json)

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": "404",
                "errors": [
                    {
                        "source": "query",
                        "message": "Invalid hub key"
                    }
                ]
            }

+ Request an entity with schema s0 hub key (application/json)

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": "404",
                "errors": [
                    {
                        "source": "query",
                        "message": "Only hub keys matching schema >= s1 are supported"
                    }
                ]
            }

+ Request an entity that does not exist (application/json)

+ Response 404 (application/json; charset=UTF-8)

    + Body

            {
                "status": "404",
                "errors": [
                    {
                        "source": "query",
                        "message": "Not found"
                    }
                ]
            }


# Group Assets

## Search for offers [/v1/query/search/offers]

### Search for Assets and their Offers [POST]

#### Input
List of source_id_type and source_id value pairs.

| Property       | Description                    | Type   | Mandatory |
| :-------       | :----------                    | :---   | :----     |
| source_id_type | The type of the asset identity | string | yes       |
| source_id      | The asset identity             | string | yes       |

#### Output
| Property | Description                      | Type   |
| :------- | :----------                      | :---   |
| status   | The status of the request        | number |
| data     | Array of assets and their offers | array  |

Assets not found in database are omitted in data list.

If no offers for the given asset(s) are found, relevant information about external
sources which provide offers can still be contained within the organisation information
held by the Accounts service in the hub. [Please refer to the Accounts service documentation for
how to get reference links](https://github.com/openpermissions/accounts-srv/blob/master/documents/apiary/api.md).


+ Request offers for assets present in database (application/json)
    + Headers

            Accept: application/json

    + Body

            [
                {
                    "source_id_type": "examplecopictureid",
                    "source_id": "100456"
                },
                {
                    "source_id_type": "examplecopictureid",
                    "source_id": "100123"
                }
            ]

+ Response 200 (application/json; charset=UTF-8)
    + Headers

            Access-Control-Allow-Origin: *

    + Body

            {
                "status": 200,
                "data": [
                    {
                        "source_id_type": "examplecopictureid",
                        "source_id": "100456",
                        "offers": [
                            {
                                "profile": "http://digicat.io/ns/ol/1.0/",
                                "policyName": "Non-commercial Website",
                                "policyDescription": "Use an image on a blog or website&lt;br/&gt;&lt;br/&gt;Site does not carry advertising or sell products or services.&lt;br/&gt;Site receives no more than 50,000 views per month&lt;br/&gt;Maximum size of image 400 x 400px.",
                                "hubKey": "https://www.openpermissions.org/s0/hub1/offer/chub/exampleco-offerid/01",
                                "undefined": "http://www.w3.org/ns/odrl/2/invalid",
                                "permission": [
                                    {
                                        "duty": [
                                            {
                                                "action": "http://www.w3.org/ns/odrl/2/attribute",
                                                "target": {
                                                    "description": "This photograph (c) ExampleCo Ltd, all rights reserved."
                                                }
                                            },
                                            {
                                                "target": {
                                                    "predicate": "http://digicat.io/ns/olex/0.1/explicitOffer",
                                                    "hubKey": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/bab1717645504af49e58d864ca59b56a",
                                                    "uid": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/bab1717645504af49e58d864ca59b56a",
                                                    "target_object": "https://www.openpermissions.org/s0/hub1/offer/chub/exampleco-offerid/01"
                                                },
                                                "assigner": "https://www.openpermissions.org/s0/hub1/party/chub/pid/exampleco",
                                                "constraint": [
                                                    {
                                                    "operator": "http://www.w3.org/ns/odrl/2/eq",
                                                    "unit": "http://cvx.iptc.org/iso4217a/GBP",
                                                    "payAmount": "1"
                                                    }
                                                ],
                                                "action": "http://www.w3.org/ns/odrl/2/compensate"
                                            }
                                        ],
                                        "target": {
                                            "predicate": "http://digicat.io/ns/olex/0.1/explicitOffer",
                                            "hubKey": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/bab1717645504af49e58d864ca59b56a",
                                            "uid": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/bab1717645504af49e58d864ca59b56a",
                                            "target_object": "https://www.openpermissions.org/s0/hub1/offer/chub/exampleco-offerid/01"
                                        },
                                        "assigner": "https://www.openpermissions.org/s0/hub1/party/chub/pid/exampleco",
                                        "constraint": [
                                            {
                                                "operator": "http://www.w3.org/ns/odrl/2/lteq",
                                                "width": 400,
                                                "unit": "http://digicat.io/ns/ol/1.0/pixel"
                                            },
                                            {
                                                "operator": "http://www.w3.org/ns/odrl/2/lteq",
                                                "unit": "http://digicat.io/ns/ol/1.0/pixel",
                                                "height": 400
                                            },
                                            {
                                                "views": 50000,
                                                "host": {
                                                    "hubKey": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/fb0a704d48e149829cdc0ed7a5557be7",
                                                    "uid": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/fb0a704d48e149829cdc0ed7a5557be7",
                                                    "purpose": "http://digicat.io/ns/ol/1.0/non_commercial_purpose",
                                                    "description": "Blog, website, no advertising."
                                                },
                                                "operator": "http://www.w3.org/ns/odrl/2/lteq",
                                                "unit": "http://digicat.io/ns/ol/1.0/visitorsPerMonth"
                                            },
                                            {
                                                "operator": "http://www.w3.org/ns/odrl/2/lteq",
                                                "post": 1,
                                                "host": {
                                                    "hubKey": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/fb0a704d48e149829cdc0ed7a5557be7",
                                                    "uid": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/fb0a704d48e149829cdc0ed7a5557be7",
                                                    "purpose": "http://digicat.io/ns/ol/1.0/non_commercial_purpose",
                                                    "description": "Blog, website, no advertising."
                                                }
                                            },
                                            {
                                                "operator": "http://www.w3.org/ns/odrl/2/isPartOf",
                                                "spatial": "http://digicat.io/ns/ol/1.0/World"
                                            }
                                        ],
                                        "action": "http://www.w3.org/ns/odrl/2/display"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "source_id_type": "examplecopictureid",
                        "source_id": "100123",
                        "hub_key": ""https://openpermissions.org/s0/hub1/asset/exampleco/examplecopictureid/100123",
                        "offers": [
                            {
                                "profile": "http://digicat.io/ns/ol/1.0/",
                                "policyName": "Non-commercial Website",
                                "policyDescription": "Use an image on a blog or website&lt;br/&gt;&lt;br/&gt;Site does not carry advertising or sell products or services.&lt;br/&gt;Site receives no more than 50,000 views per month&lt;br/&gt;Maximum size of image 400 x 400px.",
                                "hubKey": "https://www.openpermissions.org/s0/hub1/offer/chub/exampleco-offerid/01",
                                "undefined": "http://www.w3.org/ns/odrl/2/invalid",
                                "permission": [
                                    {
                                        "duty": [
                                            {
                                                "action": "http://www.w3.org/ns/odrl/2/attribute",
                                                "target": {
                                                    "description": "This photograph (c) ExampleCo Ltd, all rights reserved."
                                                }
                                            },
                                            {
                                                "target": {
                                                    "predicate": "http://digicat.io/ns/olex/0.1/explicitOffer",
                                                    "hubKey": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/bab1717645504af49e58d864ca59b56a",
                                                    "uid": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/bab1717645504af49e58d864ca59b56a",
                                                    "target_object": "https://www.openpermissions.org/s0/hub1/offer/chub/exampleco-offerid/01"
                                                },
                                                "assigner": "https://www.openpermissions.org/s0/hub1/party/chub/pid/exampleco",
                                                "constraint": [
                                                    {
                                                    "operator": "http://www.w3.org/ns/odrl/2/eq",
                                                    "unit": "http://cvx.iptc.org/iso4217a/GBP",
                                                    "payAmount": "1"
                                                    }
                                                ],
                                                "action": "http://www.w3.org/ns/odrl/2/compensate"
                                            }
                                        ],
                                        "target": {
                                            "predicate": "http://digicat.io/ns/olex/0.1/explicitOffer",
                                            "hubKey": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/bab1717645504af49e58d864ca59b56a",
                                            "uid": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/bab1717645504af49e58d864ca59b56a",
                                            "target_object": "https://www.openpermissions.org/s0/hub1/offer/chub/exampleco-offerid/01"
                                        },
                                        "assigner": "https://www.openpermissions.org/s0/hub1/party/chub/pid/exampleco",
                                        "constraint": [
                                            {
                                                "operator": "http://www.w3.org/ns/odrl/2/lteq",
                                                "width": 400,
                                                "unit": "http://digicat.io/ns/ol/1.0/pixel"
                                            },
                                            {
                                                "operator": "http://www.w3.org/ns/odrl/2/lteq",
                                                "unit": "http://digicat.io/ns/ol/1.0/pixel",
                                                "height": 400
                                            },
                                            {
                                                "views": 50000,
                                                "host": {
                                                    "hubKey": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/fb0a704d48e149829cdc0ed7a5557be7",
                                                    "uid": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/fb0a704d48e149829cdc0ed7a5557be7",
                                                    "purpose": "http://digicat.io/ns/ol/1.0/non_commercial_purpose",
                                                    "description": "Blog, website, no advertising."
                                                },
                                                "operator": "http://www.w3.org/ns/odrl/2/lteq",
                                                "unit": "http://digicat.io/ns/ol/1.0/visitorsPerMonth"
                                            },
                                            {
                                                "operator": "http://www.w3.org/ns/odrl/2/lteq",
                                                "post": 1,
                                                "host": {
                                                    "hubKey": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/fb0a704d48e149829cdc0ed7a5557be7",
                                                    "uid": "https://www.openpermissions.org/s0/hub1/asset/chub/uuid/fb0a704d48e149829cdc0ed7a5557be7",
                                                    "purpose": "http://digicat.io/ns/ol/1.0/non_commercial_purpose",
                                                    "description": "Blog, website, no advertising."
                                                }
                                            },
                                            {
                                                "operator": "http://www.w3.org/ns/odrl/2/isPartOf",
                                                "spatial": "http://digicat.io/ns/ol/1.0/World"
                                            }
                                        ],
                                        "action": "http://www.w3.org/ns/odrl/2/display"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }


+ Request offers for assets not present in database (application/json)
    + Headers

            Accept: application/json

    + Body

            [
                {
                    "source_id_type": "exampleco",
                    "source_id": "NonExistingIDvalue1"
                },
                {
                    "source_id_type": "exampleco",
                    "source_id": "NonExistingIDvalue2"
                }
            ]

+ Response 200 (application/json; charset=UTF-8)
    + Headers

            Access-Control-Allow-Origin: *

    + Body

            {
                "status": "200",
                "data": []
            }


+ Request offers with invalid data (application/json)
    + Headers

            Accept: application/json

    + Body

            ...invalid data...

+ Response 400 (application/json; charset=UTF-8)
    + Headers

            Access-Control-Allow-Origin: *

    + Body

            {
                "status": "400",
                "errors": [
                    {
                        "source": "repository",
                        "message": "No JSON object could be decoded"
                    }
                ]
            }


+ Request offers with missing data (application/json)
    + Headers

            Accept: application/json

+ Response 400 (application/json; charset=UTF-8)
    + Headers

            Access-Control-Allow-Origin: *

    + Body


            {
                "status": "400",
                "errors": [
                    {
                        "source": "repository",
                        "message": "No JSON object could be decoded"
                    }
                ]
            }


# Group Licensors

## Licensors of an asset [/v1/query/licensors{?source_id_type}{?source_id}]

Note: this endpoint uses query parameters instead of a RESTful URL structure
(like `{source_id_type}/{source_id}/licensors`) because both source ID and type
may be strings that look odd in a URL path (e.g. source ID could be a URL).


+ Parameters
    + source_id_type (required, string)  ... The type of the asset identity
    + source_id (required, string)  ... The asset identity

### Retrieve Licensors of an asset [GET]

#### Output
| Property | Description                      | Type   |
| :------- | :----------                      | :---   |
| status   | The status of the request        | number |
| data     | Array of Licensors for the asset | array  |

+ Request Licensor data for an asset present in database
    + Headers

            Accept: application/json

+ Response 200 (application/json; charset=UTF-8)
    + Headers

            Access-Control-Allow-Origin: *

    + Body

            {
                "status": 200,
                "data": [
                    {
                        "organisation_id": "examplecopicturelibrary",
                        "name": "repo",
                        "created_by": "testadmin",
                        "state": "approved"
                    }
                ]
            }

+ Request Licensor data with missing source_id or source_id_type
    + Headers

            Accept: application/json

+ Response 400 (application/json; charset=UTF-8)
    + Headers

            Access-Control-Allow-Origin: *

    + Body

            {
                "status": "400",
                "errors": [
                    {
                        "source": "repository",
                        "message": "Must have "source_id_type" and "source_id" parameters"
                    }
                ]
            }


+ Request Licensor data with invalid source_id/source_id_type pair
    + Headers

            Accept: application/json

+ Response 400 (application/json; charset=UTF-8)
    + Headers

            Access-Control-Allow-Origin: *

    + Body

            {
                "status": "400",
                "errors": [
                    {
                        "source": "repository",
                        "message": "source_id is an invalid hub key"
                    }
                ]
            }

+ Request Licensor data for assets not found in database
    + Headers

            Accept: application/json

+ Response 404 (application/json; charset=UTF-8)
    + Headers

            Access-Control-Allow-Origin: *

    + Body

            {
                "status": "404",
                "errors": [
                    {
                        "source": "repository",
                        "message": "Not found"
                    }
                ]
            }
