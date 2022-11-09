var reverse = false

if (reverse) {
    var math_prereqs = {
        "MATH1210": [
            "MATH1220"
        ],
        "MATH1310": [
            "MATH1320"
        ],
        "MATH1320": [
            "MATH2310",
            "MATH3000",
            "MATH3100",
            "MATH3250",
            "MATH4040",
            "MATH5080"
        ],
        "MATH3000": [
            "MATH4040",
            "MATH4140",
            "MATH5080"
        ],
        "MATH3310": [
            "MATH4040",
            "MATH4140",
            "MATH4310",
            "MATH4770",
            "MATH4250",
            "MATH5080"
        ],
        "MATH3354": [
            "MATH4040",
            "MATH4652",
            "MATH4750",
            "MATH5030"
        ],
        "MATH3100": [
            "MATH4110",
            "MATH4140"
        ],
        "MATH3351": [
            "MATH4140",
            "MATH4220",
            "MATH4720",
            "MATH4770",
            "MATH4250",
            "MATH4652",
            "MATH4750",
            "MATH5080",
            "MATH5700"
        ],
        "MATH3250": [
            "MATH4220",
            "MATH4300",
            "MATH4720"
        ],
        "MATH2310": [
            "MATH4720",
            "MATH4770",
            "MATH4330",
            "MATH4750",
            "MATH5030",
            "MATH5700"
        ],
        "MATH7340": [
            "MATH7410"
        ],
        "MATH7310": [
            "MATH7410"
        ],
        "MATH5651": [
            "MATH7751",
            "MATH7752"
        ],
        "MATH5652": [
            "MATH7751",
            "MATH7752"
        ],
        "MATH5310": [
            "MATH7820",
            "MATH7310"
        ],
        "MATH5770": [
            "MATH7820",
            "MATH7800"
        ],
        "APMA3080": [
            "MATH4250"
        ],
        "MATH2315": [
            "MATH4330"
        ],
        "MATH4651": [
            "MATH4652"
        ],
        "MATH5352": [
            "MATH7800"
        ]
    }
} else {
    var math_prereqs = {
        "MATH1140": [],
        "MATH1190": [],
        "MATH1210": [],
        "MATH1220": [
            [
                "MATH1210"
            ]
        ],
        "MATH1310": [],
        "MATH1320": [
            [
                "MATH1310"
            ]
        ],
        "MATH2310": [
            [
                "MATH1320"
            ]
        ],
        "MATH2315": [],
        "MATH3000": [
            [
                "MATH1320"
            ]
        ],
        "MATH3100": [
            [
                "MATH1320"
            ]
        ],
        "MATH3250": [
            [
                "MATH1320"
            ]
        ],
        "MATH3310": [],
        "MATH3350": [],
        "MATH3351": [],
        "MATH3354": [],
        "MATH4900": [],
        "MATH4993": [],
        "MATH8999": [],
        "MATH9995": [],
        "MATH9998": [],
        "MATH9999": [],
        "MATH1150": [],
        "MATH3340": [],
        "MATH4040": [
            [
                "MATH1320"
            ],
            [
                "MATH3000",
                "MATH3310",
                "MATH3354"
            ]
        ],
        "MATH4110": [
            [
                "MATH3100"
            ]
        ],
        "MATH4140": [
            [
                "MATH3100",
                "MATH3351"
            ],
            [
                "MATH3000",
                "MATH3310"
            ]
        ],
        "MATH4220": [
            [
                "MATH3250"
            ],
            [
                "MATH3351"
            ]
        ],
        "MATH4300": [
            [
                "MATH3250"
            ]
        ],
        "MATH4310": [
            [
                "MATH3310"
            ]
        ],
        "MATH4651": [],
        "MATH4720": [
            [
                "MATH2310",
                "MATH3250"
            ],
            [
                "MATH3351"
            ]
        ],
        "MATH4770": [
            [
                "MATH2310",
                "MATH3310"
            ],
            [
                "MATH3351"
            ]
        ],
        "MATH5653": [],
        "MATH5896": [],
        "MATH7000": [],
        "MATH7340": [],
        "MATH7370": [],
        "MATH7410": [
            [
                "MATH7340"
            ],
            [
                "MATH7310"
            ]
        ],
        "MATH7559": [],
        "MATH7600": [],
        "MATH7751": [
            [
                "MATH5651",
                "MATH5652"
            ]
        ],
        "MATH7810": [],
        "MATH7820": [
            [
                "MATH5310",
                "MATH5770"
            ]
        ],
        "MATH7900": [],
        "MATH8510": [],
        "MATH8559": [],
        "MATH8620": [],
        "MATH8852": [],
        "MATH8855": [],
        "MATH8880": [],
        "MATH8998": [],
        "MATH9010": [],
        "MATH9250": [],
        "MATH9310": [],
        "MATH9360": [],
        "MATH9410": [],
        "MATH9820": [],
        "MATH9950": [],
        "MATH3315": [],
        "MATH4901": [],
        "MATH1110": [],
        "MATH1160": [],
        "MATH4250": [
            [
                "MATH3351",
                "APMA3080"
            ],
            [
                "MATH3310"
            ]
        ],
        "MATH4330": [
            [
                "MATH2310",
                "MATH2315"
            ]
        ],
        "MATH4652": [
            [
                "MATH3351",
                "MATH4651"
            ],
            [
                "MATH3354"
            ]
        ],
        "MATH4660": [],
        "MATH4750": [
            [
                "MATH2310"
            ],
            [
                "MATH3351"
            ],
            [
                "MATH3354"
            ]
        ],
        "MATH4840": [],
        "MATH5030": [
            [
                "MATH2310"
            ],
            [
                "MATH3354"
            ]
        ],
        "MATH5080": [
            [
                "MATH1320",
                "MATH3351"
            ],
            [
                "MATH3000",
                "MATH3310"
            ]
        ],
        "MATH5700": [
            [
                "MATH2310",
                "MATH3351"
            ]
        ],
        "MATH7010": [],
        "MATH7310": [
            [
                "MATH5310"
            ]
        ],
        "MATH7752": [
            [
                "MATH5651",
                "MATH5652"
            ]
        ],
        "MATH7800": [
            [
                "MATH5352",
                "MATH5770"
            ]
        ],
        "MATH7830": [],
        "MATH8310": [],
        "MATH8410": [],
        "MATH8450": [],
        "MATH8720": [],
        "MATH8750": [],
        "MATH8851": [],
        "MATH8853": []
    }
}



var math_classes = ['APMA3080', 'MATH1210', 'MATH1220', 'MATH1310', 'MATH1320', 'MATH2310', 'MATH2315', 'MATH3000', 'MATH3100', 'MATH3250', 'MATH3310', 'MATH3351', 'MATH3354', 'MATH4040', 'MATH4110', 'MATH4140', 'MATH4220', 'MATH4250', 'MATH4300', 'MATH4310', 'MATH4330', 'MATH4651', 'MATH4652', 'MATH4720', 'MATH4750', 'MATH4770', 'MATH5030', 'MATH5080', 'MATH5310', 'MATH5352', 'MATH5651', 'MATH5652', 'MATH5700', 'MATH5770', 'MATH7310', 'MATH7340', 'MATH7410', 'MATH7751', 'MATH7752', 'MATH7800', 'MATH7820']
var math_set = new Set(math_classes)

$(document).ready(function () {

    function getClassName(text) {
        var index = 0
        var lvl = 0

        for (let i = 0; i < text.length; i++) {
            var lvl = parseInt(text.charAt(i))
            if (isNaN(lvl) == false) {
                index = i
                break
            }
        }
        return [text.substring(0, index) + "<br>" + text.substring(index), lvl]
    }

    function getPoint(idName) {
        var target = document.getElementById(idName);
        var radius = $("#" + idName).css("width").slice(0, -2)
        var margin = $("#" + idName).css("height").slice(0, -2)

        radius = parseInt(radius)
        margin = parseInt(margin)

        return [target.offsetLeft + radius + margin / 3, target.offsetTop + radius + margin / 3];
    }

    var major = ""
    var prevLvl = 1
    $("#anchor").append("<div class='level' id='level1'></div>");

    for (let i = 0; i < math_classes.length; i++) {
        var key = math_classes[i]
        var li = getClassName(key)
        var cname = li[0]
        var lvl = li[1]
        var idName = "level" + lvl

        if (prevLvl != lvl) {
            $("#anchor").append("<div class='level' id=" + idName + "></div>");
        }

        $("#" + idName).append("<div class='node' id=" + key + ">" + cname + "</div>");

        prevLvl = lvl
    }

    var i = 0
    if (reverse) {
        for (let [key, value] of Object.entries(math_prereqs)) {
            if (math_set.has(key)) {
                var parentCoords = getPoint(key)

                value.forEach(element => {
                    var childCoords = getPoint(element)
                    var name = "connector" + i

                    $("#anchor-line").append(`
                        <div class="arrow arrow-` + key + `" id="` + name + `">
                            <svg height="3000" width="3000" style="z-index: 2;">
                                <defs>
                                    <marker id="markerArrow" markerWidth="15" markerHeight="13" refX="2" refY="6" orient="auto">
                                        <path d="M2,2 L2,11 L10,6 L2,2" style="fill: #000000;" />
                                    </marker>
                                </defs>
                        
                                <line x1="` + parentCoords[0] + `" y1="` + parentCoords[1] + `" x2="` + childCoords[0] + `" y2="` + childCoords[1] + `" />
                            </svg>
                        </div>
                    `);
                    $("#" + name).css('zIndex', 0)
                    $("#" + name).hide();
                    i += 1
                })

            }
        }
    } else {
        for (let [key, li] of Object.entries(math_prereqs)) {
            if (math_set.has(key)) {
                var parentCoords = getPoint(key)

                li.forEach(values => {
                    values.forEach(element => {
                        var childCoords = getPoint(element)
                        var name = "connector" + i

                        $("#anchor-line").append(`
                            <div class="arrow arrow-` + key + `" id="` + name + `">
                                <svg height="3000" width="3000" style="z-index: 2;">
                                    <defs>
                                        <marker id="markerArrow" markerWidth="15" markerHeight="13" refX="2" refY="6" orient="auto">
                                            <path d="M2,2 L2,11 L10,6 L2,2" style="fill: #000000;" />
                                        </marker>
                                    </defs>
                            
                                    <line x1="` + parentCoords[0] + `" y1="` + parentCoords[1] + `" x2="` + childCoords[0] + `" y2="` + childCoords[1] + `" />
                                </svg>
                            </div>
                        `);
                        $("#" + name).css('zIndex', 0)
                        $("#" + name).hide();
                        i += 1
                    })
                })

            }
        }
    }

    var visited = new Set()
    var tovisit = []
    var blues = {}

    if (reverse) {
        $('.node').click(function () {

            $(".arrow").hide()
            $(".node").css("background-color", "aquamarine")

            idName = String(this.id)
            tovisit.push(idName)
            $(".arrow-" + idName).show()
            blue = 255
            blues = {
                idName: 255
            }

            while (tovisit.length != 0) {
                var parent = tovisit.pop()
                if (blues[parent] == undefined) {
                    blues[parent] = 255
                }
                $(".arrow-" + parent).show()
                $("#" + parent).css("background-color", "rgb(150, " + blues[parent] + ", " + blues[parent] + ")")
                console.log(parent)
                console.log(blues)

                if (math_prereqs[parent] != undefined) {
                    math_prereqs[parent].forEach(child => {
                        if (visited.has(child) == false) {
                            tovisit.push(child)
                            blues[child] = blues[parent] - 50
                        }
                    })
                }
            }

        });
    } else {
        $('.node').click(function () {

            $(".arrow").hide()
            $(".node").css("background-color", "aquamarine")

            idName = String(this.id)
            tovisit.push([idName])
            $(".arrow-" + idName).show()
            blue = 255
            blues = {
                idName: 255
            }

            while (tovisit.length != 0) {
                console.log(tovisit)
                var parents = tovisit.pop()
                parents.forEach(parent => {
                    if (blues[parent] == undefined) {
                        blues[parent] = 255
                    }
                    $(".arrow-" + parent).show()
                    $("#" + parent).css("background-color", "rgb(150, " + blues[parent] + ", " + blues[parent] + ")")

                    if (math_prereqs[parent] != undefined) {
                        math_prereqs[parent].forEach(child => {
                            if (visited.has(child) == false) {
                                tovisit.push(child)
                                blues[child] = blues[parent] - 50
                            }
                        })
                    }
                })
            }

        });
    }

});