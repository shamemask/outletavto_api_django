import asyncio
import os

from asgiref.sync import sync_to_async
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView

from .api_client import Pr_Lg, RosskoAPI, ABCP
import pandas as pd
from tabulate import tabulate
import json
all_numbers =[
['55263','3Ton'],
['TC545','3Ton'],
['AB404','ABRO'],
['AB505','ABRO'],
['AB8200RW','ABRO'],
['CC200','ABRO'],
['DA650','ABRO'],
['ES332','ABRO'],
['FC650','ABRO'],
['SL624','ABRO'],
['AGA002Z','AGA'],
['AGA048Z','AGA'],
['A1539','AIKO'],
['A9426','AIKO'],
['C218','AIKO'],
['O118','AIKO'],
['EF400','AIM-ONE'],
['OT390','AIM-ONE'],
['AITC01','AIRLINE'],
['ATRCS03','AIRLINE'],
['ATRCS06','AIRLINE'],
['SA30011S','AIRLINE'],
['SP1296','ALCO Filters'],
['MO533','AMC Filter'],
['SO801','AMC Filter'],
['TF1652','AMC Filter'],
['MO511','AMC'],
['MO511','AMC'],
['AMDEL447','AMD'],
['AMDFA17','AMD'],
['AMDFA27','AMD'],
['AMDFA343','AMD'],
['AMDFA38','AMD'],
['AMDFA397','AMD'],
['AMDFA41','AMD'],
['AMDFA418','AMD'],
['AMDFA43','AMD'],
['AMDFA46','AMD'],
['AMDFA52','AMD'],
['AMDFA57','AMD'],
['AMDFA734','AMD'],
['AMDFA749','AMD'],
['AMDFA773','AMD'],
['AMDFA774','AMD'],
['AMDFA775','AMD'],
['AMDFA777','AMD'],
['AMDFA791','AMD'],
['AMDFA791','AMD'],
['AMDFA794','AMD'],
['AMDFA91','AMD'],
['AMDFC167','AMD'],
['AMDFC167','AMD'],
['AMDFC17','AMD'],
['AMDFC173','AMD'],
['AMDFC22','AMD'],
['AMDFC25','AMD'],
['AMDFC28','AMD'],
['AMDFC28','AMD'],
['AMDFC29','AMD'],
['AMDFC32','AMD'],
['AMDFC32A','AMD'],
['AMDFC39','AMD'],
['AMDFC53','AMD'],
['AMDFC53','AMD'],
['AMDFC738','AMD'],
['AMDFC738','AMD'],
['AMDFC739','AMD'],
['AMDFC742','AMD'],
['AMDFC753','AMD'],
['AMDFC753A','AMD'],
['AMDFC753C','AMD'],
['AMDFC753C','AMD'],
['AMDFC756C','AMD'],
['AMDFC785','AMD'],
['AMDFC788','AMD'],
['AMDFC811','AMD'],
['AMDFC819','AMD'],
['AMDFC842','AMD'],
['AMDFC842','AMD'],
['AMDFC842','AMD'],
['AMDFL14','AMD'],
['AMDFL25','AMD'],
['AMDFL25','AMD'],
['AMDFL285','AMD'],
['AMDJFA89','AMD'],
['AMDJFA89','AMD'],
['AMDJFC73C','AMD'],
['AMDJFC74','AMD'],
['AMDJFC96C','AMD'],
['AMDREN333','AMD'],
['AFK771210','ANYU'],
['AFK771276','ANYU'],
['ABP01','AREON'],
['ABP02','AREON'],
['ABP02','AREON'],
['ABP03','AREON'],
['APL02','AREON'],
['APL02','AREON'],
['APL04','AREON'],
['AXV05','AREON'],
['LR05','AREON'],
['LR07','AREON'],
['LR12','AREON'],
['ASINFA2396','ASIN'],
['ASINFA2578','ASIN'],
['ASINFA2583','ASIN'],
['ASINFA2624','ASIN'],
['ASINFA2631','ASIN'],
['ASINFC217','ASIN'],
['ASINFC217','ASIN'],
['347049B','ASSO'],
['AC267','ASTROHIM'],
['AC8602','ASTROHIM'],
['AC8606','ASTROHIM'],
['A01508401','AUTOBACS'],
['A01508404','AUTOBACS'],
['AV931010','AV Steel'],
['43733','AVS'],
['43734','AVS'],
['80393','AVS'],
['A78077S','AVS'],
['410000010','AWM'],
['410000011','AWM'],
['410000012','AWM'],
['410000014','AWM'],
['410000016','AWM'],
['410000019','AWM'],
['410000020','AWM'],
['410000021','AWM'],
['410000024','AWM'],
['410000026','AWM'],
['410000028','AWM'],
['410000030','AWM'],
['410000031','AWM'],
['410000032','AWM'],
['410000033','AWM'],
['410000035','AWM'],
['410000037','AWM'],
['410000038','AWM'],
['410000039','AWM'],
['410000040','AWM'],
['410000042','AWM'],
['410000088','AWM'],
['430600085','AWM'],
['439P00905','AWM'],
['WPZ934','Aisin'],
['0420505','Akitaka'],
['ARG131050L','Arirang'],
['ARG131050R','Arirang'],
['ARG322512','Arirang'],
['ARG324132','Arirang'],
['ARG324343','Arirang'],
['ARG324713','Arirang'],
['1001195','Ashika'],
['1002279','Ashika'],
['USM18','Auto-GUR'],
['P119','Autopartner'],
['U891','Autopartner'],
['75377710','Avar'],
['BK4938','B-RING'],
['GB9833C','BIG FILTER'],
['GB9909','BIG FILTER'],
['FA1130','BM-Motorsport'],
['FA1263','BM-Motorsport'],
['FA2227','BM-Motorsport'],
['FA2527','BM-Motorsport'],
['13717590597','BMW'],
['BRF23','BRAVE'],
['1001','Bardahl'],
['36161','Bardahl'],
['36162','Bardahl'],
['36163','Bardahl'],
['36311','Bardahl'],
['36312','Bardahl'],
['36313','Bardahl'],
['36333','Bardahl'],
['4042','BiBiCare'],
['ADG02376','Blue Print'],
['ADG02376','Blue Print'],
['VW0LT97020L','BodyParts'],
['0241235752','Bosch'],
['0451103033','Bosch'],
['1417010997','Bosch'],
['1457070001','Bosch'],
['1457429619','Bosch'],
['1987948403','Bosch'],
['F026407069','Bosch'],
['L04010','Brembo'],
['P85098','Brembo'],
['10701900','Bullsone'],
['15674020','Bullsone'],
['15674021','Bullsone'],
['15674023','Bullsone'],
['15674024','Bullsone'],
['30027901','Bullsone'],
['080457','CARGO'],
['8204111','CHAMPION OIL'],
['8211652','CHAMPION OIL'],
['CA500200','COSMOFEN'],
['CE0349','CTR'],
['CL0374','CTR'],
['GV0009','CTR'],
['GV0041','CTR'],
['A130R2001','CWORKS'],
['A130R3001','CWORKS'],
['A130R3004','CWORKS'],
['A22SR1004','CWORKS'],
['G7400029','Carville Racing'],
['15A4E0','Castrol'],
['COF100571E','Champion'],
['19034917B','Corteco'],
['10FCA00057000','DEQST'],
['MTMR0109453','DOMINANT'],
['DFA1103','DOUBLE FORCE'],
['DFA16134','DOUBLE FORCE'],
['DFA173','DOUBLE FORCE'],
['DFA2244','DOUBLE FORCE'],
['DFA26168','DOUBLE FORCE'],
['DFA2628','DOUBLE FORCE'],
['DFA27107','DOUBLE FORCE'],
['DFA28010','DOUBLE FORCE'],
['DFA3028','DOUBLE FORCE'],
['DFC2336','DOUBLE FORCE'],
['DFC2442','DOUBLE FORCE'],
['DFC27007','DOUBLE FORCE'],
['DAF1286','DYNAMATRIX-KOREA'],
['DAF786','DYNAMATRIX-KOREA'],
['DCFK191S','DYNAMATRIX-KOREA'],
['DOFX258D','DYNAMATRIX-KOREA'],
['KTB296','Dayco'],
['SS20205','Delphi'],
['TC1150','Delphi'],
['TC2170','Delphi'],
['TC2373','Delphi'],
['A141759','Denckermann'],
['10318BLACK20M','Denka'],
['DCF588P','Denso'],
['223010','EAG'],
['10170301','ELF'],
['213914','ELF'],
['EL020301','ELTRANS'],
['EL020301','ELTRANS'],
['EL090103','ELTRANS'],
['8809478942162','ENEOS'],
['EKO0403','Ekofil'],
['634380','Elring'],
['ENI0W20ISINT5','Eni'],
['NSC615','Exedy'],
['1445005','FORD'],
['15595A','FORD'],
['15CF54','FORD'],
['1781003','FORD'],
['1883037','FORD'],
['1883037','FORD'],
['4611835','FORD'],
['256781','FORTLUFT'],
['HYABACF3','Febest'],
['MAB102','Febest'],
['01381','Febi'],
['06162','Febi'],
['06162','Febi'],
['109207','Febi'],
['21829','Febi'],
['22548','Febi'],
['24575','Febi'],
['30096','Febi'],
['31091','Febi'],
['31092','Febi'],
['34918','Febi'],
['410030153','Felix'],
['410030154','Felix'],
['410040169','Felix'],
['410060007','Felix'],
['411040015','Felix'],
['411040021','Felix'],
['411040022','Felix'],
['411040058','Felix'],
['411040063','Felix'],
['411040064','Felix'],
['411040065','Felix'],
['411040087','Felix'],
['411040093','Felix'],
['411040096','Felix'],
['411040097','Felix'],
['411040111','Felix'],
['411040115','Felix'],
['411040116','Felix'],
['411040154','Felix'],
['411041035','Felix'],
['411041036','Felix'],
['411041043','Felix'],
['430130005','Felix'],
['430130005','Felix'],
['430206026','Felix'],
['430206027','Felix'],
['430206030','Felix'],
['430206030','Felix'],
['430206031','Felix'],
['430206031','Felix'],
['430206032','Felix'],
['430206032','Felix'],
['430206033','Felix'],
['430206246','Felix'],
['430206370','Felix'],
['430206371','Felix'],
['430206371','Felix'],
['430207014','Felix'],
['A30206031','Felix'],
['A30206033','Felix'],
['FN246','Fenom'],
['FN403','Fenom'],
['AK2187','Filtron'],
['AP0743','Filtron'],
['AP1031','Filtron'],
['K1078','Filtron'],
['OE6408','Filtron'],
['OE6501','Filtron'],
['OE6652','Filtron'],
['OE6714','Filtron'],
['OE6882','Filtron'],
['OM513','Filtron'],
['OP595','Filtron'],
['OP617','Filtron'],
['OP6292','Filtron'],
['AF919','Finwhale'],
['LF513','Finwhale'],
['FA003','Fortech'],
['FA004','Fortech'],
['FA008','Fortech'],
['FA017','Fortech'],
['FA020','Fortech'],
['FA020','Fortech'],
['FA022','Fortech'],
['FA026','Fortech'],
['FA036','Fortech'],
['FA040','Fortech'],
['FA041','Fortech'],
['FA053','Fortech'],
['FA065','Fortech'],
['FA065','Fortech'],
['FA114','Fortech'],
['FA115','Fortech'],
['FA121','Fortech'],
['FA122','Fortech'],
['FA134','Fortech'],
['FA180','Fortech'],
['FA180','Fortech'],
['FA182','Fortech'],
['FA189','Fortech'],
['FA190','Fortech'],
['FA206','Fortech'],
['FA217','Fortech'],
['FA227','Fortech'],
['FA239','Fortech'],
['FA239','Fortech'],
['FA240','Fortech'],
['FA245','Fortech'],
['FA271','Fortech'],
['FS001C','Fortech'],
['FS004','Fortech'],
['FS013','Fortech'],
['FS014','Fortech'],
['FS016C','Fortech'],
['FS017C','Fortech'],
['FS022','Fortech'],
['FS028','Fortech'],
['FS035','Fortech'],
['FS040','Fortech'],
['FS088C','Fortech'],
['FS130C','Fortech'],
['FS130C','Fortech'],
['FS145','Fortech'],
['FS148','Fortech'],
['FS151C','Fortech'],
['FS157','Fortech'],
['FCR210134','Francecar'],
['FCR210138','Francecar'],
['FCR210140','Francecar'],
['FCR210960','Francecar'],
['253142405','G-Energy'],
['253142406','G-Energy'],
['GP504','G-Power'],
['B1G10206082','GALFER'],
['24445723','GENERAL MOTORS'],
['93165557','GENERAL MOTORS'],
['95017768','GENERAL MOTORS'],
['95599919','GENERAL MOTORS'],
['H8036000','GLASER'],
['5521','Gates'],
['5539','Gates'],
['6PK1735','Gates'],
['K015521XS','Gates'],
['T41101A','Gates'],
['T42041A','Gates'],
['T42042A','Gates'],
['713930STD','Glyco'],
['AG390CF','Goodwill'],
['AG493','Goodwill'],
['AG535','Goodwill'],
['110323','GraSS'],
['110372','GraSS'],
['110384','GraSS'],
['110393','GraSS'],
['116100','GraSS'],
['118100','GraSS'],
['700001','GraSS'],
['800001','GraSS'],
['800440','GraSS'],
['AC0165','GraSS'],
['AC0167','GraSS'],
['IT0321','GraSS'],
['IT0326','GraSS'],
['IF0161','Green Filter'],
['IF0336K','Green Filter'],
['KF0133','Green Filter'],
['LF0413','Green Filter'],
['OK0169','Green Filter'],
['SA160','HOLA'],
['SA160','HOLA'],
['0822899974','HONDA'],
['15400PLMA01','HONDA'],
['15400RTA003','HONDA'],
['1011002','HYUNDAI XTeer'],
['1011018','HYUNDAI XTeer'],
['1011126','HYUNDAI XTeer'],
['E1451L','Hengst'],
['P999G12','Hepu'],
['P999G12005','Hepu'],
['P999GRN','Hepu'],
['HG3216','Hi-Gear'],
['HG3416','Hi-Gear'],
['HG3421','Hi-Gear'],
['HG3436','Hi-Gear'],
['HG5688','Hi-Gear'],
['HG6096','Hi-Gear'],
['0310000130','Hyundai-KIA'],
['0450000115','Hyundai-KIA'],
['0510000110','Hyundai-KIA'],
['0510000141','Hyundai-KIA'],
['0510000441','Hyundai-KIA'],
['0520000120','Hyundai-KIA'],
['0520000620','Hyundai-KIA'],
['0520000620','Hyundai-KIA'],
['1885510060','Hyundai-KIA'],
['1885510060','Hyundai-KIA'],
['214212B030','Hyundai-KIA'],
['2630035505','Hyundai-KIA'],
['263202F100','Hyundai-KIA'],
['273012B010','Hyundai-KIA'],
['281132S000','Hyundai-KIA'],
['281133S100','Hyundai-KIA'],
['28113F2000','Hyundai-KIA'],
['28113M4000','Hyundai-KIA'],
['289622B310','Hyundai-KIA'],
['31112F9000','Hyundai-KIA'],
['31920S1900','Hyundai-KIA'],
['5810125A10','Hyundai-KIA'],
['581014LA00','Hyundai-KIA'],
['583050UA00','Hyundai-KIA'],
['866114L500','Hyundai-KIA'],
['866114L500','Hyundai-KIA'],
['868412T100','Hyundai-KIA'],
['868422T100','Hyundai-KIA'],
['971332W000','Hyundai-KIA'],
['97133D1000','Hyundai-KIA'],
['97133G8000','Hyundai-KIA'],
['9769034310','Hyundai-KIA'],
['977623X000','Hyundai-KIA'],
['S281131R100','Hyundai-KIA'],
['1845004','IDEMITSU'],
['1849001','IDEMITSU'],
['1849004','IDEMITSU'],
['2156001','IDEMITSU'],
['2156004','IDEMITSU'],
['30011328746','IDEMITSU'],
['30015048724','IDEMITSU'],
['30015048746','IDEMITSU'],
['30301201746','IDEMITSU'],
['530017110','Ina'],
['1121400500','JP Group'],
['A0002','JS Asakashi'],
['FA459S','Japanparts'],
['FA524S','Japanparts'],
['FO316S','Japanparts'],
['FOECO051','Japanparts'],
['FOECO060','Japanparts'],
['FOW01S','Japanparts'],
['JDA0019','Just Drive'],
['JDA0114','Just Drive'],
['JDA0165','Just Drive'],
['JDA886V','Just Drive'],
['JDACX046C','Just Drive'],
['JDACX058','Just Drive'],
['JDACX066','Just Drive'],
['JDAX034','Just Drive'],
['JDAX044','Just Drive'],
['JFM0009','Just Drive'],
['320409','KANGAROO'],
['320423','KANGAROO'],
['355104','KANGAROO'],
['L1970C04E1','KIXX'],
['L2061P20E1','KIXX'],
['L209044TE1','KIXX'],
['L209144TE1','KIXX'],
['L2091AL1E1','KIXX'],
['L2091AL1E1','KIXX'],
['L215444TE1','KIXX'],
['L215444TE1','KIXX'],
['L250944TE1','KIXX'],
['L251844TE1','KIXX'],
['L251944TE1','KIXX'],
['L251944TE1','KIXX'],
['L2519AL1E1','KIXX'],
['L271744TE1','KIXX'],
['L2717AL1E1','KIXX'],
['L531044TE1','KIXX'],
['L531644TE1','KIXX'],
['KHS657','KORMAX'],
['KA0117','KORTEX'],
['KA0142','KORTEX'],
['KA0269','KORTEX'],
['KC0016S','KORTEX'],
['KC0041','KORTEX'],
['KC0102','KORTEX'],
['KR9411','Kerry'],
['KR9411','Kerry'],
['KR969','Kerry'],
['KS00031','Korson'],
['KS00031','Korson'],
['KS00041','Korson'],
['KS00042','Korson'],
['KS00082','Korson'],
['62022RSCM','Koyo'],
['77554610','Ks'],
['21110812202082','LADA'],
['LN1495','LAVR'],
['LN1495','LAVR'],
['LN2106','LAVR'],
['1455401','LEMFORDER'],
['3361901','LEMFORDER'],
['3831401','LEMFORDER'],
['A1109141','LIFAN'],
['B8121170','LIFAN'],
['19191','LUKOIL'],
['19192','LUKOIL'],
['19531','LUKOIL'],
['19540','LUKOIL'],
['3148675','LUKOIL'],
['C9305','LYNXauto'],
['C9305','LYNXauto'],
['C9306','LYNXauto'],
['C9306','LYNXauto'],
['C9447','LYNXauto'],
['CO3601A','LYNXauto'],
['L10460','LYNXauto'],
['L10755','LYNXauto'],
['L10755B','LYNXauto'],
['L12251','LYNXauto'],
['L12805','LYNXauto'],
['L18127','LYNXauto'],
['LAC1006C','LYNXauto'],
['LC1902','LYNXauto'],
['LC1925','LYNXauto'],
['LC1926','LYNXauto'],
['LC216','LYNXauto'],
['LO1901','LYNXauto'],
['LX430','LYNXauto'],
['LX650','LYNXauto'],
['ME1049','LYNXauto'],
['PR7140','LYNXauto'],
['LN1005','Lavr'],
['LN1309','Lavr'],
['LN1436','Lavr'],
['LN1436','Lavr'],
['LN1750','Lavr'],
['LN1750','Lavr'],
['LN2511','Lavr'],
['3919','Liqui moly'],
['LCC6122HU','LivCar'],
['LFOE241','Lucas'],
['K7069','M-Filter'],
['501579','M-Standard'],
['502095','M-Standard'],
['153071762333','MAGNETI MARELLI'],
['CUK26017','MANN-FILTER'],
['HU9254Y','MANN-FILTER'],
['W68','MANN-FILTER'],
['W7008','MANN-FILTER'],
['W9142','MANN-FILTER'],
['W92021','MANN-FILTER'],
['9943','MANNOL'],
['9964','MANNOL'],
['9990','MANNOL'],
['9990','MANNOL'],
['9990','MANNOL'],
['9990','MANNOL'],
['MN81011','MANNOL'],
['M9811005','MARSHALL'],
['ML6936','MARSHALL'],
['ML7341','MARSHALL'],
['830077280','MAZDA'],
['B6Y1143029A','MAZDA'],
['A0001802609','MERCEDES-BENZ'],
['A000989760213BLER','MERCEDES-BENZ'],
['A0031846101','MERCEDES-BENZ'],
['A2820940004','MERCEDES-BENZ'],
['A6421800009','MERCEDES-BENZ'],
['A6511800109','MERCEDES-BENZ'],
['1000021','METACO'],
['1000105','METACO'],
['1020018','METACO'],
['1020043','METACO'],
['1020052','METACO'],
['1020115','METACO'],
['4024610','MITSUBISHI'],
['4056A049','MITSUBISHI'],
['MZ100139EX','MITSUBISHI'],
['MZ690115','MITSUBISHI'],
['MZ690116','MITSUBISHI'],
['MZ690150','MITSUBISHI'],
['04234BS','MOTIP'],
['OC1051A','Mahle/Knecht'],
['OC456','Mahle/Knecht'],
['OC467A','Mahle/Knecht'],
['OC90OF','Mahle/Knecht'],
['EEOK0003Y','Mando'],
['EEOK0003Y','Mando'],
['MOF0123','Mando'],
['MOF4459','Mando'],
['MOF4459','Mando'],
['MOF4476','Mando'],
['MC225CL','Masuma'],
['MC329','Masuma'],
['MC334','Masuma'],
['MD02030S','Masuma'],
['MFA1136','Masuma'],
['MFA1142','Masuma'],
['MFA595','Masuma'],
['MFA595','Masuma'],
['MFAH518','Masuma'],
['MFAM300','Masuma'],
['MFAM308','Masuma'],
['MFAT009','Masuma'],
['MFAT026','Masuma'],
['MFC2127','Masuma'],
['MU016U','Masuma'],
['MU018U','Masuma'],
['MU018U','Masuma'],
['MU024U','Masuma'],
['MU19G','Masuma'],
['MU24G','Masuma'],
['NSD049U','Masuma'],
['RU498','Masuma'],
['RU552','Masuma'],
['011889','Metelli'],
['030904','Metelli'],
['29143230001','Meyle'],
['O1647','Micro'],
['AFAD150','Miles'],
['AFAD328','Miles'],
['AFAI143','Miles'],
['AFAU019','Miles'],
['AFAU089','Miles'],
['AFAU112','Miles'],
['AFC1253','Miles'],
['AFC1353','Miles'],
['AFFS024','Miles'],
['AFOE081','Miles'],
['AFW1014','Miles'],
['AFW1090','Miles'],
['AFW1149','Miles'],
['AFW1173','Miles'],
['AFW1206','Miles'],
['AFW1212','Miles'],
['AFW1225','Miles'],
['AFW1295','Miles'],
['AFW2293','Miles'],
['153553','Mobil'],
['156154','Mobil'],
['156154','Mobil'],
['FA625NY','NAKAYAMA'],
['G33055','NAKAYAMA'],
['13361','NAVIGATOR'],
['13362','NAVIGATOR'],
['209815000100','NE'],
['NF1020P','NEVSKY FILTER'],
['5282','NGK'],
['ILKR7B8','NGK'],
['V0009','NGN'],
['V172085302','NGN'],
['V172085304','NGN'],
['V172085305','NGN'],
['V172085601','NGN'],
['V182575104','NGN'],
['V182575105','NGN'],
['1520865F0A','NISSAN'],
['56260VC300','NISSAN'],
['A52089F60ARV','NISSAN'],
['KE90090042','NISSAN'],
['AN1065','NORDFIL'],
['CN1035','NORDFIL'],
['CN1035','NORDFIL'],
['CN1035K','NORDFIL'],
['CN10892','NORDFIL'],
['GA35275','NTN-SNR'],
['R14100','NTN-SNR'],
['R15570','NTN-SNR'],
['8711490765','NURAL'],
['7701','Nac'],
['7708','Nac'],
['7708','Nac'],
['77107','Nac'],
['77135','Nac'],
['77141','Nac'],
['77143','Nac'],
['77148','Nac'],
['77152','Nac'],
['7720','Nac'],
['77254','Nac'],
['77303ST','Nac'],
['77318ST','Nac'],
['77318ST','Nac'],
['7733','Nac'],
['77347ST','Nac'],
['77389ST','Nac'],
['7755','Nac'],
['7775','Nac'],
['7799ST','Nac'],
['8801','Nac'],
['8836','Nac'],
['8855','Nac'],
['8858','Nac'],
['8862','Nac'],
['8866','Nac'],
['NFE1032','Narichin'],
['NFE2174','Narichin'],
['NFH2038','Narichin'],
['NFK1115','Narichin'],
['NFK1122','Narichin'],
['NFK1122','Narichin'],
['NFM1039','Narichin'],
['NFM1039','Narichin'],
['NFM1065','Narichin'],
['NFM1065','Narichin'],
['NFM2013','Narichin'],
['NFT1135','Narichin'],
['NFT1144','Narichin'],
['NFT1183','Narichin'],
['NFZ1052','Narichin'],
['NFZ1091','Narichin'],
['NFZ2032','Narichin'],
['PN1530S','NiBK'],
['J1345006','Nipparts'],
['N1310906','Nipparts'],
['2719754','Nk'],
['9036113','Nk'],
['209815000100','Npr'],
['2595','OILRIGHT'],
['5509','OILRIGHT'],
['GSPH233','ONNURI'],
['FS05','Olymp'],
['64150','Osram'],
['P370291','PATRON'],
['PF1337','PATRON'],
['PF1405','PATRON'],
['PF2534','PATRON'],
['PF3151','PATRON'],
['PF4171','PATRON'],
['PH2581','PATRON'],
['PM03305','PEMCO'],
['PM03505','PEMCO'],
['FAP2413','PILENGA'],
['FDP7870','PILENGA'],
['FOP6315','PILENGA'],
['SHP2772O','PILENGA'],
['SHP7266','PILENGA'],
['SHP7267','PILENGA'],
['3352','PILOTS'],
['850101','PINGO'],
['5105','PLAK'],
['C491','PURFLUX'],
['PAA082','Parts-Mall'],
['1109CL','Peugeot-Citroen'],
['2428','Polmostrow'],
['00267','Poxipol'],
['QF36A00351','QUATTRO FRENI'],
['QZ1745121060','Quartz'],
['152095084R','RENAULT'],
['165469466R','RENAULT'],
['440603905R','RENAULT'],
['440607493R','RENAULT'],
['7700274177','RENAULT'],
['7701208174','RENAULT'],
['7711943761','RENAULT'],
['8200142677','RENAULT'],
['8201627433','RENAULT'],
['RX0001TPN','RIXX'],
['RX0002ATX','RIXX'],
['RX0002TPN','RIXX'],
['RX0012TPX','RIXX'],
['322229','ROLF'],
['322232','ROLF'],
['322232','ROLF'],
['322233','ROLF'],
['RWK60076','ROLLTEC'],
['430101H02','ROSDOT'],
['430101H03','ROSDOT'],
['430110011','ROSDOT'],
['20058004099','ROWE'],
['20058005099','ROWE'],
['20109005099','ROWE'],
['20109005099','ROWE'],
['20118004099','ROWE'],
['20118005099','ROWE'],
['20125001099','ROWE'],
['20125004099','ROWE'],
['20138005099','ROWE'],
['20163001099','ROWE'],
['20245001099','ROWE'],
['20245004099','ROWE'],
['20245005099','ROWE'],
['20246001099','ROWE'],
['20246004099','ROWE'],
['20246005099','ROWE'],
['202591772A','ROWE'],
['202594532A','ROWE'],
['202595952A','ROWE'],
['203645952A','ROWE'],
['203665952A','ROWE'],
['203671772A','ROWE'],
['203674532A','ROWE'],
['203675952A','ROWE'],
['21014001503','ROWE'],
['21014001503','ROWE'],
['21014001503','ROWE'],
['RW6137','RUNWAY'],
['111112300401999','Ravenol'],
['1211108004','Ravenol'],
['4014835719316','Ravenol'],
['4014835722613','Ravenol'],
['4014835722613','Ravenol'],
['4014835722699','Ravenol'],
['40814342','Rosneft'],
['40815332','Rosneft'],
['SA1138','SCT'],
['SA1151','SCT'],
['SA1164','SCT'],
['SA1214','SCT'],
['SA1217','SCT'],
['SA1217','SCT'],
['SA1304','SCT'],
['SA1322','SCT'],
['SB2170','SCT'],
['SB2171','SCT'],
['SB2212','SCT'],
['SB2242','SCT'],
['SB2381','SCT'],
['SB2401','SCT'],
['SB2401','SCT'],
['SB295','SCT'],
['SB995','SCT'],
['SH401','SCT'],
['SH4053P','SCT'],
['SH4076P','SCT'],
['SH427P','SCT'],
['SH430P','SCT'],
['SH4784P','SCT'],
['SH4790P','SCT'],
['SH4799P','SCT'],
['SM101','SCT'],
['SM102','SCT'],
['SM105','SCT'],
['SM106','SCT'],
['SM108','SCT'],
['SM113','SCT'],
['SM125','SCT'],
['SM133','SCT'],
['SM134','SCT'],
['SM137','SCT'],
['SM137','SCT'],
['SM140','SCT'],
['SM148','SCT'],
['SM160','SCT'],
['SM166','SCT'],
['SM180','SCT'],
['ST330','SCT'],
['AC0232C','SIBTEK'],
['AC62','SIBTEK'],
['AF06141','SIBTEK'],
['AF2003','SIBTEK'],
['613500','SINTEC'],
['614500','SINTEC'],
['801941','SINTEC'],
['801942','SINTEC'],
['801943','SINTEC'],
['802558','SINTEC'],
['70250SKY','SKY PARTS'],
['75200LMSKY','SKY PARTS'],
['AMDFC167','SOLARIS'],
['VWA08900','STARTVOLT'],
['SP1005','SUFIX'],
['SR1001','SUFIX'],
['0200003000','SVS'],
['0200006000','SVS'],
['3000158001','Sachs'],
['A16870','Sakura'],
['A33440','Sakura'],
['SP1199','Sangsin brake'],
['SP1239','Sangsin brake'],
['SQC1810','Sapfire'],
['2250007','Sasic'],
['ST03L115562','Sat'],
['ST071115562','Sat'],
['ST1780128030','Sat'],
['ST1780174020','Sat'],
['ST2319009001','Sat'],
['ST28113C1100','Sat'],
['ST97133D3000','Sat'],
['STMBW5000B2TW','Sat'],
['800216','Sibiria'],
['800256','Sibiria'],
['800884','Sibiria'],
['802165','Sibiria'],
['VKD35038','Skf'],
['VKJA5379','Skf'],
['700616','Starex'],
['700617','Starex'],
['700618','Starex'],
['700619','Starex'],
['700620','Starex'],
['700620','Starex'],
['700621','Starex'],
['700621','Starex'],
['700623','Starex'],
['700624','Starex'],
['700654','Starex'],
['7101104SX','Stellox'],
['7551763SX','Stellox'],
['605043','TAKAYAMA'],
['605043','TAKAYAMA'],
['605045','TAKAYAMA'],
['DK105','TDK'],
['19601','TOTACHI'],
['19804','TOTACHI'],
['19901','TOTACHI'],
['20701','TOTACHI'],
['21001','TOTACHI'],
['21004','TOTACHI'],
['4562374690967','TOTACHI'],
['4562374690967','TOTACHI'],
['4562374691094','TOTACHI'],
['4562374691094','TOTACHI'],
['4589904524028','TOTACHI'],
['E0304','TOTACHI'],
['0415231090','TOYOTA'],
['0415237010','TOYOTA'],
['0415238020','TOYOTA'],
['04152YZZA1','TOYOTA'],
['04152YZZA3','TOYOTA'],
['0888013705','TOYOTA'],
['0888013705','TOYOTA'],
['0888013706','TOYOTA'],
['1780128030','TOYOTA'],
['1780131131','TOYOTA'],
['1780151020','TOYOTA'],
['2339051070','TOYOTA'],
['415238010','TOYOTA'],
['4552244020','TOYOTA'],
['8521253081','TOYOTA'],
['8522248130','TOYOTA'],
['8713958010','TOYOTA'],
['9091520004','TOYOTA'],
['90915YZZD4','TOYOTA'],
['90915YZZE1','TOYOTA'],
['90915YZZE1','TOYOTA'],
['60FGP','TRANSMASTER UNIVERSAL'],
['77FG','TRANSMASTER UNIVERSAL'],
['77FG','TRANSMASTER UNIVERSAL'],
['VB51K','TRANSMASTER UNIVERSAL'],
['GDB3580','TRW'],
['PFG110','TRW'],
['911421','TSN'],
['97110','TSN'],
['979','TSN'],
['20A075A52B','TYC'],
['20A076A52B','TYC'],
['P235','Teknorot'],
['P236','Teknorot'],
['U3781','Tokico'],
['LDK7RTCU','Torch'],
['430206217','Tosol-Sintez'],
['430210013','Tosol-Sintez'],
['6PK737','Trialli'],
['EMM0504','Trialli'],
['2311401','UFI'],
['2311401','UFI'],
['4602934','Unix'],
['4602934','Unix'],
['4605249','Unix'],
['4605904','Unix'],
['036129620J','VAG'],
['038103385A','VAG'],
['038103714G','VAG'],
['03C115561H','VAG'],
['03C115561H','VAG'],
['03C115562','VAG'],
['04E115561H','VAG'],
['04E115561H','VAG'],
['04E115561H','VAG'],
['059198405','VAG'],
['06A115561B','VAG'],
['06J115403Q','VAG'],
['06J115403Q','VAG'],
['06K905601B','VAG'],
['06L115562B','VAG'],
['1J0407181','VAG'],
['59198405','VAG'],
['6RU698151A','VAG'],
['6RU698525A','VAG'],
['7P0129620A','VAG'],
['7P6127177A','VAG'],
['GR52195M4','VAG'],
['N90467301','VAG'],
['N90998702','VAG'],
['N91009302','VAG'],
['VE55084','VAL racing'],
['703141410','VICTOR REINZ'],
['703141410','VICTOR REINZ'],
['712878110','VICTOR REINZ'],
['713753300','VICTOR REINZ'],
['FO1209R','VTR'],
['PRB33','Valeo phc'],
['750586','Valvoline'],
['866890','Valvoline'],
['866890','Valvoline'],
['872281','Valvoline'],
['872286','Valvoline'],
['872364','Valvoline'],
['872373','Valvoline'],
['872375','Valvoline'],
['872378','Valvoline'],
['872552','Valvoline'],
['872560','Valvoline'],
['872794','Valvoline'],
['881676','Valvoline'],
['885852','Valvoline'],
['887914','Valvoline'],
['VWSL004RU','Venwell'],
['VWSL004RU','Venwell'],
['VWSL004RU','Venwell'],
['VWSL006RU','Venwell'],
['VWSL011RU','Venwell'],
['VWSL016RU','Venwell'],
['WEKK028','WenderW'],
['132615','Zic'],
['132622','Zic'],
['132660','Zic'],
['132665','Zic'],
['162200','Zic'],
['162615','Zic'],
['162622','Zic'],
['162629','Zic'],
['162660','Zic'],
['162660','Zic'],
['162665','Zic'],
['162681','Zic'],
['172660','Zic'],
['ZN455C','Zollex'],
['CAZ1027','ZuvTeil'],
['3205','reinWell'],
['500659','topran'],
['40630','АвтоDело'],
['42120','АвтоDело'],
['44110','АвтоDело'],
['44111','АвтоDело'],
['00002','Автохимия'],
['00002','Автохимия'],
['00002','Автохимия'],
['311105K101','БАКОР'],
['6001547472РИ','БРТ'],
['РЕМКОМПЛЕКТ86РШ','БРТ'],
['1303','ВМПАВТО'],
['1906','ВМПАВТО'],
['1906','ВМПАВТО'],
['1910','ВМПАВТО'],
['1920','ВМПАВТО'],
['8610','ВМПАВТО'],
['215208','Дело Техники'],
['515613','Дело Техники'],
['KV253115A','КВАДРАТИС'],
['430206219','Полярник'],
['430206221','Полярник'],
['430206345','Полярник'],
['17888','ФОБОС'],
['000106','Хорс'],
['000106','Хорс'],
['000121','Хорс'],
['000122','Хорс'],
]

class AsyncCatalog_table(APIView):
    @method_decorator(swagger_auto_schema(
        operation_description="Get data asynchronously",
        responses={200: "OK - Data fetched asynchronously"},
    ))
    async def get(self, request, endpoint):
        # Асинхронная функция для отрисовки шаблона
        async def render_template():
            table_list = []
            args_req = request.GET
            context = await ABCP().get_dict(endpoint, **args_req)
            if isinstance(context, dict):
                for k, v in context.items():
                    if isinstance(v, dict):
                        v['name'] = k
                        table_list.append(v)
                if not table_list:
                    table_list.append(context)
            elif isinstance(context, list):
                table_list = context


            df = pd.DataFrame(table_list)
            # excel_filename = 'abcp_articles_info.xlsx'
            # path_excel_filename = os.getcwd() + '\\xlsx\\' + excel_filename
            # df = pd.read_excel(path_excel_filename)
            # df = df[['number', 'images', 'brand']]
            result_dict = df.to_dict(orient='records')
            return await sync_to_async(render)(request, 'dftable.html', context={'html_table':result_dict})
        # Получаем HTML-страницу из асинхронной функции
        response_html = await render_template()

        # Возвращаем HTTP-ответ
        return HttpResponse(response_html)


async def Pr_Lg_table(request, endpoint):
    args = request.GET
    context = await Pr_Lg().get_pd(endpoint, **args)
    return render(request, 'dftable.html', context)


async def Rossko_table(request, endpoint):
    args = request.GET
    context = await RosskoAPI(endpoint).get_pd(endpoint,**args)
    return render(request, 'dftable.html', context)

class AsyncCatalog(APIView):
    async def get(self, request):
        async def get_data(data,):
            dict_data = {'brand': data[1], 'number': data[0], 'format': ['bniphmt']}
            response = await ABCP().get_dict('articles_info', **dict_data)
            if 'images' in response:
                response['images'] = '\n\r'.join(
                    ['http://pubimg.4mycar.ru/images/' + v for k, v in response['images'] if k == 'name']) if response[
                    'images'] else ''
            if 'properties' in response:
                response['properties'] = '\n\r'.join([f'{k}:{v}' for k, v in response['properties'].items()])
            return response
        # Асинхронная функция для отрисовки шаблона
        async def render_template():
            args = request.GET
            data = [['55263'], ['3Ton']]
            html_table = {}
            table_list = []
            tasks = []
            for data in all_numbers:
                tasks.append(get_data(data))
                await asyncio.sleep(1)
            table_list = await asyncio.gather(*tasks)
            df = pd.DataFrame(table_list)
            excel_filename = 'abcp_articles_info.xlsx'
            path_excel_filename = os.getcwd()+'\\xlsx\\'+excel_filename
            df.to_excel(path_excel_filename, index=False)
            # df = pd.read_excel(path_excel_filename)
            # df = df[['number','images','brand']]
            result_dict = df.to_dict(orient='records')
            # df.to_excel(path_excel_filename, index=False)
            return await sync_to_async(render)(request, 'dftable.html', context={'html_table':result_dict})
        # Получаем HTML-страницу из асинхронной функции
        response_html = await render_template()

        # Возвращаем HTTP-ответ
        return HttpResponse(response_html)
