import json

PROMODS_COMPANIES = ['ikea', 'bauhaus', 'alds', 'europcar', 'lidl', 'xxxl', 'man_fac', 'albertheijn', 'mcdonalds', 'tartak', 'rewe', 'man_dlr', 'jumbo', 'auhof', 'omv4', 'omv2', 'metro', 'billa', 'omv1', 'obi', 'bp_retail', 'hofer', 'omv3', 'tesco', 'daf_dlr', 'dhl', 'ikea_pl', 'auchan', 'nd', 'shell', 'zlecenie', 'biedronka', 'budowa', 'stacja', 'saab', 'dagli', 'elgiganten', 'szatmari', 'castorama', 'lidl_centrum', 'budimex', 'm1', 'zbyszko',
'netto', 'komfort', 'leclerc', 'statoil', 'naftoport', 'wurth', 'roboty', 'betard', 'kopal_zw', 'raben', 'cemex', 'citronex', 'rafineria_gd', 'expert', 'jadranska', 'albertheijn', 'icelandair', 'mercadona', 'lkw_walter', 'billa', 'mazet', 'transwood', 'leroymerlin', 'konzum', 'ina', 'samkaup', 'olis', 'port_bolin', 'lacquide', 'bondi', 'samskip', 'hb_grandi', 'eimskip', 'vegagerdin', 'smyril', 'dia', 'lukoil', 'heineken', 'effo', 'prisma', 'jadranska1', 'jadranska2', 'sildarvinn', 'psa_ant', 'gnt_auto', 'willys', 'fandwhr', 'lafarge_t', 'aquael', 'salag', 'mediamarkt', 'mediaexpert', 'boliden', 'iav', 'kronan', 'ice_gla', 'fuel_depot', 'bonus', 'hekla', 'isavia', 'timbursala', 'port_sudur', 'port_isa', 'orkan', 'port_sudavik', 'konzum', 'kuenenagelll', 'n1', 'seljaland', 'hawesmarket', 'creamery', 'jadranska', 'jewson', 'eroski', 'captiglo', 'polarisline1', 'seedvault', 'port_blond', 'sah_afurdir', 'samkaup', 'landsvirkjun', 'vsv', 'vest_port', 'pfi', 'gardshorn', 'vegagerdin_r', 'svalsat', 'epicentrk', 'flex', 'renault', 'likmerge', 'roadworks_a7', 'ljug_handel', 'audi', 'waberers', 'biedronka_in', 'gospodarstwo', 'minimarket3', 'minimarket2', 'mostostal', 'transwood', 'opener', 'delphia', 'bct_gdynia', 'podlogi_elk', 'plastimet', 'rybackie_elk', 'ziko', 'serwis', 'philips', 'minimarket1', 'ot_port', 'sawmillforst', 'dino', 'aero_elblag', 'market', 'minimarket5', 'roboty', 'ciepli_zamb', 'atlanta_zamb', 'agromat', 'agrolen', 'agromasz']

def get_country(city_name):
    with open('static/assets/files/companies.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        for city in data:
            if city.get("city_name") == city_name:
                return city.get("country")
                break
    return None