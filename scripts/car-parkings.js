/**
 * Created by davojta on 10/31/16.
 */

var geojsonArea = require('geojson-area');


var allSides = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            27.440063059329987,
                            53.85989715516856
                        ],
                        [
                            27.440063059329987,
                            53.86058367863119
                        ],
                        [
                            27.44011402130127,
                            53.86058367863119
                        ],
                        [
                            27.44011402130127,
                            53.85989715516856
                        ],
                        [
                            27.440063059329987,
                            53.85989715516856
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            27.43902236223221,
                            53.860578933115946
                        ],
                        [
                            27.43902236223221,
                            53.86061689722267
                        ],
                        [
                            27.43999868631363,
                            53.86061689722267
                        ],
                        [
                            27.43999868631363,
                            53.860578933115946
                        ],
                        [
                            27.43902236223221,
                            53.860578933115946
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            27.438620030879974,
                            53.85992721057898
                        ],
                        [
                            27.438620030879974,
                            53.86029261936811
                        ],
                        [
                            27.438684403896332,
                            53.86029261936811
                        ],
                        [
                            27.438684403896332,
                            53.85992721057898
                        ],
                        [
                            27.438620030879974,
                            53.85992721057898
                        ]
                    ]
                ]
            }
        }
    ]
}

var allowedSides = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            27.44008183479309,
                            53.859903482625185
                        ],
                        [
                            27.44008183479309,
                            53.860582096792825
                        ],
                        [
                            27.44012475013733,
                            53.860582096792825
                        ],
                        [
                            27.44012475013733,
                            53.859903482625185
                        ],
                        [
                            27.44008183479309,
                            53.859903482625185
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            27.439030408859253,
                            53.860602660686695
                        ],
                        [
                            27.439030408859253,
                            53.86063429742677
                        ],
                        [
                            27.440044283866882,
                            53.86063429742677
                        ],
                        [
                            27.440044283866882,
                            53.860602660686695
                        ],
                        [
                            27.439030408859253,
                            53.860602660686695
                        ]
                    ]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            27.43863075971603,
                            53.85992404685258
                        ],
                        [
                            27.43863075971603,
                            53.86027521902195
                        ],
                        [
                            27.438662946224213,
                            53.86027521902195
                        ],
                        [
                            27.438662946224213,
                            53.85992404685258
                        ],
                        [
                            27.43863075971603,
                            53.85992404685258
                        ]
                    ]
                ]
            }
        }
    ]
}

var arr = [allSides, allowedSides]

console.log('квартир: ', 6*46)
var needPlace = ~~(6*46*0.75*2.3*4.18)
console.log('необходимо машиномест', 6*46*0.75, '; площади под машины: ', needPlace)


arr.forEach(function (geojson) {
    var area = geojsonArea.geometry(geojson.features[0].geometry);

    var sum =  geojson.features
        .map(f => f.geometry)
        .reduce((s, g) => s+= geojsonArea.geometry(g), 0)

    console.log('площадь: ', Math.floor(sum), '; машиноместа: ', ~~(sum/(2.3*4.18)))
    console.log('дефицит: ', 100 - ~~(sum*100 / needPlace))
})

