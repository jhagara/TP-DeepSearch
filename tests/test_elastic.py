# -*- coding: utf-8 -*-
import unittest
from elasticsearch import Elasticsearch
from semantic import Semantic
import config


class TestElastic(unittest.TestCase):
    #set corrent elastic index environment
    config.set_environment(config.default_elastic_index)

    def test_all(self):
        default_issue = {'number': 'Bratislava, v utorok 1. júla 1941',
                         'name': 'Slovak41452134894315486465216489319',
                         'page_width': 3455,
                         'page_height': 4871}

        default_result = [
[{'page': 1, 'b': '4743', 'l': '157', 'type': 'fulltext', 't': '894', 'text': 'V tejto krajine, disponujúcej nad naj¬väčším obilným bohatstvom, vyskytujeAk je ťažko udať jednotlivé číslice okmetskej brannej moci, tak to platí aj) duchu v sovietskej armáde. Ani tuia neslobodno oddávať falošným pred-itavám. Isté je, že dnes už väčšina dô-itojníkov patrí ku komunistickej strane.Vo vyšších služobných miestach sú te-Jner všetci velitelia a generáli členmi/strany. Zavedenie takzvaných politic¬kých komisárov podlieha mnohým zme¬nám. V základe majú úlohu výzvednýchdôstojníkov. Bolo by však nesprávnevidieť v nich nepohodlných konkuren¬tov pre ostatný dôstojnícky sbor. So¬vietski mocipáni vynasnažili sa vyvolať, v ľude čo najviac brannú vôľu. Založilirozsiahle inštitúcie na politické a brannévzdelávanie širokých más. Kládli dôrazaj na to, aby komunisti vstupujúci dostrany, odslúžili si vojenčinu v soviet¬skej armáde. Dnes je povinnosťou, žesaždý vyšší zamestnanec SSSR musí byťaj záložným dôstojníkom. Nakoľko sastrana v tejto Obrovskej krajine zako¬řenila, ukáže čas. Isté je, že sovietskimocipáni vehnali tisíce, ba milióny rus¬kého národa do strašnej biedy. Ťažkoveriť, že by sa na toto všetko zabudlo aže by vo vážnom prípade početné ná¬rody SSSR daly sa s oduševnením po¬strieľať za tých, čo ešte včera pomocouGPU používali proti masám najtvrdšie¬ho teroru. V každom prípade chýbajúsovietskym dôstojníkom vojenské skú¬senosti. Viac ráz síce vyhlasovali predverejnosťou, že skúsenosti z terajšiehoeurópskeho konfliktu použijú aj pri re¬organizácii sovietskej brannej  moci.1 boľševici ako dobrí letci, ale ich strojeuž vtedy nezodpovedaly technickým po¬žiadavkám. Medzitým přešly roky, vktorých Nemci zlepšili svoje lietadlá,čo sa predtým nepokladalo za možné.Za zvláštnu sovietsku špecialitu platiliparašutisti. Keď však sledujeme soviet¬ske noviny, zistíme, že sa aj tu ženu ibaza akýmsi rekordom. Nie je však naj¬dôležitejšie, aby parašutista skočil s nie-koľkotisíc-metrovej výšky, alebo aby vniektorej dedine prejavila posledná ba¬bička guráž k soskoku s lietadla. Vojen¬ské požiadavky sú celkom iné. To doká¬zaly práve boje na Kréte. Čo do flotily— SSSR má svoju námornú flotilu zasta¬ralú. Naproti tomu má väčší p*>čet po¬noriek, z ktorých väčšia časť je na Ďa-ekom východe.K strašidlu parného valca pripojuje sateraz zbožňovanie techniky. V SSSRforsírovali zo všetkých síl motorizáciu vkaždom smere. A predsa bolo v Moskvev mieri pred terajšou vojnou ťažko do¬stať taxi. Neslobodno síce zabudnúť, žev SSSR vybudovali nové závody na mo¬torizáciu, ale technika sama nemôže do¬siahnuť víťazstvo. K tomu sú potrebnéaj iné predpoklady. Vzdušná zbraň SSSRpokladá sa stále za čosi mimoriadneho,V španielskom ťažení dokázali  sa sícePodľa tradície a podľa celkového cha¬rakteru tohto štátu máta ešte i dnesstrašidlo »p a r neho valca«. Tentoparný valec Nemecko už raz zažilo a za¬držalo ho nielen pred Tannenbergom,ale neskoršie aj v bojoch mazúrskych.Prelom pri Gorlici uskutočnil sa napriekmocným ruským silám, ktoré stály opro¬ti nemeckým vojakom a keď pred 25rokmi Brusilov nešetril nijakých ľudí,ale masy svojich vojsk bezohľadne hnalproti nemecko-rakúskej obrane, dosia¬hol iba čiastočných úspechov, ale nikdyvíťazstva.                                              ;,=■O brannej moci SSSR vyskytujú samnohé cifry, ale cena týchto číslic je vovšeobecnosti veľmi problematická —možno ich ľahko preceniť, možno ichvšak ľahko aj podceniť. Aj číslice,ktoré samotný SSSR oznamuje, niesú chránené pred takýmito omylmi.Preto číslice o brannej moci sovietskejúnie nie sú natoľko dôležité, ako vy¬jasnenie určitých základnýchotázok o brannej moci a bran¬nej  odolnosti SSSR.G. — Bratislava, 30. júna.', 'r': '912'}, {'page': 1, 'b': '876', 'l': '188', 'type': 'heading', 't': '766', 'text': 'Nie cifry - a!e duch', 'r': '906'}, {'page': 1, 'b': '4743', 'l': '957', 'type': 'fulltext', 't': '4268', 'text': 'sa ešte vždy na niektorých miestachhlad. Táto skutočnosť je vari najlepšímpríkladom o dosiaľ nezvládnutej desor-ganizácii. Neporiadky v SSSR prejavujúsa najviac v dopravní c tv e. Posta¬vili síce železnice, dôležité pre vojenskéciele. Spomíname pritom turkestansko-sibírsku železnicu alebo nové železnicev Bielom Rusku a na bývalom poľskomúzemí. Napriek tomu posudzujú objek¬tívni a informovaní znalci sovietoruskédopravné pomery pesimisticky. Netreba', 'r': '1696'}, {'page': 1, 'b': '4739', 'l': '1740', 'type': 'fulltext', 't': '4266', 'text': 'zabudnúť ani na to, že vzdialenosť vý¬chodnej hranice od západnej hraniceSSSR robí 15.000 km. Na hranici stojí,ako vodca Nemeckej ríše, Adolf Hitlervo svojej proklamácii povedal, 160 sovie-toruských divízií a vo svoj om rozkaze vo¬jakom na východnom fronte poukázalÄdolf Hitler aj na to, že boj bude tvrdý,ťažký a plný zodpovednosti. Jedno jevšak isté: tento boj, či nepriateľ budestavať tuhší alebo slabší odpor, skončísa víťazstvom nemeckej moci.', 'r': '2483'}],
[{'page': 1, 'b': '4149', 'l': '957', 'type': 'fulltext', 't': '3697', 'text': 'STK. Viohy, 30. júna.Úradne 0znamu jií, že francúzska vláda pre¬rušila diplomatické styky so Sovietskym svä-Francúzsko  prerušilo  diploma¬tické styky so Sovietskym sväzom.Nemecké oddiely obsadily dnes ĽvOv. Na ci¬tadele veje od 4,20 hod. ríšska vojenská vlajka.Z vodcovského hlavného Manu oznamujehlavné veliteľstvo brannej moci:STK. Berlín, 30. júna.', 'r': '1696'}, {'page': 1, 'b': '3655', 'l': '1403', 'type': 'heading', 't': '3581', 'text': 'Dnes padol Lvov', 'r': '2040'}, {'page': 1, 'b': '4185', 'l': '1716', 'type': 'fulltext', 't': '3695', 'text': 'V obvode Ľvova bolo sostrelených v leteckomI boj} 31 a na zemi zničených 14 lietadiel. VcelkuSTK. Berlín, 30. júma.Nemecké letectvo pokračovalo v uplynulejnoci úspešne v svojlich útokoch na letištia navýchodnom fronte. Bombami boly zasiahnutéletecké hal, pripravené lietadlá a ubikáde. Vobvode prii Minsku boly iv leteckom boji so-strclené 4 nepriateľské lietadlá a 73 lietadielj zničených, alebo  poškodených na zemi.Neipr e (t ržit é   útolky  nemeckéholetectva na východe,', 'r': '2482'}],
[{'page': 1, 'b': '2179', 'l': '979', 'type': 'fulltext', 't': '1510', 'text': 'My Slováci, ktorí sme do tohto boja proti boľševizmu nastúpili medzi prvými, môžemebyť pyšní, že aj slovenská armáda bojuje nielen statočne, ale aj s najväčšou odvahou a hrdinsko-sťou. Svedčia o tom zprávy, ktoré vydáva naše Tlačové veliteľstvo armády a práve tak aj uzna¬nie, ktoré sa nám dostáva od vysokých nemeckých dôstojníkov.Sú to všetko výsledky, aké dejiny ešte nezaznamenaly a prekonávajú nielen všetko, čo sadoteraz dosiahlo, ale aj všetko, čo si v tom ohľade bolo úložné doteraz predstaviť. Včera a dnescelý svet obdivuje nemecké úspechy.Nemci za tento čas obsadili a dobyli G r o d n o, Brest-Litovsk, Vilno,K o v n o, Dvinsk a ako oznamujú dnes,    po t v r d om boji padol im do rúk ajPozemné úspechy sú tiež skvelé.Nemci zničili 4107 lietadiel, 2233 pancierov, 600 kanónov a padlo Imdo rúk vyše 40.000 sovietskych zajatcov.Včerajší deň znamená v dejinách vojny nemecko-sovietskej významný medzník, lebo tohodna hlavné veliteľstvo nemeckej brannej moci, ktoré od začiatku operácii na východe obmedzo¬valo sa len na krátke konštatovanie o úspechoch nemeckej armády, rozhodlo sa oznámiť verej¬nosti nemeckej i verejnosti celého sveta doteraj "ie nemecké úspechy. Tieto úspechy boly takéobrovské, aké nikto neočakával. Ako sme už v „Slováku-pondelníku" oznámili, Nemci v mimo¬riadnych zprávách, ktoré vydávali včera, v nedeľu, podali výsledok svojich akcií, ktorý v čísll-ciach vyzerá takto:(ý) Bratislava, 30. júna.', 'r': '2451'}, {'page': 1, 'b': '1476', 'l': '1050', 'type': 'heading', 't': '768', 'text': 'Francúzsko prerušilo diplomatické styky so SSSRUkrajina sa oslobodzujeDnes padol Lvov — Nových 22.000 brt. na dne morskomSkvelá bilancia nemeckej brannej moci za prvý týždeň operáciiVíťazný postup slovenského vojska', 'r': '3127'}, {'page': 1, 'b': '3376', 'l': '2516', 'type': 'fulltext', 't': '1514', 'text': "Ozvena vo sveteVo východnej Afrike na úseku Dembldollo(Galia a Sidamo) zahnali sme okamžitým proti¬útokom na útek nepriateľské vojsko, pokúšajúcesa napadnúť naše pozície.Britské lietadlá previedly nálet na Bengazi apokusily sa viac ráz napadnú prístav v Tripo-Iise, boly však vždy sostrelené našimi rýchlo za-siahnuvšími stíhačkami.V severnej Afrike naše delostrelectvo ostreľo¬valo na tobruckom úseku sústreďovanie vojska azapríčinilo protivníkovi citeľné straty na muž¬stve a materiále.Hlavný stan talianskej brannej moci oznamu¬je:STK. Bim, 30. júna.Zpráva talianskej brannejSTK. Berlín, 30. júna.Ako sa dozvedá KM'., nemecká letecká zbraňzničila tejt0 noci početné britské lode v ná¬mornej oblasti okolo východného Anglicka. Asi100 kilometrov severne od Great-YarmOulhpoškodily bombami vojenskú dopravnú loď o10 až 12.000 brt., plaviacu sa v konvoji. S jejskazou možno rátať. V tej istej oblasti poiopilyobchodnú loď „ 10.000 brt. a ďalšiu obchodnúloď o í500 hrt. Konečne na lom istom miestepoškodily ťažko štvrtú obeh,,dmi loď o 4 až5000 brt.Opäf vyše 22.000 brt. na dne morskom.Formácie nemeckých strmhlav útočiacichlietadiel útočily znovu na sústreďovania nepria.teľského vojska a obranné pozície, zničily mno¬ho pancierov, viaceré pozície delostrelectva avykoľajily železničné vlaky.Nemecké letectvo znovu čo najfažšic bom¬bardovalo rýchlo ustupujúce nepriateľské koló¬ny a motorizované oddiely, zničilo prit0m že¬lezničné objekty a trailc a potopilo transportnúloď o 3 až 4000 tonách.bolo na celom východnom fronte v leteckýchbojoch ^střelených 48 červených lietadiel a114 bol0 zničených alebo poškodených na zemi.", 'r': '3263'}],
[{'page': 1, 'b': '515', 'l': '192', 'type': 'fulltext', 't': '215', 'text': 'Adresa redakcie a ad¬ministrácie: Bratislav*Trieda kráľa Alexandrač. 12. Telefon redakcie aadministrácie: 6820, 6821,6822, 2313, 3223, 2062.Veci týkajúce sa pred¬platného a inzerátov vy¬bavuje len admini¬strácia.', 'r': '550'}],
[{'page': 1, 'b': '3532', 'l': '958', 'type': 'fulltext', 't': '2459', 'text': '27. júna naša pechota, podporovanáútočnou vozbou, podnikla ofenzívu nanepriateľské línie a narazila na železo-V utorok 24. Júna prekročilo sloven¬ské vojsko slovenské štátne hranice apostupovalo k rieke Sam, ktorá tvoríhranicu medzi Nemeckom a SSSR. 26.júna rieku slovenské jednotky překro¬čily a hneď narazily na tuhý odpor boľ¬ševikov, ktorí ich privítali mohutnoudelostreleckou paľbou. Slovenskí vojacihneď v prvých bojoch ukázali, že s ni¬mi musí nepriateľ počítať a že budúsvojim nemeckým kamarátom dobrýmipomocníkmi. Pri začiatočných bojochzničily haše jednotky mnoho nepriateľ¬ských guľometných hniezd. Zaútočilanaša útočná vozba, ktorá spôsobilav nepriateľských radoch veľký zmätoka narobila veľa materiálnej škody aľudských strát nepriateľovi.tieto:boja proti boľševikom. Podrobnosti súzprávy o zásahu slovenskej armády doDo   našej   verejnosti   pronikly   prvéTVA — Bratislava, 30. júna', 'r': '1696'}, {'page': 1, 'b': '2386', 'l': '1104', 'type': 'heading', 't': '2225', 'text': 'Prielom slovenského vojskacez nepriateľské opevnené línie', 'r': '2321'}, {'page': 1, 'b': '3529', 'l': '1741', 'type': 'fulltext', 't': '2415', 'text': 'V prvých bojoch sa vyznamenalomnoho vojakov, lebo každý jednotli¬vec, či dôstojník, poddôstojník, alebovojak, bojuje s nadšením a odvahou.Vyslovili sa o tom nemeckí dôstojníci,ktorí mali možnosť boj sledovať a zdô¬razňujú, že toľko odvahy, statočnosti ahrdinstva ešte nevideli. Slovenská ar¬máda dokazuje svetu, že vie, za čo bo¬juje, že chce v tomto gigantickom bojispolu so všetkými vojnuvedúcimi ar-máďmi zvíťaziť a zničiť nepriateľa Euró¬py a ľudstva.betonové pevnosti (bunkery), ktoré bo¬ly "yvŕolené aj protitankovými kanón¬mi, ťažkými guľometmi a mínometmi.Nepriatelia sa húževnaté bránili, aleproti odvahe a statočnosti slovenskýchchlapcov jeho tvrdošijný odpor nesta¬čil. Slovenské jednotky dobyly 8 ne¬priateľských pevností a na širšom úse¬ku přelomily nepriateľský front. Pri tom¬to zásahu ukořistily vojenný materiál.Zajatí boľševici boli mongolskej rasy.Po prelomení nepriateľských línií sa slo¬venské vojsko nezastavilo v boji a vovíťaznom postupe pokračuje a rozširujeúspechy.', 'r': '2481'}],
[{'page': 1, 'b': '3487', 'l': '2528', 'type': 'heading', 't': '3423', 'text': 'Fiihrer - osloboditeľ Európy', 'r': '3266'}, {'page': 1, 'b': '4738', 'l': '2529', 'type': 'fulltext', 't': '3514', 'text': 'STK. Paríž, 30. júna.Mimoriadne zprávy hlavného veliteľstva bran¬nej moci o veľkých začiatočných úspechoch ne¬meckej brannej moci vzalo obyvateľstvo na ve¬domie už v nedeľu odpoludnia z mimoriadnychvydaní, jednako však časopisy, ktoré proti obvyk¬lému zvyku vyšly v pondelok ráno, malý veľkýodbyt. Časopis „Petit Parisien" podtrhuje v nad¬pisoch mimoriadne úspechy nemeckých zbraní navýchode a hovorí o bezpríkladných víťazstvách.Propagandisti Tretej Internacionály a plutokra-Francúzsko.Časopis „Vblkischer Beobachter" vyhlasuje,že zdržanlivosť vo zprávách nemeckej brannejmoci viedla k pravej záplave nepriateľskýchzpráv o údajnom stroskotaní nemeckých operácií.Avšak táto nemecká taktika mala svoj úspech užv tom, že v Moskve, ako vysvitalo zo sovietskychvojenských zpráv, si neboli na čistom, čo sa nasovietskom fronte v skutočnosti odohráva. Ne¬mecká ofenzíva vrazila s osvedčenou energiou dosovietskeho nástupu a nepriateľský plán poľnéhoťaženia radikálne zničila. Hneď na počiatku poľ¬ného ťaženia nemecké oddiely malý rozhodujúciúspech.Berlínska pondelňajšia tlač vyzdvihuje naúvodnom mieste pod veľkými nadpismi, ako na¬príklad „Európa zachránená", „Nástup soviet¬skych vojsk rozbitý", „Víťazné nemecké ťaženiena východe" včerajšie mimoriadne zprávy hlav¬ného veliteľstva nemeckej brannej moci. Časopi¬sy zdôrazňujú, že Je v pláne vojenného vedeniaponechávať nepriateľa dlho v neistote o svojichoperačných úmysloch.STK. Berlín, 30. júna.', 'r': '3266'}]
                ]

        journal_path = '/path/to/marc21'
        semantic = Semantic(
        xml=config.get_full_path('tests', 'slovak_1941_1_strana_1.xml'),
        header_config=config.get_full_path('tests', 'page_header_conf_1941_1.json'))

        semantic.save_to_elastic('Slovak41452134894315486465216489319', '/tests', journal_path)

        es = Elasticsearch()

        res = es.search(index=config.elastic_index(), doc_type="article",
                        body={"query": {"match": {'issue.name': 'Slovak41452134894315486465216489319'}}})
        counter = 0
        print("Got %d Hits:" % res['hits']['total'])
        for hit in res['hits']['hits']:
            self.assertEqual(hit["_source"]["issue"]["name"], default_issue["name"])
            self.assertEqual(hit["_source"]["issue"]["number"], default_issue["number"])
            self.assertEqual(hit["_source"]["issue"]["page_width"], default_issue["page_width"])
            self.assertEqual(hit["_source"]["issue"]["page_height"], default_issue["page_height"])
            # self.assertEqual(len(hit["_source"]["groups"]), len(default_result[counter])) # screw you dynamically created jsons and articles
            counter += 1

        res = es.search(index=config.elastic_index(), doc_type="issue",
                        body={"query": {"match": {'name': 'Slovak41452134894315486465216489319'}}})

        for hit in res['hits']['hits']:
            self.assertEqual(hit["_source"]["journal_marc21"], journal_path)
