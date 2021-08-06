import requests
from nsetools import Nse
import yfinance as yf
from CandleStick import brain_candle
from Volume import volume_indicator
from Indicator import technical_indicator
from SupportResistance import sr_indicator
import pandas as pd
from prettytable import PrettyTable
import math
import datetime
import pytz
from Performance import handler
from humanfriendly import format_timespan

FinalStockList = {'21STCENMGM': '21st Century Management Services Limited', '3MINDIA': '3M India Limited', 'AARTIDRUGS': 'Aarti Drugs Limited', 'AARTIIND': 'Aarti Industries Limited', 'AAVAS': 'Aavas Financiers Limited', 'ABB': 'ABB India Limited', 'ABBOTINDIA': 'Abbott India Limited', 'ABFRL': 'Aditya Birla Fashion and Retail Limited', 'ACC': 'ACC Limited', 'ACCELYA': 'Accelya Solutions India Limited', 'ACCURACY': 'Accuracy Shipping Limited', 'ACE': 'Action Construction Equipment Limited', 'ADANIENT': 'Adani Enterprises Limited', 'ADANIGREEN': 'Adani Green Energy Limited', 'ADANIPORTS': 'Adani Ports and Special Economic Zone Limited', 'ADANIPOWER': 'Adani Power Limited', 'ADANITRANS': 'Adani Transmission Limited', 'ADVENZYMES': 'Advanced Enzyme Technologies Limited', 'AEGISCHEM': 'Aegis Logistics Limited', 'AJANTPHARM': 'Ajanta Pharma Limited', 'AKSHARCHEM': 'AksharChem India Limited', 'ALEMBICLTD': 'Alembic Limited', 'ALKEM': 'Alkem Laboratories Limited', 'ALKYLAMINE': 'Alkyl Amines Chemicals Limited', 'ALLCARGO': 'Allcargo Logistics Limited', 'ALMONDZ': 'Almondz Global Securities Limited', 'ALOKINDS': 'Alok Industries Limited', 'ALPHAGEO': 'Alphageo (India) Limited', 'AMARAJABAT': 'Amara Raja Batteries Limited', 'AMBER': 'Amber Enterprises India Limited', 'AMBIKCO': 'Ambika Cotton Mills Limited', 'AMBUJACEM': 'Ambuja Cements Limited', 'ANANTRAJ': 'Anant Raj Limited', 'ANDHRACEMT': 'Andhra Cements Limited', 'ANDHRSUGAR': 'The Andhra Sugars Limited', 'ANGELBRKG': 'Angel Broking Limited', 'ANURAS': 'Anupam Rasayan India Limited', 'APARINDS': 'Apar Industries Limited', 'APCOTEXIND': 'Apcotex Industries Limited', 'APLAPOLLO': 'APL Apollo Tubes Limited', 'APLLTD': 'Alembic Pharmaceuticals Limited', 'APOLLO': 'Apollo Micro Systems Limited', 'APOLLOHOSP': 'Apollo Hospitals Enterprise Limited', 'APOLLOPIPE': 'Apollo Pipes Limited', 'APOLLOTYRE': 'Apollo Tyres Limited', 'APTECHT': 'Aptech Limited', 'ARVIND': 'Arvind Limited', 'ARVINDFASN': 'Arvind Fashions Limited', 'ARVSMART': 'Arvind SmartSpaces Limited', 'ASAHIINDIA': 'Asahi India Glass Limited', 'ASAHISONG': 'Asahi Songwon Colors Limited', 'ASHOKA': 'Ashoka Buildcon Limited', 'ASHOKLEY': 'Ashok Leyland Limited', 'ASIANPAINT': 'Asian Paints Limited', 'ASIANTILES': 'Asian Granito India Limited', 'ASTERDM': 'Aster DM Healthcare Limited', 'ASTRAMICRO': 'Astra Microwave Products Limited', 'ASTRON': 'Astron Paper & Board Mill Limited', 'ATFL': 'Agro Tech Foods Limited', 'ATGL': 'Adani Total Gas Limited', 'ATUL': 'Atul Limited', 'ATULAUTO': 'Atul Auto Limited', 'AUBANK': 'AU Small Finance Bank Limited', 'AUROPHARMA': 'Aurobindo Pharma Limited', 'AVADHSUGAR': 'Avadh Sugar & Energy Limited', 'AVANTIFEED': 'Avanti Feeds Limited', 'AWHCL': 'Antony Waste Handling Cell Limited', 'AXISBANK': 'Axis Bank Limited', 'BAJAJ-AUTO': 'Bajaj Auto Limited', 'BAJAJCON': 'Bajaj Consumer Care Limited', 'BAJAJELEC': 'Bajaj Electricals Limited', 'BAJAJFINSV': 'Bajaj Finserv Limited', 'BAJAJHIND': 'Bajaj Hindusthan Sugar Limited', 'BAJAJHLDNG': 'Bajaj Holdings & Investment Limited', 'BAJFINANCE': 'Bajaj Finance Limited', 'BALAMINES': 'Balaji Amines Limited', 'BALKRISIND': 'Balkrishna Industries Limited', 'BALRAMCHIN': 'Balrampur Chini Mills Limited', 'BANCOINDIA': 'Banco Products (I) Limited', 'BANDHANBNK': 'Bandhan Bank Limited', 'BANKBARODA': 'Bank of Baroda', 'BANKINDIA': 'Bank of India', 'BARBEQUE': 'Barbeque Nation Hospitality Limited', 'BASF': 'BASF India Limited', 'BATAINDIA': 'Bata India Limited', 'BAYERCROP': 'Bayer Cropscience Limited', 'BBL': 'Bharat Bijlee Limited', 'BBTC': 'Bombay Burmah Trading Corporation Limited', 'BCG': 'Brightcom Group Limited', 'BDL': 'Bharat Dynamics Limited', 'BECTORFOOD': 'Mrs. Bectors Food Specialities Limited', 'BEL': 'Bharat Electronics Limited', 'BEML': 'BEML Limited', 'BEPL': 'Bhansali Engineering Polymers Limited', 'BERGEPAINT': 'Berger Paints (I) Limited', 'BFUTILITIE': 'BF Utilities Limited', 'BHARATFORG': 'Bharat Forge Limited', 'BHARTIARTL': 'Bharti Airtel Limited', 'BIOCON': 'Biocon Limited', 'BIRLACORPN': 'Birla Corporation Limited', 'BLISSGVS': 'Bliss GVS Pharma Limited', 'BLS': 'BLS International Services Limited', 'BLUEDART': 'Blue Dart Express Limited', 'BLUESTARCO': 'Blue Star Limited', 'BODALCHEM': 'Bodal Chemicals Limited', 'BOMDYEING': 'Bombay Dyeing & Mfg Company Limited', 'BOROLTD': 'Borosil Limited', 'BORORENEW': 'BOROSIL RENEWABLES LIMITED', 'BOSCHLTD': 'Bosch Limited', 'BRIGADE': 'Brigade Enterprises Limited', 'BRITANNIA': 'Britannia Industries Limited', 'BSE': 'BSE Limited', 'BSOFT': 'BIRLASOFT LIMITED', 'BURGERKING': 'Burger King India Limited', 'BUTTERFLY': 'Butterfly Gandhimathi Appliances Limited', 'CADILAHC': 'Cadila Healthcare Limited', 'CAMLINFINE': 'Camlin Fine Sciences Limited', 'CANBK': 'Canara Bank', 'CANFINHOME': 'Can Fin Homes Limited', 'CARBORUNIV': 'Carborundum Universal Limited', 'CARERATING': 'CARE Ratings Limited', 'CASTROLIND': 'Castrol India Limited', 'CCL': 'CCL Products (India) Limited', 'CEATLTD': 'CEAT Limited', 'CENTENKA': 'Century Enka Limited', 'CENTEXT': 'Century Extrusions Limited', 'CENTRALBK': 'Central Bank of India', 'CENTRUM': 'Centrum Capital Limited', 'CENTURYPLY': 'Century Plyboards (India) Limited', 'CENTURYTEX': 'Century Textiles & Industries Limited', 'CERA': 'Cera Sanitaryware Limited', 'CESC': 'CESC Limited', 'CGCL': 'Capri Global Capital Limited', 'CGPOWER': 'CG Power and Industrial Solutions Limited', 'CHAMBLFERT': 'Chambal Fertilizers & Chemicals Limited', 'CHEMBOND': 'Chembond Chemicals Ltd', 'CHEMCON': 'Chemcon Speciality Chemicals Limited', 'CHENNPETRO': 'Chennai Petroleum Corporation Limited', 'CIGNITITEC': 'Cigniti Technologies Limited', 'CINELINE': 'Cineline India Limited', 'CIPLA': 'Cipla Limited', 'CLEAN': 'Clean Science and Technology Limited', 'COALINDIA': 'Coal India Limited', 'COCHINSHIP': 'Cochin Shipyard Limited', 'COFFEEDAY': 'Coffee Day Enterprises Limited', 'COLPAL': 'Colgate Palmolive (India) Limited', 'COMPINFO': 'Compuage Infocom Limited', 'CONCOR': 'Container Corporation of India Limited', 'CONFIPET': 'Confidence Petroleum India Limited', 'COROMANDEL': 'Coromandel International Limited', 'COSMOFILMS': 'Cosmo Films Limited', 'CRAFTSMAN': 'Craftsman Automation Limited', 'CREDITACC': 'CREDITACCESS GRAMEEN LIMITED', 'CRISIL': 'CRISIL Limited', 'CSBBANK': 'CSB Bank Limited', 'CUB': 'City Union Bank Limited', 'CUMMINSIND': 'Cummins India Limited', 'CYIENT': 'Cyient Limited', 'DAAWAT': 'LT Foods Limited', 'DABUR': 'Dabur India Limited', 'DALBHARAT': 'Dalmia Bharat Limited', 'DALMIASUG': 'Dalmia Bharat Sugar and Industries Limited', 'DBL': 'Dilip Buildcon Limited', 'DCAL': 'Dishman Carbogen Amcis Limited', 'DCBBANK': 'DCB Bank Limited', 'DCMSHRIRAM': 'DCM Shriram Limited', 'DCW': 'DCW Limited', 'DECCANCE': 'Deccan Cements Limited', 'DEEPAKFERT': 'Deepak Fertilizers And Petrochemicals Corporation Limited', 'DEEPAKNTR': 'Deepak Nitrite Limited', 'DEEPINDS': 'Deep Industries Limited', 'DELTACORP': 'Delta Corp Limited', 'DEN': 'Den Networks Limited', 'DFMFOODS': 'DFM Foods Limited', 'DHAMPURSUG': 'Dhampur Sugar Mills Limited', 'DHANI': 'Dhani Services Limited', 'DHANUKA': 'Dhanuka Agritech Limited', 'DICIND': 'DIC India Limited', 'DIGISPICE': 'DiGiSPICE Technologies Limited', 'DIXON': 'Dixon Technologies (India) Limited', 'DLF': 'DLF Limited', 'DMART': 'Avenue Supermarts Limited', 'DOLLAR': 'Dollar Industries Limited', 'DVL': 'Dhunseri Ventures Limited', 'DWARKESH': 'Dwarikesh Sugar Industries Limited', 'DYNPRO': 'Dynemic Products Limited', 'EASEMYTRIP': 'Easy Trip Planners Limited', 'ECLERX': 'eClerx Services Limited', 'EDELWEISS': 'Edelweiss Financial Services Limited', 'EICHERMOT': 'Eicher Motors Limited', 'EIDPARRY': 'EID Parry India Limited', 'EIHAHOTELS': 'EIH Associated Hotels Limited', 'EIHOTEL': 'EIH Limited', 'ELECON': 'Elecon Engineering Company Limited', 'ELECTCAST': 'Electrosteel Castings Limited', 'ELGIEQUIP': 'Elgi Equipments Limited', 'EMAMILTD': 'Emami Limited', 'EMAMIPAP': 'Emami Paper Mills Limited', 'EMAMIREAL': 'Emami Realty Limited', 'ENDURANCE': 'Endurance Technologies Limited', 'EQUITAS': 'Equitas Holdings Limited', 'ERIS': 'Eris Lifesciences Limited', 'ESCORTS': 'Escorts Limited', 'EVEREADY': 'Eveready Industries India Limited', 'EVERESTIND': 'Everest Industries Limited', 'EXCEL': 'Excel Realty N Infra Limited', 'EXCELINDUS': 'Excel Industries Limited', 'EXIDEIND': 'Exide Industries Limited', 'FCL': 'Fineotex Chemical Limited', 'FEDERALBNK': 'The Federal Bank  Limited', 'FILATEX': 'Filatex India Limited', 'FINCABLES': 'Finolex Cables Limited', 'FINPIPE': 'Finolex Industries Limited', 'FLUOROCHEM': 'Gujarat Fluorochemicals Limited', 'FMGOETZE': 'Federal-Mogul Goetze (India) Limited.', 'FORCEMOT': 'FORCE MOTORS LTD', 'FORTIS': 'Fortis Healthcare Limited', 'FRETAIL': 'Future Retail Limited', 'FSL': 'Firstsource Solutions Limited', 'GABRIEL': 'Gabriel India Limited', 'GAIL': 'GAIL (India) Limited', 'GANECOS': 'Ganesha Ecosphere Limited', 'GANGESSECU': 'Ganges Securities Limited', 'GATI': 'GATI Limited', 'GAYAPROJ': 'Gayatri Projects Limited', 'GENUSPOWER': 'Genus Power Infrastructures Limited', 'GEOJITFSL': 'Geojit Financial Services Limited', 'GEPIL': 'GE Power India Limited', 'GET&D': 'GE T&D India Limited', 'GICHSGFIN': 'GIC Housing Finance Limited', 'GICRE': 'General Insurance Corporation of India', 'GILLANDERS': 'Gillanders Arbuthnot & Company Limited', 'GILLETTE': 'Gillette India Limited', 'GLAND': 'Gland Pharma Limited', 'GLAXO': 'GlaxoSmithKline Pharmaceuticals Limited', 'GLENMARK': 'Glenmark Pharmaceuticals Limited', 'GLOBUSSPR': 'Globus Spirits Limited', 'GMMPFAUDLR': 'GMM Pfaudler Limited', 'GMRINFRA': 'GMR Infrastructure Limited', 'GNA': 'GNA Axles Limited', 'GODFRYPHLP': 'Godfrey Phillips India Limited', 'GODREJAGRO': 'Godrej Agrovet Limited', 'GODREJCP': 'Godrej Consumer Products Limited', 'GODREJIND': 'Godrej Industries Limited', 'GODREJPROP': 'Godrej Properties Limited', 'GOKULAGRO': 'Gokul Agro Resources Limited', 'GOLDENTOBC': 'Golden Tobacco Limited', 'GPIL': 'Godawari Power And Ispat limited', 'GPPL': 'Gujarat Pipavav Port Limited', 'GRANULES': 'Granules India Limited', 'GRAPHITE': 'Graphite India Limited', 'GRASIM': 'Grasim Industries Limited', 'GRAVITA': 'Gravita India Limited', 'GREAVESCOT': 'Greaves Cotton Limited', 'GREENPLY': 'Greenply Industries Limited', 'GRINFRA': 'G R Infraprojects Limited', 'GRSE': 'Garden Reach Shipbuilders & Engineers Limited', 'GUFICBIO': 'Gufic Biosciences Limited', 'GUJGASLTD': 'Gujarat Gas Limited', 'HAL': 'Hindustan Aeronautics Limited', 'HAPPSTMNDS': 'Happiest Minds Technologies Limited', 'HATHWAY': 'Hathway Cable & Datacom Limited', 'HAVELLS': 'Havells India Limited', 'HCG': 'Healthcare Global Enterprises Limited', 'HCL-INSYS': 'HCL Infosystems Limited', 'HCLTECH': 'HCL Technologies Limited', 'HDFCAMC': 'HDFC Asset Management Company Limited', 'HDFCBANK': 'HDFC Bank Limited', 'HDFCLIFE': 'HDFC Life Insurance Company Limited', 'HEG': 'HEG Limited', 'HERANBA': 'Heranba Industries Limited', 'HERITGFOOD': 'Heritage Foods Limited', 'HEROMOTOCO': 'Hero MotoCorp Limited', 'HFCL': 'HFCL Limited', 'HIKAL': 'Hikal Limited', 'HIL': 'HIL Limited', 'HILTON': 'Hilton Metal Forging Limited', 'HINDALCO': 'Hindalco Industries Limited', 'HIRECT': 'Hind Rectifiers Limited', 'HITECH': 'Hi-Tech Pipes Limited', 'HOMEFIRST': 'Home First Finance Company India Limited', 'HONAUT': 'Honeywell Automation India Limited', 'HSCL': 'Himadri Speciality Chemical Limited', 'IBREALEST': 'Indiabulls Real Estate Limited', 'ICICIBANK': 'ICICI Bank Limited', 'ICICIGI': 'ICICI Lombard General Insurance Company Limited', 'ICICIPRULI': 'ICICI Prudential Life Insurance Company Limited', 'ICIL': 'Indo Count Industries Limited', 'IDBI': 'IDBI Bank Limited', 'IDEA': 'Vodafone Idea Limited', 'IDFC': 'IDFC Limited', 'IDFCFIRSTB': 'IDFC First Bank Limited', 'IFCI': 'IFCI Limited', 'IGARASHI': 'Igarashi Motors India Limited', 'IGL': 'Indraprastha Gas Limited', 'IGPL': 'IG Petrochemicals Limited', 'IIFL': 'IIFL Finance Limited', 'IIFLSEC': 'IIFL Securities Limited', 'IMFA': 'Indian Metals & Ferro Alloys Limited', 'IMPAL': 'India Motor Parts and Accessories Limited', 'INDHOTEL': 'The Indian Hotels Company Limited', 'INDIACEM': 'The India Cements Limited', 'INDIAGLYCO': 'India Glycols Limited', 'INDIAMART': 'Indiamart Intermesh Limited', 'INDIANB': 'Indian Bank', 'INDIANHUME': 'Indian Hume Pipe Company Limited', 'INDIGO': 'InterGlobe Aviation Limited', 'INDNIPPON': 'India Nippon Electricals Limited', 'INDOCO': 'Indoco Remedies Limited', 'INDOTHAI': 'Indo Thai Securities Limited', 'INDRAMEDCO': 'Indraprastha Medical Corporation Limited', 'INDUSINDBK': 'IndusInd Bank Limited', 'INDUSTOWER': 'Indus Towers Limited', 'INEOSSTYRO': 'INEOS Styrolution India Limited', 'INFIBEAM': 'Infibeam Avenues Limited', 'INFY': 'Infosys Limited', 'INOXLEISUR': 'INOX Leisure Limited', 'INOXWIND': 'Inox Wind Limited', 'INSECTICID': 'Insecticides (India) Limited', 'INTELLECT': 'Intellect Design Arena Limited', 'INVENTURE': 'Inventure Growth & Securities Limited', 'IOLCP': 'IOL Chemicals and Pharmaceuticals Limited', 'IPL': 'India Pesticides Limited', 'IRB': 'IRB Infrastructure Developers Limited', 'IRCON': 'Ircon International Limited', 'ISEC': 'ICICI Securities Limited', 'ISGEC': 'Isgec Heavy Engineering Limited', 'ITC': 'ITC Limited', 'ITI': 'ITI Limited', 'IWEL': 'Inox Wind Energy Limited', 'IZMO': 'IZMO Limited', 'JAICORPLTD': 'Jai Corp Limited', 'JAMNAAUTO': 'Jamna Auto Industries Limited', 'JASH': 'Jash Engineering Limited', 'JAYSREETEA': 'Jayshree Tea & Industries Limited', 'JBCHEPHARM': 'JB Chemicals & Pharmaceuticals Limited', 'JBMA': 'JBM Auto Limited', 'JCHAC': 'Johnson Controls - Hitachi Air Conditioning India Limited', 'JINDALSAW': 'Jindal Saw Limited', 'JINDALSTEL': 'Jindal Steel & Power Limited', 'JISLDVREQS': 'Jain Irrigation Systems Limited', 'JISLJALEQS': 'Jain Irrigation Systems Limited', 'JKLAKSHMI': 'JK Lakshmi Cement Limited', 'JKPAPER': 'JK Paper Limited', 'JKTYRE': 'JK Tyre & Industries Limited', 'JMCPROJECT': 'JMC Projects (India)  Limited', 'JMFINANCIL': 'JM Financial Limited', 'JPPOWER': 'Jaiprakash Power Ventures Limited', 'JSL': 'Jindal Stainless Limited', 'JSLHISAR': 'Jindal Stainless (Hisar) Limited', 'JSWENERGY': 'JSW Energy Limited', 'JSWISPL': 'JSW Ispat Special Products Limited', 'JSWSTEEL': 'JSW Steel Limited', 'JTEKTINDIA': 'Jtekt India Limited', 'JUBLFOOD': 'Jubilant Foodworks Limited', 'JUBLINGREA': 'Jubilant Ingrevia Limited', 'JUBLPHARMA': 'Jubilant Pharmova Limited', 'JUSTDIAL': 'Just Dial Limited', 'JYOTHYLAB': 'Jyothy Labs Limited', 'KAJARIACER': 'Kajaria Ceramics Limited', 'KAKATCEM': 'Kakatiya Cement Sugar & Industries Limited', 'KALPATPOWR': 'Kalpataru Power Transmission Limited', 'KALYANKJIL': 'Kalyan Jewellers India Limited', 'KAMDHENU': 'Kamdhenu Limited', 'KANSAINER': 'Kansai Nerolac Paints Limited', 'KAPSTON': 'Kapston Facilities Management Limited', 'KARDA': 'Karda Constructions Limited', 'KARURVYSYA': 'Karur Vysya Bank Limited', 'KCP': 'KCP Limited', 'KCPSUGIND': 'KCP Sugar and Industries Corporation Limited', 'KEI': 'KEI Industries Limited', 'KELLTONTEC': 'Kellton Tech Solutions Limited', 'KESORAMIND': 'Kesoram Industries Limited', 'KHADIM': 'Khadim India Limited', 'KHANDSE': 'Khandwala Securities Limited', 'KILITCH': 'Kilitch Drugs (India) Limited', 'KIOCL': 'KIOCL Limited', 'KIRIINDUS': 'Kiri Industries Limited', 'KIRLOSIND': 'Kirloskar Industries Limited', 'KNRCON': 'KNR Constructions Limited', 'KOTAKBANK': 'Kotak Mahindra Bank Limited', 'KOTHARIPET': 'Kothari Petrochemicals Limited', 'KPITTECH': 'KPIT Technologies Limited', 'KRBL': 'KRBL Limited', 'KREBSBIO': 'Krebs Biochemicals and Industries Limited', 'KSCL': 'Kaveri Seed Company Limited', 'KSL': 'Kalyani Steels Limited', 'KTKBANK': 'The Karnataka Bank Limited', 'L&TFH': 'L&T Finance Holdings Limited', 'LAKPRE': 'Lakshmi Precision Screws Limited', 'LAOPALA': 'La Opala RG Limited', 'LAURUSLABS': 'Laurus Labs Limited', 'LAXMIMACH': 'Lakshmi Machine Works Limited', 'LEMONTREE': 'Lemon Tree Hotels Limited', 'LGBBROSLTD': 'LG Balakrishnan & Bros Limited', 'LICHSGFIN': 'LIC Housing Finance Limited', 'LIKHITHA': 'Likhitha Infrastructure Limited', 'LINDEINDIA': 'Linde India Limited', 'LODHA': 'Macrotech Developers Limited', 'LT': 'Larsen & Toubro Limited', 'LTI': 'Larsen & Toubro Infotech Limited', 'LTTS': 'L&T Technology Services Limited', 'LUPIN': 'Lupin Limited', 'LUXIND': 'Lux Industries Limited', 'LXCHEM': 'Laxmi Organic Industries Limited', 'MAGMA': 'Magma Fincorp Limited', 'MAHABANK': 'Bank of Maharashtra', 'MAHEPC': 'Mahindra EPC Irrigation Limited', 'MAHESHWARI': 'Maheshwari Logistics Limited', 'MAHINDCIE': 'Mahindra CIE Automotive Limited', 'MAHLIFE': 'Mahindra Lifespace Developers Limited', 'MAHLOG': 'Mahindra Logistics Limited', 'MAITHANALL': 'Maithan Alloys Limited', 'MANALIPETC': 'Manali Petrochemicals Limited', 'MANAPPURAM': 'Manappuram Finance Limited', 'MANGCHEFER': 'Mangalore Chemicals & Fertilizers Limited', 'MANGLMCEM': 'Mangalam Cement Limited', 'MANINDS': 'Man Industries (India) Limited', 'MARICO': 'Marico Limited', 'MARINE': 'Marine Electricals (India) Limited', 'MARKSANS': 'Marksans Pharma Limited', 'MARUTI': 'Maruti Suzuki India Limited', 'MASTEK': 'Mastek Limited', 'MATRIMONY': 'Matrimony.Com Limited', 'MAXHEALTH': 'Max Healthcare Institute Limited', 'MAXVIL': 'Max Ventures and Industries Limited', 'MAZDOCK': 'Mazagon Dock Shipbuilders Limited', 'MCDOWELL-N': 'United Spirits Limited', 'METROPOLIS': 'Metropolis Healthcare Limited', 'MFSL': 'Max Financial Services Limited', 'MGL': 'Mahanagar Gas Limited', 'MHRIL': 'Mahindra Holidays & Resorts India Limited', 'MIDHANI': 'Mishra Dhatu Nigam Limited', 'MINDACORP': 'Minda Corporation Limited', 'MINDAIND': 'Minda Industries Limited', 'MINDTREE': 'MindTree Limited', 'MMFL': 'MM Forgings Limited', 'MMP': 'MMP Industries Limited', 'MOIL': 'MOIL Limited', 'MOLDTKPAC': 'Mold-Tek Packaging Limited', 'MOREPENLAB': 'Morepen Laboratories Limited', 'MOTHERSUMI': 'Motherson Sumi Systems Limited', 'MOTILALOFS': 'Motilal Oswal Financial Services Limited', 'MPHASIS': 'MphasiS Limited', 'MRF': 'MRF Limited', 'MSTCLTD': 'Mstc Limited', 'MTARTECH': 'Mtar Technologies Limited', 'MUNJALAU': 'Munjal Auto Industries Limited', 'MUTHOOTFIN': 'Muthoot Finance Limited', 'NAHARCAP': 'Nahar Capital and Financial Services Limited', 'NAHARPOLY': 'Nahar Poly Films Limited', 'NAM-INDIA': 'Nippon Life India Asset Management Limited', 'NATCOPHARM': 'Natco Pharma Limited', 'NAUKRI': 'Info Edge (India) Limited', 'NAVINFLUOR': 'Navin Fluorine International Limited', 'NAVNETEDUL': 'Navneet Education Limited', 'NAZARA': 'Nazara Technologies Limited', 'NBCC': 'NBCC (India) Limited', 'NBVENTURES': 'Nava Bharat Ventures Limited', 'NCC': 'NCC Limited', 'NCLIND': 'NCL Industries Limited', 'NELCO': 'NELCO Limited', 'NESCO': 'Nesco Limited', 'NESTLEIND': 'Nestle India Limited', 'NEULANDLAB': 'Neuland Laboratories Limited', 'NEWGEN': 'Newgen Software Technologies Limited', 'NH': 'Narayana Hrudayalaya Ltd.', 'NHPC': 'NHPC Limited', 'NIITLTD': 'NIIT Limited', 'NILKAMAL': 'Nilkamal Limited', 'NIPPOBATRY': 'Indo-National Limited', 'NITCO': 'Nitco Limited', 'NITINFIRE': 'Nitin Fire Protection Industries Limited', 'NITINSPIN': 'Nitin Spinners Limited', 'NITIRAJ': 'Nitiraj Engineers Limited', 'NLCINDIA': 'NLC India Limited', 'NMDC': 'NMDC Limited', 'NOCIL': 'NOCIL Limited', 'NTPC': 'NTPC Limited', 'NURECA': 'Nureca Limited', 'OBEROIRLTY': 'Oberoi Realty Limited', 'OCCL': 'Oriental Carbon & Chemicals Limited', 'OIL': 'Oil India Limited', 'OLECTRA': 'Olectra Greentech Limited', 'ONMOBILE': 'OnMobile Global Limited', 'ORIENTCEM': 'Orient Cement Limited', 'ORIENTELEC': 'Orient Electric Limited', 'ORIENTPPR': 'Orient Paper & Industries Limited', 'PAGEIND': 'Page Industries Limited', 'PALASHSECU': 'Palash Securities Limited', 'PANACHE': 'Panache Digilife Limited', 'PANAMAPET': 'Panama Petrochem Limited', 'PARAGMILK': 'Parag Milk Foods Limited', 'PATELENG': 'Patel Engineering Limited', 'PCJEWELLER': 'PC Jeweller Limited', 'PDSMFL': 'PDS Multinational Fashions Limited', 'PEL': 'Piramal Enterprises Limited', 'PERSISTENT': 'Persistent Systems Limited', 'PETRONET': 'Petronet LNG Limited', 'PFC': 'Power Finance Corporation Limited', 'PFIZER': 'Pfizer Limited', 'PFS': 'PTC India Financial Services Limited', 'PGIL': 'Pearl Global Industries Limited', 'PHILIPCARB': 'Phillips Carbon Black Limited', 'PHOENIXLTD': 'The Phoenix Mills Limited', 'PIDILITIND': 'Pidilite Industries Limited', 'PIIND': 'PI Industries Limited', 'PIONDIST': 'Pioneer Distilleries Limited', 'PIONEEREMB': 'Pioneer Embroideries Limited', 'PITTIENG': 'Pitti Engineering Limited', 'PNBGILTS': 'PNB Gilts Limited', 'PNBHOUSING': 'PNB Housing Finance Limited', 'PNC': 'Pritish Nandy Communications Limited', 'PNCINFRA': 'PNC Infratech Limited', 'POKARNA': 'Pokarna Limited', 'POLYCAB': 'Polycab India Limited', 'POLYMED': 'Poly Medicure Limited', 'POLYPLEX': 'Polyplex Corporation Limited', 'POWERGRID': 'Power Grid Corporation of India Limited', 'POWERINDIA': 'ABB Power Products and Systems India Limited', 'PRAJIND': 'Praj Industries Limited', 'PRAKASH': 'Prakash Industries Limited', 'PRECAM': 'Precision Camshafts Limited', 'PRECOT': 'Precot Limited', 'PRECWIRE': 'Precision Wires India Limited', 'PRESTIGE': 'Prestige Estates Projects Limited', 'PRICOLLTD': 'Pricol Limited', 'PRIMESECU': 'Prime Securities Limited', 'PRINCEPIPE': 'Prince Pipes And Fittings Limited', 'PRIVISCL': 'Privi Speciality Chemicals Limited', 'PRSMJOHNSN': 'Prism Johnson Limited', 'PSPPROJECT': 'PSP Projects Limited', 'PTC': 'PTC India Limited', 'PURVA': 'Puravankara Limited', 'PVR': 'PVR Limited', 'QUESS': 'Quess Corp Limited', 'QUICKHEAL': 'Quick Heal Technologies Limited', 'RADICO': 'Radico Khaitan Limited', 'RAILTEL': 'Railtel Corporation Of India Limited', 'RAIN': 'Rain Industries Limited', 'RAJESHEXPO': 'Rajesh Exports Limited', 'RALLIS': 'Rallis India Limited', 'RAMCOCEM': 'The Ramco Cements Limited', 'RAMCOSYS': 'Ramco Systems Limited', 'RANEHOLDIN': 'Rane Holdings Limited', 'RAYMOND': 'Raymond Limited', 'RBLBANK': 'RBL Bank Limited', 'RCF': 'Rashtriya Chemicals and Fertilizers Limited', 'RCOM': 'Reliance Communications Limited', 'RECLTD': 'REC Limited', 'REDINGTON': 'Redington (India) Limited', 'RELAXO': 'Relaxo Footwears Limited', 'RELCAPITAL': 'Reliance Capital Limited', 'RELIANCE': 'Reliance Industries Limited', 'RELIGARE': 'Religare Enterprises Limited', 'RELINFRA': 'Reliance Infrastructure Limited', 'RENUKA': 'Shree Renuka Sugars Limited', 'REPCOHOME': 'Repco Home Finance Limited', 'RHFL': 'Reliance Home Finance Limited', 'RHIM': 'RHI MAGNESITA INDIA LIMITED', 'RICOAUTO': 'Rico Auto Industries Limited', 'RIIL': 'Reliance Industrial Infrastructure Limited', 'RITES': 'RITES Limited', 'RNAVAL': 'Reliance Naval and Engineering Limited', 'ROSSARI': 'Rossari Biotech Limited', 'ROSSELLIND': 'Rossell India Limited', 'ROUTE': 'ROUTE MOBILE LIMITED', 'RPOWER': 'Reliance Power Limited', 'RPSGVENT': 'RPSG VENTURES LIMITED', 'RSWM': 'RSWM Limited', 'RTNINDIA': 'RattanIndia Enterprises Limited', 'RUBYMILLS': 'The Ruby Mills Limited', 'RUSHIL': 'Rushil Decor Limited', 'S&SPOWER': 'S&S Power Switchgears Limited', 'SAGCEM': 'Sagar Cements Limited', 'SAKAR': 'Sakar Healthcare Limited', 'SALASAR': 'Salasar Techno Engineering Limited', 'SANGHIIND': 'Sanghi Industries Limited', 'SANOFI': 'Sanofi India Limited', 'SARDAEN': 'Sarda Energy & Minerals Limited', 'SAREGAMA': 'Saregama India Limited', 'SARLAPOLY': 'Sarla Performance Fibers Limited', 'SATIN': 'Satin Creditcare Network Limited', 'SBCL': 'Shivalik Bimetal Controls Limited', 'SBICARD': 'SBI Cards and Payment Services Limited', 'SBILIFE': 'SBI Life Insurance Company Limited', 'SBIN': 'State Bank of India', 'SCHAEFFLER': 'Schaeffler India Limited', 'SCI': 'Shipping Corporation Of India Limited', 'SEAMECLTD': 'Seamec Limited', 'SEQUENT': 'Sequent Scientific Limited', 'SHALBY': 'Shalby Limited', 'SHANKARA': 'Shankara Building Products Limited', 'SHANTIGEAR': 'Shanthi Gears Limited', 'SHARDACROP': 'Sharda Cropchem Limited', 'SHAREINDIA': 'Share India Securities Limited', 'SHILPAMED': 'Shilpa Medicare Limited', 'SHK': 'S H Kelkar and Company Limited', 'SHREDIGCEM': 'Shree Digvijay Cement Co.Ltd', 'SHYAMCENT': 'Shyam Century Ferrous Limited', 'SHYAMMETL': 'Shyam Metalics and Energy Limited', 'SIEMENS': 'Siemens Limited', 'SINTERCOM': 'Sintercom India Limited', 'SIS': 'SIS LIMITED', 'SITINET': 'Siti Networks Limited', 'SIYSIL': 'Siyaram Silk Mills Limited', 'SJVN': 'SJVN Limited', 'SKFINDIA': 'SKF India Limited', 'SMCGLOBAL': 'SMC Global Securities Limited', 'SMSPHARMA': 'SMS Pharmaceuticals Limited', 'SOBHA': 'Sobha Limited', 'SOLARA': 'Solara Active Pharma Sciences Limited', 'SOLARINDS': 'Solar Industries India Limited', 'SONACOMS': 'Sona BLW Precision Forgings Limited', 'SONATSOFTW': 'Sonata Software Limited', 'SOTL': 'Savita Oil Technologies Limited', 'SOUTHBANK': 'The South Indian Bank Limited', 'SPARC': 'Sun Pharma Advanced Research Company Limited', 'SPECIALITY': 'Speciality Restaurants Limited', 'SPICEJET': 'SPICEJET LTD', 'SPLIL': 'SPL Industries Limited', 'SRF': 'SRF Limited', 'SRIPIPES': 'Srikalahasthi Pipes Limited', 'SRTRANSFIN': 'Shriram Transport Finance Company Limited', 'SSWL': 'Steel Strips Wheels Limited', 'STAR': 'Strides Pharma Science Limited', 'STEELCITY': 'Steel City Securities Limited', 'STEELXIND': 'STEEL EXCHANGE INDIA LIMITED', 'STLTECH': 'Sterlite Technologies Limited', 'STOVEKRAFT': 'Stove Kraft Limited', 'SUBEXLTD': 'Subex Limited', 'SUBROS': 'Subros Limited', 'SUDARSCHEM': 'Sudarshan Chemical Industries Limited', 'SUMICHEM': 'Sumitomo Chemical India Limited', 'SUMMITSEC': 'Summit Securities Limited', 'SUNCLAYLTD': 'Sundaram Clayton Limited', 'SUNDARAM': 'Sundaram Multi Pap Limited', 'SUNDARMFIN': 'Sundaram Finance Limited', 'SUNDARMHLD': 'Sundaram Finance Holdings Limited', 'SUNDRMBRAK': 'Sundaram Brake Linings Limited', 'SUNFLAG': 'Sunflag Iron And Steel Company Limited', 'SUNPHARMA': 'Sun Pharmaceutical Industries Limited', 'SUNTECK': 'Sunteck Realty Limited', 'SUNTV': 'Sun TV Network Limited', 'SUPRAJIT': 'Suprajit Engineering Limited', 'SUPREMEIND': 'Supreme Industries Limited', 'SURYAROSNI': 'Surya Roshni Limited', 'SUTLEJTEX': 'Sutlej Textiles and Industries Limited', 'SUVEN': 'Suven Life Sciences Limited', 'SUVENPHAR': 'Suven Pharmaceuticals Limited', 'SUZLON': 'Suzlon Energy Limited', 'SYMPHONY': 'Symphony Limited', 'TAKE': 'Take Solutions Limited', 'TALBROAUTO': 'Talbros Automotive Components Limited', 'TARC': 'Anant Raj Global Limited', 'TATACHEM': 'Tata Chemicals Limited', 'TATACOFFEE': 'Tata Coffee Limited', 'TATACOMM': 'Tata Communications Limited', 'TATAELXSI': 'Tata Elxsi Limited', 'TATAMETALI': 'Tata Metaliks Limited', 'TATAMOTORS': 'Tata Motors Limited', 'TATAMTRDVR': 'Tata Motors Limited', 'TATAPOWER': 'Tata Power Company Limited', 'TATASTEEL': 'Tata Steel Limited', 'TATASTLBSL': 'Tata Steel Bsl Limited', 'TATASTLLP': 'Tata Steel Long Products Limited', 'TATVA': 'Tatva Chintan Pharma Chem Limited', 'TBZ': 'Tribhovandas Bhimji Zaveri Limited', 'TCI': 'Transport Corporation of India Limited', 'TCIEXP': 'TCI Express Limited', 'TCNSBRANDS': 'TCNS Clothing Co. Limited', 'TECHM': 'Tech Mahindra Limited', 'TEXRAIL': 'Texmaco Rail & Engineering Limited', 'THANGAMAYL': 'Thangamayil Jewellery Limited', 'THERMAX': 'Thermax Limited', 'THYROCARE': 'Thyrocare Technologies Limited', 'TIDEWATER': 'Tide Water Oil Company (India) Limited', 'TIINDIA': 'Tube Investments of India Limited', 'TINPLATE': 'The Tinplate Company of India Limited', 'TIRUMALCHM': 'Thirumalai Chemicals Limited', 'TITAN': 'Titan Company Limited', 'TNPETRO': 'Tamilnadu PetroProducts Limited', 'TORNTPHARM': 'Torrent Pharmaceuticals Limited', 'TORNTPOWER': 'Torrent Power Limited', 'TREEHOUSE': 'Tree House Education & Accessories Limited', 'TRENT': 'Trent Limited', 'TRIDENT': 'Trident Limited', 'TRIL': 'Transformers And Rectifiers (India) Limited', 'TTKPRESTIG': 'TTK Prestige Limited', 'TV18BRDCST': 'TV18 Broadcast Limited', 'TVSMOTOR': 'TVS Motor Company Limited', 'TVSSRICHAK': 'TVS Srichakra Limited', 'TWL': 'Titagarh Wagons Limited', 'UBL': 'United Breweries Limited', 'UFLEX': 'UFLEX Limited', 'UFO': 'UFO Moviez India Limited', 'UJJIVAN': 'Ujjivan Financial Services Limited', 'UJJIVANSFB': 'Ujjivan Small Finance Bank Limited', 'UMESLTD': 'Usha Martin Education & Solutions Limited', 'UNIDT': 'United Drilling Tools Limited', 'UNIONBANK': 'Union Bank of India', 'UPL': 'UPL Limited', 'USHAMART': 'Usha Martin Limited', 'VADILALIND': 'Vadilal Industries Limited', 'VAKRANGEE': 'Vakrangee Limited', 'VALIANTORG': 'Valiant Organics Limited', 'VARDHACRLC': 'Vardhman Acrylics Limited', 'VBL': 'Varun Beverages Limited', 'VEDL': 'Vedanta Limited', 'VETO': 'Veto Switchgears And Cables Limited', 'VGUARD': 'V-Guard Industries Limited', 'VIDHIING': 'Vidhi Specialty Food Ingredients Limited', 'VINATIORGA': 'Vinati Organics Limited', 'VIPIND': 'VIP Industries Limited', 'VISAKAIND': 'Visaka Industries Limited', 'VISHAL': 'Vishal Fabrics Limited', 'VMART': 'V-Mart Retail Limited', 'VOLTAMP': 'Voltamp Transformers Limited', 'VOLTAS': 'Voltas Limited', 'VRLLOG': 'VRL Logistics Limited', 'VTL': 'Vardhman Textiles Limited', 'WABAG': 'VA Tech Wabag Limited', 'WABCOINDIA': 'WABCO India Limited', 'WELCORP': 'Welspun Corp Limited', 'WELSPUNIND': 'Welspun India Limited', 'WHEELS': 'Wheels India Limited', 'WHIRLPOOL': 'Whirlpool of India Limited', 'WIPRO': 'Wipro Limited', 'WOCKPHARMA': 'Wockhardt Limited', 'WONDERLA': 'Wonderla Holidays Limited', 'WSTCSTPAPR': 'West Coast Paper Mills Limited', 'XCHANGING': 'Xchanging Solutions Limited', 'YESBANK': 'Yes Bank Limited', 'ZEEL': 'Zee Entertainment Enterprises Limited', 'ZENSARTECH': 'Zensar Technologies Limited', 'ZOMATO': 'Zomato Limited', 'ZOTA': 'Zota Health Care LImited', 'ZYDUSWELL': 'Zydus Wellness Limited'}

candle_stick = 0
count = 0
amountPerStock = 5000

def get_filenames(Date_Range):
    # IST = pytz.timezone('Asia/Kolkata')
    # ist_today = datetime.datetime.now(IST)
    # ist_prevDay = ist_today - datetime.timedelta(days=1)
    # return str(ist_today.strftime('%Y-%m-%d')), str(ist_prevDay.strftime('%Y-%m-%d'))
    return str(Date_Range[-1].strftime('%Y-%m-%d')), str(Date_Range[-2].strftime('%Y-%m-%d'))


def message_handler(data, candle_response, volume_response, technical_response, sr_response):
    t = PrettyTable(['Bullish', candle_response['candle_stick']['stock_id']])
    t.add_row(['Quantity       ', math.ceil(amountPerStock / data['close'][-1])])
    t.add_row(['Buy       ', round(data['close'][-1], 2)])
    t.add_row(['StopLoss  ', round(data['low'][-1], 2)])
    t.add_row(['Candle    ', candle_response['candle_stick']['pattern']])
    t.add_row(['Technical ', technical_response['technical_indicator']["pattern"]])
    t.add_row(['SR        ', sr_response['sr_indicator']["pattern"]])
    t.add_row(['SR_Value  ', round(sr_response['sr_indicator']["level"], 2)])
    return t


def format_df(df):
    table = PrettyTable([''] + list(df.columns))
    for row in df.itertuples():
        table.add_row(row)
    return str(table)


def telegram_notification(message):
    response = requests.post("https://api.telegram.org/bot1898967363:AAFKsxIHb3HlCkLl7SZcM8FcSS2tP0llmlc/sendMessage",
                             params={'chat_id': '-544542415', 'text': message})


starttime = datetime.datetime.now()
Report = []
today = ''
prevDay = ''
for stock_id, stock_name in FinalStockList.items():
    try:
        print(count, end='\r\n')
        data = yf.Ticker(str(stock_id) + '.NS').history(period='1y')
        data.columns = ['open', 'high', 'low', 'close', 'Volume', 'Dividends', 'Stock Splits']
        candle_response = brain_candle.candle_stick(data, stock_id, stock_name)
        volume_response = volume_indicator.volume_indicate(data, stock_id, stock_name)
        technical_response = technical_indicator.technical_indicate(data, stock_id, stock_name)
        sr_response = sr_indicator.sr_indicate(data, stock_id, stock_name)
        count += 1
        today, prevDay = get_filenames(data.index)
        if candle_response['candle_stick']['indicator'] and volume_response['volume_indicator']['indicator'] and \
                technical_response['technical_indicator']["indicator"] and sr_response['sr_indicator']["indicator"]:
            candle_stick += 1
            Close_Price=round(data['close'][-1],2)
            Report.append([stock_id,Close_Price,amountPerStock//Close_Price])
            print('{} - {}'.format(stock_id, stock_name))
            message = message_handler(data, candle_response, volume_response, technical_response, sr_response)
            telegram_notification(message)
    except Exception as e:
        print(e)

try:
    Report_Data = pd.DataFrame(Report, index=None)
    Report_Data.columns = ['Stock ID', 'Close Price', 'Quantity']
    Report_Data.sort_values('Close Price', inplace=True)
    telegram_notification(format_df(Report_Data))
    Report_Data.to_csv('/Users/jyotijen/Desktop/StockRecommend/' + today + '.csv')
    Performance, Income, Investment = handler.performance_calculate(prevDay, amountPerStock)
    telegram_notification(format_df(Performance))
    telegram_notification('Investment: {} Income: {}'.format(Investment, Income))

except Exception as e:
    print(e)

TotalTime = format_timespan((datetime.datetime.now() - starttime).total_seconds())
telegram_notification('Total Time Consumed:{}'.format(TotalTime))