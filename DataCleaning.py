

"""
    Program Name: DataCleaning.py
    Author Name:  Alyssa Fedgo and Megha Sudhakaran
    Date:         May 21, 2021
    Project:      WIDS2021: Predict electric load based on factors such as weather, GDP, population size
    Purpose:      To merge the input data sets and fill out missing information for weather
"""


import pandas as pd
import numpy as np
from datetime import datetime
from pytz import UTC
from pytz import timezone
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

#Alyssa's code


""" Read in the data sets """


ercot=pd.read_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\ercot_hourly_load.csv')

covid_conf=pd.read_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\texas_covid_confirmed.csv', parse_dates=['Date'])

covid_death=pd.read_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\texas_covid_deaths.csv', parse_dates=['Date'])

gdp=pd.read_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\Gdp.csv')

pop_density=pd.read_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\Population_Density.csv')
    
weather_history=pd.read_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\weather_history.csv',parse_dates=['date'])

#Dictionary for cities to region

cities={
    "Coast":[
        "Ace","Alvin","Anahuac","Angleton","Bacliff","Batson","Bay City","Baytown","Beasley","Beaumont","Bellaire",
        "Bellville","Blessing","Bloomington","Boling", "Bon Wier","Brazoria","Bridge City","Brookshire","Buna",
        "Burkeville","Call","Camden","Cedar Lane","Channelview","Chester","China","Cleveland","Clute","Coldspring",
        "Collegeport","Colmesneil","Conroe","Corrigan","Crosby","Cypress","Daisetta","Damon","Danbury","Danevang",
        "Dayton","Deer Park","Devers","Deweyville","Dickinson", "Doucette","Eagle Lake","East Bernard","Edna","Egypt",
        "El Campo","Elmaton","Evadale","Francitas","Fred","Freeport","Fresno","Friendswood", "Fulshear","Galena Park",
        "Galveston","Ganado","Gilchrist","Glen Flora","Goodrich","Groves","Guy","Hamshire","Hankamer","Hardin","Hempstead",
        "High Island","Highlands","Hillister","Hitchcock","Hockley", "Houston","Huffman","Hull", "Humble","Hungerford",
        "Inez","Jasper","Katy","Kemah","Kendleton","Kingwood","Kirbyville", "Kountze","La Marque","La Porte","La Salle",
        "La Ward","Lake Jackson", "Lane City","League City", "Leggett", "Liberty","Lissie","Liverpool","Livingston",
        "Lolita","Louise","Lumberton","Magnolia", "Manvel","Markham","Matagorda","Mcfaddin","Midfield","Missouri City",
        "Mont Belvieu","Montgomery","Moscow","Nederland","Needville","New Caney","Newton","Nome","Nursery","Oakhurst",
        "Onalaska", "Orange","Orchard","Palacios","Pasadena","Pattison","Pearland", "Pierce","Pinehurst","Placedo",
        "Pledger","Point Comfort","Pointblank","Port Arthur","Port Bolivar","Port Lavaca","Port Neches", "Port O'Connor",
        "Porter","Prairie View","Richmond","Romayor","Rosenberg","Rosharon","Rye","Sabine Pass","San Felipe","Santa Fe",
        "Saratoga","Seabrook","Seadrift","Sealy","Shepherd","Sheridan","Silsbee","Simonton","Sour Lake", "South Houston",
        "Splendora","Spring", "Spurger","Stafford", "Stowell","Sugar Land", "Sweeny", "Telferner","Texas City",  "Thicket",
        "Thompsons","Tomball","Van Vleck",  "Vanderbilt","Victoria", "Vidor","Village Mills",  "Votaw","Wadsworth", "Waller",
        "Wallis","Wallisville",  "Warren", "Webster", "West Columbia","Wharton","Wiergate", "Willis","Winnie","Woodville"
        ],
    "East":[
        "Alto","Anderson","Apple Springs", "Arp", "Athens",  "Atlanta","Avinger","Beckville",  "Bedias","Ben Wheeler",
        "Big Sandy","Bivins","Bloomburg","Brashear","Bremond","Bronson","Brookeland","Brownsboro","Bryan","Buffalo",
        "Bullard","Calvert","Canton","Carthage","Cayuga","Center","Centerville","Chandler","Chireno","College Station",
        "Como","Cookville","Crockett","Cumby","Cuney","Cushing","Daingerfield","De Berry","Diana","Diboll","Dike","Donie",
        "Douglass","Douglassville","Edgewood","Elkhart",  "Emory", "Etoile","Eustace","Fairfield", "Flint", "Flynn",
        "Franklin","Frankston","Fruitvale","Gallatin","Garrison","Gary","Gilmer","Grand Saline","Grapeland", "Groveton",
        "Hearne","Hemphill","Henderson","Hughes Springs", "Huntington", "Iola","Jacksonville","Jefferson",   "Jewett",
        "Joaquin",  "Kennard","Kildare","Kirvin","Laneville","Larue",  "Latexo", "Leesburg",     "Leona","Lindale","Linden",
        "Lone Star","Long Branch","Lovelady","Lufkin","Madisonville",    "Malakoff","Marietta","Marquez","McLeod", "Midway",
        "Milam","Montalba","Mount Enterprise", "Mount Pleasant", "Mount Vernon","Mumford","Murchison","Nacogdoches","Naples",
        "Navasota","Neches","New London","New Summerfield","Normangee","North Zulch","Oakwood", "Omaha","Ore City","Overton",
        "Palestine","Pennington","Pickton","Pineland","Pittsburg","Plantersville",  "Point", "Pollok","Queen City","Quitman",
        "Ratcliff","Reklaw","Richards","Rusk","Sacul","Saltillo", "Scroggins","Shelbyville","Shiro","Streetman","Sulphur Bluff",
        "Sulphur Springs", "Talco","Tatum","Teague", "Tenaha", "Tennessee Colony", "Timpson","Trinidad",  "Trinity","Troup",
        "Tyler","Van","Waskom","Wells","Whitehouse", "Wills Point","Winfield","Winona","Woden","Wortham","Yantis","Zavalla"
        ],
    "Far West":[
        "Ackerly","Alpine","Andrews","Anthony","Balmorhea","Barstow","Big Bend National Park","Big Lake","Big Spring",
        "Canutillo","Clint","Coahoma","Coyanosa","Crane","Dell City","Dryden","El Paso","Fabens","Forsan","Fort Bliss",
        "Fort Davis","Fort Hancock","Fort Stockton", "Gail","Garden City","Gardendale","Goldsmith","Grandfalls", "Imperial",
        "Iraan","Kermit","Knott","Lamesa","Lenorah", "Marathon","Marfa","McCamey", "Mentone","Midkiff", "Midland","Monahans",
        "Notrees","Odessa","Odonnell","Orla","Ozona","Pecos","Presidio","Pyote","Rankin","Redford","Salt Flat","San Elizario",
        "Sanderson","Saragosa","Sheffield","Sierra Blanca","Stanton", "Tarzan","Terlingua","Tornillo", "Toyah","Valentine",
        "Van Horn","Welch", "Wickett","Wink"
        ],
    "North":[
        "Afton","Allison","Annona","Archer City","Arthur City","Aspermont","Avery","Bagwell","Bailey","Bellevue",
        "Bells","Benjamin","Blossom","Bogata","Bonham","Bowie", "Briscoe","Brookston","Burkburnett","Byers","Childress",
        "Chillicothe","Clarendon","Clarksville","Collinsville","Crosbyton","Crowell",  "De Kalb","Denison",  "Deport",
        "Detroit","Dickens", "Dodd City","Ector","Electra","Era","Estelline", "Flomot","Forestburg", "Gainesville","Girard",
        "Gordonville","Goree","Gunter","Guthrie","Harrold","Haskell","Hedley", "Henrietta","Holliday","Honey Grove","Hooks",
        "Howe","Iowa Park","Ivanhoe","Jayton","Knox City",  "Ladonia",
        "Lakeview","Lelia Lake","Leonard","Lindsay","Lorenzo","Matador","Maud","Mcadoo","Megargel","Memphis","Mobeetie",
        "Montague","Muenster","Munday","Myra","Nash","New Boston","Nocona","O'Brien","Odell","Oklaunion","Old Glory",
        "Paducah","Paris","Pattonville","Petrolia","Petty","Pottsboro","Powderly","Quanah","Quitaque","Ralls", "Randolph",
        "Ravenna","Redwater","Ringgold","Roaring Springs","Rochester","Rosston","Roxton","Rule","Sadler","Saint Jo","Savoy",
        "Scotland","Seymour","Shamrock","Sheppard Afb","Sherman","Silverton","Simms","Southmayd", "Spur","Sumner","Sunset",
        "Telephone","Tell","Texarkana","Tioga","Tom Bean", "Trenton","Turkey","Valley View","Van Alstyne","Vernon","Weinert",
        "Wheeler","Whitesboro","Whitewright","Wichita Falls", "Windom","Windthorst"
             ],
    "North Central":[
        "Abbott","Addison", "Albany","Aledo","Allen","Alvarado","Alvord","Anna","Aquilla","Argyle","Arlington",
        "Aubrey","Avalon","Axtell","Azle","Baird", "Balch Springs","Bangs","Bardwell","Barry","Bartlett","Bedford","Belton",
        "Ben Franklin","Blanket","Blooming Grove","Blue Ridge","Bluff Dale","Blum",  "Boyd","Brandon","Breckenridge",
        "Bridgeport","Brookesmith","Brownwood","Bruceville","Bryson","Burleson","Bynum","Caddo","Caddo Mills","Campbell",
        "Carbon","Carlton","Carrollton","Cedar Hill", "Celeste","Celina","Chatfield","Chico","Chilton","China Spring",
        "Cisco","Cleburne","Clifton","Clyde","Colleyville","Comanche", "Commerce","Coolidge","Cooper", "Coppell",
        "Copperas Cove","Corsicana","Covington","Crandall","Cranfills Gap","Crawford","Cresson","Cross Plains","Crowley",
        "Dallas","Dawson","De Leon","Decatur","Denton","Desdemona","Desoto", "Dublin","Duncanville","Early","Eastland",
        "Eddy","Elm Mott","Energy","Enloe","Ennis","Euless","Evant","Farmersville","Fate", "Ferris","Flower Mound","Forney",
        "Forreston","Fort Hood","Fort Worth","Frisco","Frost","Garland","Gatesville","Glen Rose","Godley","Goldthwaite",
        "Gordon","Gorman","Graford","Graham","Granbury", "Grand Prairie","Grandview","Grapevine","Greenville","Groesbeck",
        "Gustine","Haltom City","Hamilton","Harker Heights","Haslet","Hewitt","Hico","Hillsboro","Holland","Hubbard",
        "Hurst","Hutchins", "Iredell","Irene","Irving","Italy","Itasca","Jacksboro","Jermyn", "Jonesboro","Josephine",
        "Joshua","Justin","Kaufman","Keene","Keller","Kemp","Kennedale","Kerens","Killeen","Klondike","Kopperl","Kosse",
        "Krum","Lake Creek","Lake Dallas","Lancaster","Lavon","Leroy", "Lewisville","Lillian","Lipan","Little Elm",
        "Little River Academy","Lone Oak","Lorena","Lott", "Loving","Mabank","Malone","Mansfield","Marlin","Mart", "May",
        "Maypearl","McGregor","Mckinney","Melissa","Meridian","Mertens","Mesquite",  "Mexia","Midlothian","Milford","Millsap",
        "Mineral Wells","Mingus","Moody", "Moran","Morgan", "Mount Calm","Mullin",   "Naval Air Station Jrb","Nemo","Nevada",
        "Newark","Newcastle","Nolanville","North Richland Hills","Oglesby","Olden","Olney","Palmer","Palo Pinto","Paradise",
        "Pecan Gap", "Penelope","Perrin", "Pilot Point","Plano","Ponder","Poolville","Pottsville","Powell","Prairie Hill",
        "Priddy","Princeton","Prosper","Purdon","Purmela","Putnam","Quinlan","Rainbow","Ranger","Reagan","Red Oak",
        "Rhome","Rice","Richardson","Richland","Riesel","Rio Vista","Rising Star","Roanoke","Rockwall","Rogers","Rosebud",
        "Rosser","Rowlett","Royse City","Sachse","Salado","Sanger","Santo","Satin","Scurry","Seagoville","Sidney",
        "South Bend","Southlake","Springtown","Stephenville","Strawn", "Sunnyvale","Tehuacana","Temple", "Terrell",
        "The Colony","Thornton", "Throckmorton","Tolar","Troy","Valley Mills","Venus",  "Waco","Walnut Springs",
        "Waxahachie","Weatherford","West","Whitney","Whitt","Wilmer", "Wolfe City",  "Woodson","Woodway","Wylie","Zephyr"
        ],
    "South":[
        "Agua Dulce","Alamo","Alice", "Aransas Pass",  "Armstrong","Artesia Wells","Asherton","Austwell","Banquete",
        "Batesville", "Bayside","Beeville","Ben Bolt","Benavides","Berclair","Big Wells", "Bigfoot","Bishop","Brownsville",
        "Bruni","Calliham","Campbellton","Carrizo Springs","Catarina","Charlotte","Christine","Combes","Concepcion",
        "Corpus Christi","Cotulla","Crystal City","Delmita","Dilley","Donna","Driscoll","Eagle Pass","Edcouch","Edinburg",
        "Edroy","El Indio","Elsa","Encinal","Encino","Falcon Heights","Falfurrias","Fannin","Fowlerton", "Freer","Fulton",
        "George West","Goliad","Gregory","Grulla", "Hargill","Harlingen","Hebbronville","Hidalgo",  "Ingleside","Jourdanton",
        "Kingsville","La Blanca","La Feria","La Joya","La Pryor","La Villa","Laredo","Lasara","Leming","Linn", "Lopeno",
        "Los Ebanos","Los Fresnos","Los Indios","Lyford","Lytle","Mathis","Mcallen","Mercedes","Mineral","Mirando City",
        "Mission","Moore","Normanna","Oakville","Odem","Oilton","Olmito","Orange Grove", "Pawnee","Pearsall","Penitas",
        "Pettus","Pharr","Pleasanton","Port Aransas","Port Isabel","Port Mansfield","Portland","Poteet","Premont",
        "Progreso","Quemado","Raymondville","Realitos", "Refugio","Rio Grande City","Rio Hondo", "Riviera","Robstown",
        "Rockport","Roma","Salineno","San Benito","San Diego","San Isidro","San Juan","San Perlita","San Ygnacio",
        "Sandia","Santa Elena","Santa Maria","Santa Rosa", "Sarita", "Sebastian", "Sinton","Skidmore","South Padre Island",
        "Sullivan City", "Taft","Three Rivers", "Tilden",  "Tivoli","Tuleta",  "Tynan","Weesatche","Weslaco", "Whitsett",
        "Woodsboro","Zapata"
        ],
    "South Central":[
        "Adkins","Alleyton","Altair","Atascosa","Austin","Bandera","Bastrop","Bergheim","Bertram","Blanco",
        "Bleiblerville","Boerne","Brenham", "Briggs","Buckholts","Buda","Bulverde","Burlington",  "Burnet", "Burton",
        "Caldwell","Cameron","Canyon Lake","Carmine","Castroville","Cat Spring","Cedar Creek","Cedar Park","Chappell Hill",
        "Cibolo","Columbus","Comfort","Converse","Cost", "Coupland","Cuero", "D Hanis","Dale","Davilla",  "Del Valle",
        "Devine","Dime Box","Driftwood","Dripping Springs", "Elgin","Ellinger", "Elmendorf","Falls City","Fayetteville",
        "Fentress","Fischer","Flatonia","Florence","Floresville", "Garwood","Gause","Georgetown","Giddings", "Gillett",
        "Glidden", "Gonzales", "Granger","Hallettsville", "Harwood","Helotes", "Hobson","Hondo", "Horseshoe Bay","Hutto",
        "Hye","Industry", "Jarrell","Jbsa Ft Sam Houston","Jbsa Lackland","Jbsa Randolph","Johnson City","Karnes City",
        "Kendalia","Kenedy","Kingsbury", "Kyle", "La Coste", "La Grange", "La Vernia", "Leander","Ledbetter", "Leesville",
        "Lexington","Liberty Hill","Lincoln","Lockhart","Luling","Manchaca","Manor","Marble Falls","Marion","Martindale",
        "Maxwell","McDade","McQueeney","Medina","Meyersville", "Mico",  "Milano","Moulton","Muldoon", "Nada","Natalia",
        "New Braunfels","New Ulm","Nixon","Nordheim","Oakland","Paige","Pandora","Panna Maria","Pflugerville","Pipe Creek",
        "Poth","Prairie Lea", "Red Rock","Rio Medina","Rock Island","Rockdale", "Rosanky","Round Mountain","Round Rock",
        "Round Top","Runge","Saint Hedwig","San Antonio","San Marcos","Schertz", "Schulenburg",  "Schwertner", "Seguin",
        "Shiner",  "Smiley","Smithville", "Snook","Somerset","Somerville","Spicewood","Spring Branch","Staples","Stockdale",
        "Sutherland Springs","Sweet Home","Tarpley","Taylor","Thorndale","Thrall", "Universal City","Vanderpool", "Von Ormy",
        "Waelder","Washington", "Weimar","West Point",  "Westhoff","Wimberley","Wrightsboro","Yancey","Yoakum", "Yorktown"
        ],
    "West":[
        "Abilene", "Anson","Art","Avoca","Ballinger","Barksdale","Barnhart","Bend","Blackwell","Bluffton",
        "Brackettville","Brady","Bronte","Buchanan Dam","Buffalo Gap", "Burkett","Camp Wood","Carlsbad","Castell",
        "Center Point","Cherokee","Christoval","Coleman","Colorado City","Comstock","Concan","Del Rio","Doole","Doss",
        "Dyess Afb","Eden","Eldorado","Eola","Fluvanna","Fort McKavett","Fredericksburg", "Fredonia","Goldsboro",
        "Goodfellow Afb","Gouldbusk", "Hamlin", "Harper",    "Hawley","Hermleigh","Hext","Hunt","Ingram", "Ira","Junction",
        "Kempner", "Kerrville","Kingsland","Knickerbocker","Knippa","Lampasas","Langtry","Laughlin Afb",   "Lawn","Leakey",
        "Llano","Lohn","Lometa","London","Loraine","Lueders", "Maryneal","Mason","McCaulley","Melvin", "Menard","Mereta",
        "Merkel","Mertzon","Miles","Millersview","Mountain Home", "Nolan","Norton","Novice","Ovalo","Paint Rock","Pontotoc",
        "Richland Springs","Rio Frio", "Robert Lee", "Roby","Rochelle","Rocksprings", "Rockwood","Roosevelt","Roscoe",
        "Rotan","Rowena",  "Sabinal","San Angelo","San Saba","Santa Anna",  "Silver","Snyder","Sonora",  "Stamford",
        "Sterling City","Stonewall","Sweetwater","Sylvester","Talpa","Tennyson", "Tow","Trent","Tuscola","Tye","Utopia",
        "Uvalde","Valera","Valley Spring","Vancourt","Voca","Voss","Wall","Water Valley","Westbrook","Willow City","Wingate",
        "Winters"
        ]
}

# Dictionary for counties to region

counties={
    "Coast":[
        "Austin","Brazoria","Calhoun", "Chambers","Colorado","Fort Bend","Galveston","Goliad","Grimes","Hardin","Harris",
        "Jackson","Jasper","Jefferson","Liberty","Matagorda","Montgomery","Newton","Orange","Polk","San Jacinto","Tyler","Victoria",
        "Waller","Wharton"
        ],
    "East":[
        "Anderson","Angelina","Brazos","Camp","Cass","Cherokee","Falls","Franklin","Freestone","Gregg","Grimes","Harrison",
        "Henderson","Hopkins","Houston","Hunt","Jasper","Kaufman","Leon","Limestone","Madison","Marion","Miller","Montgomery",
        "Morris","Nacogdoches","Navarro","Newton","Panola","Rains","Robertson","Rusk","Sabine","San Augustine","Shelby",
        "Smith","Titus","Trinity","Upshur","Van Zandt","Walker","Waller","Washington","Wood"
        ],
    "Far West":[
        "Andrews","Borden","Brewster","Crane","Crockett","Culberson","Dawson","Ector","El Paso","Gaines","Glasscock",
        "Howard","Hudspeth","Jeff Davis","Loving","Lynn","Martin","Midland","Otero","Pecos","Presidio","Reagan","Reeves",
        "Terrell","Upton","Val Verde","Ward","Winkler"
        ],
    "North":[
        "Archer","Armstrong","Baylor","Bowie","Briscoe","Childress","Clay","Collin","Collingsworth","Cooke","Cottle",
        "Crosby","Denton","Dickens","Donley","Fannin","Floyd","Foard","Grayson","Hall","Hardeman","Haskell","Hemphill",
        "Hunt", "Jack","Kent","King","Knox","Lamar","Lubbock","Montague","Motley","Red River","Stonewall","Wheeler","Wichita",
        "Wilbarger","Wise"
        ],
    "North Central":[
        "Archer","Bell","Bosque","Brown","Burnet","Callahan","Coleman","Collin","Comanche","Cooke","Coryell",
        "Dallas","Delta","Denton","Eastland","Ellis","Erath","Falls",  "Fannin","Freestone",  "Grayson","Hamilton","Henderson",
        "Hill","Hood","Hopkins","Hunt","Jack","Johnson","Kaufman","Lampasas","Limestone","McLennan","Milam","Mills","Navarro",
        "Palo Pinto","Parker","Rains", "Robertson","Rockwall","Shackelford","Somervell","Stephens","Tarrant","Throckmorton",
        "Van Zandt","Williamson","Wise","Young"
        ],
    "South":[
        "Aransas", "Atascosa",  "Bee","Bexar","Brooks","Calhoun","Cameron", "Dimmit","Duval", "Frio","Goliad","Hidalgo","Jim Hogg","Jim Wells",
        "Kenedy",  "Kleberg","La Salle","Live Oak","Maverick","McMullen","Medina","Nueces", "Refugio","San Patricio",  "Starr","Webb","Willacy",
        "Wilson","Zapata","Zavala"
        ],
    "South Central":[
        "Atascosa","Austin","Bandera","Bastrop","Bee","Bell", "Bexar","Blanco","Burleson","Burnet","Caldwell","Colorado",
        "Comal","DeWitt","Falls", "Fayette", "Frio","Goliad","Gonzales","Guadalupe","Hays","Karnes","Kendall","Kerr","Lavaca", "Lee",
        "Live Oak", "Llano","Medina","Milam","Real","Travis", "Victoria","Washington","Williamson","Wilson"
        ],
    "West":[
        "Bandera","Bell","Blanco", "Borden","Burnet","Callahan","Coke","Coleman","Concho","Coryell", "Edwards", "Fisher","Gillespie",
        "Haskell","Irion","Jones","Kendall", "Kent","Kerr","Kimble","Kinney","Lampasas","Llano","Mason","McCulloch","Medina","Menard",
        "Mills","Mitchell","Nolan","Real","Runnels","San Saba","Schleicher", "Scurry","Shackelford","Sterling","Stonewall","Sutton",
        "Taylor","Throckmorton","Tom Green","Uvalde","Val Verde"
        ]
}

# List of counties

counties_list=[
    "Austin","Brazoria","Calhoun", "Chambers","Colorado","Fort Bend","Galveston","Goliad","Grimes","Hardin","Harris",
    "Jackson","Jasper","Jefferson","Liberty","Matagorda","Montgomery","Newton","Orange","Polk","San Jacinto","Tyler","Victoria",
    "Waller","Wharton","Anderson","Angelina","Brazos","Camp","Cass","Cherokee","Falls","Franklin","Freestone","Gregg","Grimes","Harrison",
    "Henderson","Hopkins","Houston","Hunt","Jasper","Kaufman","Leon","Limestone","Madison","Marion","Montgomery",
    "Morris","Nacogdoches","Navarro","Newton","Panola","Rains","Robertson","Rusk","Sabine","San Augustine","Shelby",
    "Smith","Titus","Trinity","Upshur","Van Zandt","Walker","Waller","Washington","Wood","Andrews","Borden","Brewster","Crane","Crockett",
    "Culberson","Dawson","Ector","El Paso","Gaines","Glasscock","Howard","Hudspeth","Jeff Davis","Loving","Lynn","Martin","Midland",
    "Pecos","Presidio","Reagan","Reeves","Terrell","Upton","Val Verde","Ward","Winkler",
    "Archer","Armstrong","Baylor","Bowie","Briscoe","Childress","Clay","Collin","Collingsworth","Cooke","Cottle",
    "Crosby","Denton","Dickens","Donley","Fannin","Floyd","Foard","Grayson","Hall","Hardeman","Haskell","Hemphill",
    "Hunt", "Jack","Kent","King","Knox","Lamar","Lubbock","Montague","Motley","Red River","Stonewall","Wheeler","Wichita",
    "Wilbarger","Wise","Archer","Bell","Bosque","Brown","Burnet","Callahan","Coleman","Collin","Comanche","Cooke","Coryell",
    "Dallas","Delta","Denton","Eastland","Ellis","Erath","Falls",  "Fannin","Freestone",  "Grayson","Hamilton","Henderson",
    "Hill","Hood","Hopkins","Hunt","Jack","Johnson","Kaufman","Lampasas","Limestone","McLennan","Milam","Mills","Navarro",
    "Palo Pinto","Parker","Rains", "Robertson","Rockwall","Shackelford","Somervell","Stephens","Tarrant","Throckmorton",
    "Van Zandt","Williamson","Wise","Young","Aransas", "Atascosa",  "Bee","Bexar","Brooks","Calhoun","Cameron", "Dimmit","Duval",
    "Frio","Goliad","Hidalgo","Jim Hogg","Jim Wells","Kenedy",  "Kleberg","La Salle","Live Oak","Maverick","McMullen","Medina",
    "Nueces", "Refugio","San Patricio",  "Starr","Webb","Willacy","Wilson","Zapata","Zavala",
    "Atascosa","Austin","Bandera","Bastrop","Bee","Bell", "Bexar","Blanco","Burleson","Burnet","Caldwell","Colorado",
    "Comal","DeWitt","Falls", "Fayette", "Frio","Goliad","Gonzales","Guadalupe","Hays","Karnes","Kendall","Kerr","Lavaca", "Lee",
    "Live Oak", "Llano","Medina","Milam","Real","Travis", "Victoria","Washington","Williamson","Wilson",
    "Bandera","Bell","Blanco", "Borden","Burnet","Callahan","Coke","Coleman","Concho","Coryell", "Edwards", "Fisher","Gillespie",
    "Haskell","Irion","Jones","Kendall", "Kent","Kerr","Kimble","Kinney","Lampasas","Llano","Mason","McCulloch","Medina","Menard",
    "Mills","Mitchell","Nolan","Real","Runnels","San Saba","Schleicher", "Scurry","Shackelford","Sterling","Stonewall","Sutton",
    "Taylor","Throckmorton","Tom Green","Uvalde","Val Verde"
    ]

""" Transform COVID data setes so that county names are not variables but are values """

covid_c_melt=pd.melt(
                  covid_conf,
                  id_vars='Date',
                  value_vars=counties_list,
                  var_name='counties'
                  )

covid_d_melt=pd.melt(
                  covid_death,
                  id_vars='Date',
                  value_vars=counties_list,
                  var_name='counties'
                  )

""" Create conditional lists to search for county or city values that are in the specified regions """

condlistCounties=[
          np.isin(covid_c_melt["counties"],counties["Coast"]),
          np.isin(covid_c_melt["counties"],counties["East"]),
          np.isin(covid_c_melt["counties"],counties["Far West"]),
          np.isin(covid_c_melt["counties"],counties["North"]),
          np.isin(covid_c_melt["counties"],counties["North Central"]),
          np.isin(covid_c_melt["counties"],counties["South"]),
          np.isin(covid_c_melt["counties"],counties["South Central"]),
          np.isin(covid_c_melt["counties"],counties["West"])
           ]

condlistCounties2=[
          np.isin(covid_d_melt["counties"],counties["Coast"]),
          np.isin(covid_d_melt["counties"],counties["East"]),
          np.isin(covid_d_melt["counties"],counties["Far West"]),
          np.isin(covid_d_melt["counties"],counties["North"]),
          np.isin(covid_d_melt["counties"],counties["North Central"]),
          np.isin(covid_d_melt["counties"],counties["South"]),
          np.isin(covid_d_melt["counties"],counties["South Central"]),
          np.isin(covid_d_melt["counties"],counties["West"])
           ]

condlistCounties3=[
          np.isin(gdp["County"],counties["Coast"]),
          np.isin(gdp["County"],counties["East"]),
          np.isin(gdp["County"],counties["Far West"]),
          np.isin(gdp["County"],counties["North"]),
          np.isin(gdp["County"],counties["North Central"]),
          np.isin(gdp["County"],counties["South"]),
          np.isin(gdp["County"],counties["South Central"]),
          np.isin(gdp["County"],counties["West"])
           ]

condlistCities=[
          np.isin(weather_history["city"],cities["Coast"]),
          np.isin(weather_history["city"],cities["East"]),
          np.isin(weather_history["city"],cities["Far West"]),
          np.isin(weather_history["city"],cities["North"]),
          np.isin(weather_history["city"],cities["North Central"]),
          np.isin(weather_history["city"],cities["South"]),
          np.isin(weather_history["city"],cities["South Central"]),
          np.isin(weather_history["city"],cities["West"])
           ]

condlistCities2=[
          np.isin(pop_density["name"],cities["Coast"]),
          np.isin(pop_density["name"],cities["East"]),
          np.isin(pop_density["name"],cities["Far West"]),
          np.isin(pop_density["name"],cities["North"]),
          np.isin(pop_density["name"],cities["North Central"]),
          np.isin(pop_density["name"],cities["South"]),
          np.isin(pop_density["name"],cities["South Central"]),
          np.isin(pop_density["name"],cities["West"])
           ]

choicelist=["Coast", "East","Far West", "North", "North Central","South", "South Central", "West"]


""" GDP data set: Map counties to region, convert gdp to numeric, and then average by region """


gdp["region"]=np.select(condlistCounties3,choicelist)
gdp['gdp']=gdp['GDP'].str.replace(',','',regex=False).astype(float)
gdp_grouped = gdp.groupby(['region'],as_index=False)[['gdp']].mean()


""" Population Density data set: Map cities to region and then average  density by region """


pop_density["region"]=np.select(condlistCities2,choicelist)
pop_density_grouped = pop_density.groupby(['region'],as_index=False)[['density']].mean()


"""
    Covid Confirmed data set: Map counties to region, sum cases confirmed across region and date, and
    then create a variable that finds the difference in cases from previous date
    """


covid_c_melt["region"]=np.select(condlistCounties,choicelist)
covid_c_melt.rename(columns={'value':'Covid_Confirmed'},inplace=True)
covid_c_grouped = covid_c_melt.groupby(['Date','region'],as_index=False)[['Covid_Confirmed']].sum()
covid_c_grouped['Covid_Confirmed_Change'] = covid_c_grouped.groupby(['region'])['Covid_Confirmed'].diff()


"""
    Covid Death data set: Map counties to region, sum cases deaths across region and date, and
    then create a variable that finds the difference in cases deaths from previous date
    """


covid_d_melt["region"]=np.select(condlistCounties2,choicelist)
covid_d_melt.rename(columns={'value':'Covid_Death'},inplace=True)
covid_d_grouped = covid_d_melt.groupby(['Date','region'],as_index=False)[['Covid_Death']].sum()
covid_d_grouped['Covid_Death_Change'] = covid_d_grouped.groupby(['region'])['Covid_Death'].diff()

# Merge the 2 covid data sets together

covid_merge=pd.merge(
    covid_c_grouped,
    covid_d_grouped,
    how="inner",
    on=['Date','region'],
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None,
)


""" Weather history data set:  Map cities to region, add time to date, average out all weather variables by date and time"""


weather_history["region"]=np.select(condlistCities,choicelist)
weather_history['Time']=weather_history['time']//100
weather_history['date']=pd.to_datetime(weather_history['date'],utc=True)
weather_history['date'] +=  pd.to_timedelta(weather_history.Time, unit='h')
weather_hist_grouped = weather_history.groupby(['date','region'],as_index=False)[[
                                                      'tempC','tempF','windspeedMiles','windspeedKmph','winddirDegree','winddir16Point','weatherCode','weatherDesc',
                                                      'precipMM','precipInches','humidity','visibility','visibilityMiles','pressure','pressureInches','cloudcover',
                                                      'HeatIndexC','HeatIndexF','DewPointC','DewPointF','WindChillC','WindChillF','WindGustMiles','WindGustKmph',
                                                      'FeelsLikeC','FeelsLikeF','uvIndex']].mean()
    



"""
    Ercot data set: Change structure by collapsing region variables to one column, convert date to UTC then back to local,
    and only keep rows if its after July 2008 because that is when we have weather data
    """


ercot_melt=pd.melt(ercot,
                  id_vars='Hour_Ending',
                  value_vars=['Coast','East','Far West','North','North Central','South','South Central','West'],
                  var_name='region')
ercot_melt.rename(columns={"value":"ercot"},inplace=True)
ercot_melt["Date_string"]=ercot_melt['Hour_Ending'].str.slice(start=0,stop=19)
ercot_melt["Date"]=pd.to_datetime(ercot_melt['Hour_Ending'].str.slice(start=0,stop=10))
ercot_melt['date']=pd.to_datetime(ercot_melt['Hour_Ending'],utc=True)-pd.to_timedelta(6,unit='h')
mask = (ercot_melt['date'] >= '2008-07-1') 
ercot_filtered=ercot_melt.loc[mask]




# Merge weather data and ercot data

ercot_weather_hist=pd.merge(
    ercot_filtered,
    weather_hist_grouped,
    how="left",
    on=['date','region'],
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None,
)

# Merge previous data set with covid merged data 

ercot_weather_covid=pd.merge(
    ercot_weather_hist,
    covid_merge,
    how="left",
    on=['Date','region'],
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None,
)

# Merged previous data with gdp data 

ercot_wth_covid_gdp=pd.merge(
    ercot_weather_covid,
    gdp_grouped,
    how="left",
    on=['region'],
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None,
)

# Merged previous data with population density data 

ercot_wth_covid_gdp_pop=pd.merge(
    ercot_wth_covid_gdp,
    pop_density_grouped,
    how="left",
    on=['region'],
    left_on=None,
    right_on=None,
    left_index=False,
    right_index=False,
    sort=True,
    suffixes=("_x", "_y"),
    copy=True,
    indicator=False,
    validate=None,
)

# Output data to text file because too many rows for csv

ercot_wth_covid_gdp_pop.to_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\ercot_weather_covid_gdp_pop.txt', header=True, index=None, sep=',', mode='w')

# Average missing ercot data. 

ercot_wth_covid_gdp_pop['prev1']=ercot_wth_covid_gdp_pop['ercot'].shift(1)
ercot_wth_covid_gdp_pop['fut1']=ercot_wth_covid_gdp_pop['ercot'].shift(-1)


ercot_wth_covid_gdp_pop['ercotNew']=np.where(ercot_wth_covid_gdp_pop['ercot'].notnull(),ercot_wth_covid_gdp_pop['ercot'],
                                          ercot_wth_covid_gdp_pop[['prev1','fut1']].mean(axis=1))
ercot_wth_covid_gdp_pop.drop(columns=['prev1','fut1'],inplace=True)

# Average missing weather data. First missing value has more weight from previous value. Second missing value puts more weight on the next value

for column in ercot_wth_covid_gdp_pop[['tempC','tempF','windspeedMiles','windspeedKmph','winddirDegree','weatherCode','precipMM','precipInches','humidity','visibility',
                                       'visibilityMiles','pressure','pressureInches','cloudcover','HeatIndexC','HeatIndexF','DewPointC','DewPointF','WindChillC',
                                       'WindChillF','WindGustMiles','WindGustKmph','FeelsLikeC','FeelsLikeF','uvIndex']]:
    ercot_wth_covid_gdp_pop['prev2']=ercot_wth_covid_gdp_pop[column].shift(2)
    ercot_wth_covid_gdp_pop['prev1']=ercot_wth_covid_gdp_pop[column].shift(1)
    ercot_wth_covid_gdp_pop['fut1']=ercot_wth_covid_gdp_pop[column].shift(-1)
    ercot_wth_covid_gdp_pop['fut2']=ercot_wth_covid_gdp_pop[column].shift(-2)

    
    ercot_wth_covid_gdp_pop[column+'Int']=np.where(ercot_wth_covid_gdp_pop[column].notnull(),ercot_wth_covid_gdp_pop[column],
                                             np.where(ercot_wth_covid_gdp_pop['prev1'].notnull(),ercot_wth_covid_gdp_pop[['prev1','fut2','prev1']].mean(axis=1),
                                                      ercot_wth_covid_gdp_pop[['prev2','fut1','fut1']].mean(axis=1)))

    ercot_wth_covid_gdp_pop[column + '24']=ercot_wth_covid_gdp_pop[column+'Int'].shift(24)
    ercot_wth_covid_gdp_pop[column+'New']=np.where(ercot_wth_covid_gdp_pop['Date']=='4/30/2021',ercot_wth_covid_gdp_pop[column + '24'],ercot_wth_covid_gdp_pop[column+'Int'])
 
    ercot_wth_covid_gdp_pop.drop(columns=['prev2','prev1','fut1','fut2',column,column+'24',column+'Int' ],inplace=True)

#Megha's code

df = ercot_wth_covid_gdp_pop[["region","ercotNew","Date","Date_string",'date',"Covid_Confirmed","Covid_Confirmed_Change","Covid_Death","Covid_Death_Change","gdp",
                                  "density","tempCNew","windspeedMilesNew","winddirDegreeNew","weatherCodeNew","precipMMNew","humidityNew","visibilityNew","pressureNew",
                                  "cloudcoverNew","HeatIndexCNew","DewPointCNew","WindChillCNew","WindGustMilesNew","FeelsLikeCNew","uvIndexNew"]]

cols=["Covid_Confirmed","Covid_Confirmed_Change","Covid_Death","Covid_Death_Change"]
for i in cols:
  df[i]=df[i].fillna(0)


df.to_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\Dataframe Original.csv')


print(df.isnull().sum())


print(df.describe())


cols=["ercotNew","Covid_Confirmed","Covid_Confirmed_Change","Covid_Death","Covid_Death_Change","gdp","density","tempCNew","windspeedMilesNew","winddirDegreeNew",
      "weatherCodeNew","precipMMNew","humidityNew","visibilityNew","pressureNew","cloudcoverNew","HeatIndexCNew","DewPointCNew","WindChillCNew","WindGustMilesNew",
      "FeelsLikeCNew","uvIndexNew"]

def replace(group):
    
    mean, std = group.mean(), group.std()
    outliers = (group - mean).abs() > 2*std

    group[outliers] = mean
    return group

df.groupby('region').transform(replace)



print(df.describe())
print(df.head())

# Output data to csv and text. Text will have all the rows.


df.to_csv(r'C:\Users\afedgo\Desktop\Practice\Datathon 2021\Dataframe Outliers.csv') 


