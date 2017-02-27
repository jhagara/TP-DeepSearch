import unittest
import re
from lxml import etree
from parser.xml.discriminator.separatorsid import SeparatorId


class TestAssembler3Separators(unittest.TestCase):

    def test_assembler_all3_separators_success(self):

        original_xml="""<document xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0" producer="FineReader 8.0" pagesCount="10" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
<page width="3488" height="5003" resolution="400">
<block blockType="Text" l="186" t="124" r="584" b="188" type="text"><par l="203" t="136" r="567" b="184" type="heading">
<line baseline="184" l="203" t="136" r="567" b="184"><formatting lang="Czech" ff="Arial" fs="11.">Cena </formatting><formatting lang="Slovak" ff="Arial" fs="11.">80 </formatting><formatting lang="Czech" ff="Arial" fs="11.">hal.</formatting></line></par>
</block>
<block blockType="Text" l="184" t="236" r="588" b="550"><par align="Justified" lineSpacing="30" l="199" t="242" r="570" b="546" type="fulltext">
<line baseline="269" l="201" t="242" r="568" b="269"><formatting lang="Czech" ff="Times New Roman" fs="6.">Adres? </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">redakcie </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">a </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">ad.</formatting></line>
<line baseline="297" l="201" t="275" r="567" b="299"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ministracie: </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Bratislava.</formatting></line>
<line baseline="330" l="200" t="305" r="570" b="335"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ulica </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Ro&#271;obrany &#269;&#237;elo</formatting></line>
<line baseline="361" l="200" t="337" r="570" b="362"><formatting lang="Slovak" ff="Times New Roman" fs="6.">12, </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Telefon </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">redakcie </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">a</formatting></line>
<line baseline="391" l="200" t="368" r="567" b="396"><formatting lang="Slovak" ff="Times New Roman" fs="6.">administr&#225;cie: 6820, 6821,</formatting></line>
<line baseline="422" l="199" t="399" r="567" b="427"><formatting lang="Slovak" ff="Times New Roman" fs="6.">6822, 2313, 3223, 2062.</formatting></line>
<line baseline="453" l="200" t="430" r="565" b="459"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Veci t&#253;kaj&#250;ce sa pred&#172;</formatting></line>
<line baseline="484" l="200" t="460" r="565" b="490"><formatting lang="Slovak" ff="Times New Roman" fs="6.">platn&#233;ho a inzer&#225;tov vy&#172;</formatting></line>
<line baseline="514" l="200" t="490" r="565" b="518"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bavuje ten admini&#172;</formatting></line>
<line baseline="545" l="306" t="523" r="451" b="546"><formatting lang="Slovak" ff="Times New Roman" fs="6." spacing="15">str&#225;cia.</formatting></line></par>
</block>
<block blockType="Text" l="212" t="628" r="984" b="688" type="text"><par l="228" t="637" r="969" b="683" type="heading">
<line baseline="673" l="228" t="637" r="969" b="683"><formatting lang="Slovak" ff="Arial" fs="9." spacing="-2">Bratislava, v sobotu 20. j&#250;na 1942</formatting></line></par>
</block>
<block blockType="Picture" l="632" t="80" r="2892" b="628"/>
<block blockType="Text" l="1284" t="628" r="2128" b="688" type="text"><par l="1300" t="638" r="2124" b="684" type="heading">
<line baseline="674" l="1300" t="638" r="2124" b="684"><formatting lang="Slovak" ff="Arial" fs="9.">Zaklad&#225;f&#233;&#318; a vodca t Andrej Hlinka</formatting></line></par>
</block>
<block blockType="Text" l="2920" t="122" r="3312" b="186" type="text"><par l="2935" t="134" r="3295" b="181" type="heading">
<line baseline="181" l="2935" t="134" r="3295" b="181"><formatting lang="Slovak" ff="Arial" fs="11." spacing="-3">Ro&#269;n&#237;k </formatting><formatting lang="EnglishUnitedStates" ff="Arial" fs="11." spacing="-3">XXIV.</formatting></line></par>
</block>
<block blockType="Text" l="2916" t="236" r="3314" b="560"><par align="Justified" lineSpacing="32" l="2933" t="242" r="3298" b="555" type="fulltext">
<line baseline="266" l="2935" t="242" r="3296" b="271"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Predplatn&#233;: </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">y </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">Bratisl&#225;v*</formatting></line>
<line baseline="298" l="2934" t="273" r="3297" b="298"><formatting lang="Slovak" ff="Times New Roman" fs="6.">s don&#225;&#353;kou do domu 14</formatting></line>
<line baseline="330" l="2935" t="306" r="3297" b="335"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ks, postoa 20 Ks. Slo&#172;</formatting></line>
<line baseline="361" l="2936" t="337" r="3297" b="362"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vensko a Protektor&#225;t me&#172;</formatting></line>
<line baseline="393" l="2935" t="369" r="3297" b="398"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sa&#269;ne 20 Ks, &#353;tvxtro&#269;n*</formatting></line>
<line baseline="425" l="2933" t="401" r="3298" b="430"><formatting lang="Slovak" ff="Times New Roman" fs="6.">60 Ks, polro&#269;ne 120 Ks,</formatting></line>
<line baseline="458" l="2933" t="433" r="3297" b="458"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ro&#269;ne 240 Ks. Pre Fran&#172;</formatting></line>
<line baseline="489" l="2933" t="465" r="3298" b="491"><formatting lang="Slovak" ff="Times New Roman" fs="6.">c&#250;zsko, Nemecko a Ma&#172;</formatting></line>
<line baseline="522" l="2933" t="498" r="3298" b="523"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#271;arsko ro&#269;ne 300 Ks. In&#225;</formatting></line>
<line baseline="554" l="2933" t="529" r="3297" b="555"><formatting lang="Slovak" ff="Times New Roman" fs="6.">cudzina   rodne   433   K*.</formatting></line></par>
</block>
<block blockType="Text" l="3072" t="634" r="3290" b="684"><par l="3087" t="642" r="3274" b="679" type="fulltext">
<line baseline="678" l="3087" t="642" r="3274" b="679"><formatting lang="Slovak" ff="Arial" fs="8." spacing="-1">&#268;&#237;slo 138</formatting></line></par>
</block>
<block blockType="Text" l="176" t="766" r="972" b="4902" type="text"><par leftIndent="41" l="233" t="784" r="891" b="880" type="heading">
<line baseline="859" l="233" t="784" r="891" b="880"><formatting lang="Slovak" ff="Arial" fs="16.">Vojna a z&#225;sobovanie</formatting></line></par>
<par leftIndent="276" lineSpacing="39" l="468" t="888" r="967" b="943" type="fulltext">
<line baseline="930" l="468" t="888" r="967" b="943"><formatting lang="Slovak" ff="Times New Roman" fs="6.">(R. T.) Bratislava,   19. j&#250;na  |</formatting></line></par>
<par align="Justified" leftIndent="3" startIndent="61" lineSpacing="39" l="195" t="939" r="967" b="1808" type="fulltext">
<line baseline="972" l="259" t="939" r="966" b="981"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ka&#382;d&#225; vojna v dejin&#225;ch vy&#382;iadala si '</formatting></line>
<line baseline="1011" l="198" t="978" r="966" b="1026"><formatting lang="Slovak" ff="Times New Roman" fs="6.">obete a &#250;stupky aj od civiln&#233;ho obyvate&#318;- j</formatting></line>
<line baseline="1051" l="199" t="1011" r="967" b="1066"><formatting lang="Slovak" ff="Times New Roman" fs="6.">stva bojuj&#250;ceho &#353;t&#225;tu. Tieto sa </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">stup&#328;ovaly </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">J</formatting></line>
<line baseline="1090" l="198" t="1057" r="967" b="1100"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v pomere, ako sa vojna predl&#382;ovala. My |</formatting></line>
<line baseline="1129" l="198" t="1097" r="938" b="1132"><formatting lang="Slovak" ff="Times New Roman" fs="6.">dnes v &#353;tvrtom roku samostatn&#233;ho sloven&#172;</formatting></line>
<line baseline="1168" l="199" t="1135" r="940" b="1177"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sk&#233;ho &#353;t&#225;tu stoj&#237;me vlastne v &#353;tvrtom roku</formatting></line>
<line baseline="1207" l="196" t="1176" r="936" b="1218"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vojny a a&#382; dosia&#318; pochva&#318;ujeme si, &#382;e jej</formatting></line>
<line baseline="1246" l="197" t="1214" r="940" b="1257"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#225;sledky nedo&#318;ahly na n&#225;s tak tiesnivo, ako</formatting></line>
<line baseline="1286" l="198" t="1254" r="938" b="1293"><formatting lang="Slovak" ff="Times New Roman" fs="6.">azda inde. Ba ch&#253;r o na&#353;ich dobr&#253;ch ho&#172;</formatting></line>
<line baseline="1325" l="197" t="1293" r="940" b="1335"><formatting lang="Slovak" ff="Times New Roman" fs="6.">spod&#225;rskych pomeroch dostal sa a&#382; za hra&#172;</formatting></line>
<line baseline="1365" l="198" t="1334" r="941" b="1373"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nice, neh&#318;adiac na to, &#382;e &#269;asom </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">ud&#345;ely </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">tieto</formatting></line>
<line baseline="1404" l="195" t="1369" r="940" b="1414"><formatting lang="Slovak" ff="Times New Roman" fs="6.">priazniv&#233; a usporiadan&#233; pomery aj do o&#269;&#250;</formatting></line>
<line baseline="1443" l="199" t="1412" r="941" b="1447"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sam&#233;ho n&#225;&#353;ho ob&#269;ianstva, ktor&#233; nevedelo</formatting></line>
<line baseline="1482" l="197" t="1451" r="940" b="1492"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sa </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zprvu </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">v&#382;i&#357; do vojnovej situ&#225;cie, reptalo</formatting></line>
<line baseline="1522" l="198" t="1486" r="941" b="1531"><formatting lang="Slovak" ff="Times New Roman" fs="6.">a neuzn&#225;valo nijak&#250; vis major, do&#382;aduj&#250;c</formatting></line>
<line baseline="1561" l="197" t="1530" r="938" b="1570"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sa bez oh&#318;adu aj v z&#225;sobovan&#237; podmienok,</formatting></line>
<line baseline="1601" l="197" t="1570" r="940" b="1610"><formatting lang="Slovak" ff="Times New Roman" fs="6.">na ak&#233; bolo zvyknut&#233; v pokoji. T&#237;to oby&#172;</formatting></line>
<line baseline="1641" l="195" t="1610" r="940" b="1648"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vatelia &#353;t&#225;tu kone&#269;ne pochopili prav&#253; stav</formatting></line>
<line baseline="1680" l="197" t="1649" r="939" b="1689"><formatting lang="Slovak" ff="Times New Roman" fs="6.">a venovali svoju d&#244;veru zodpovedn&#253;m &#353;t&#225;t&#172;</formatting></line>
<line baseline="1719" l="195" t="1690" r="940" b="1729"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nym &#269;inite&#318;om. Preto dnes m&#244;&#382;eme s uspo&#172;</formatting></line>
<line baseline="1759" l="195" t="1728" r="940" b="1768"><formatting lang="Slovak" ff="Times New Roman" fs="6.">kojen&#237;m kon&#353;tatova&#357; u n&#225;s konsolid&#225;ciu</formatting></line>
<line baseline="1799" l="197" t="1770" r="618" b="1808"><formatting lang="Slovak" ff="Times New Roman" fs="6.">hospod&#225;rskych pomerov.</formatting></line></par>
<par align="Justified" leftIndent="2" rightIndent="25" startIndent="57" lineSpacing="39" l="194" t="1807" r="942" b="2512" type="fulltext">
<line baseline="1838" l="255" t="1807" r="938" b="1845"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#268;omu za to &#271;akova&#357;? </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Nepochybn&#233; </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">pre&#172;</formatting></line>
<line baseline="1877" l="198" t="1849" r="939" b="1885"><formatting lang="Slovak" ff="Times New Roman" fs="6.">dov&#353;etk&#253;m tomu, &#382;e sme sa v prav&#253; &#269;as</formatting></line>
<line baseline="1917" l="195" t="1886" r="940" b="1925"><formatting lang="Slovak" ff="Times New Roman" fs="6.">neb&#225;li pozrie&#357; tvrdej skuto&#269;nosti rovno do</formatting></line>
<line baseline="1956" l="197" t="1926" r="941" b="1963"><formatting lang="Slovak" ff="Times New Roman" fs="6.">o&#269;&#250;. Nesna&#382;ili sme sa uk&#225;ja&#357; sa m&#225;rnymi</formatting></line>
<line baseline="1995" l="195" t="1965" r="938" b="2004"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#225;dejami na nejak&#253; n&#225;hly vojensk&#253; obrat,</formatting></line>
<line baseline="2035" l="199" t="2004" r="941" b="2042"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ale s rozvahou, rozumne sme sa </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">vystrojili</formatting></line>
<line baseline="2074" l="199" t="2043" r="939" b="2083"><formatting lang="Slovak" ff="Times New Roman" fs="6.">a pripravili na cel&#253; priebeh vojny. Obyva&#172;</formatting></line>
<line baseline="2114" l="196" t="2085" r="938" b="2122"><formatting lang="Slovak" ff="Times New Roman" fs="6.">te&#318;stvu odkryli sme v prav&#253; &#269;as prav&#253; stav,</formatting></line>
<line baseline="2154" l="199" t="2119" r="939" b="2162"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Wci prv&#233; oper&#225;cie </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">boly </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">trocha bolestn&#233;.</formatting></line>
<line baseline="2193" l="197" t="2162" r="941" b="2201"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Pam&#228;tajme sa na prvotn&#253; z&#225;sah do distrib&#250;&#172;</formatting></line>
<line baseline="2233" l="195" t="2201" r="939" b="2242"><formatting lang="Slovak" ff="Times New Roman" fs="6.">cie m&#250;ky, cukru, m&#228;sa a in&#253;ch ka&#382;doden&#172;</formatting></line>
<line baseline="2272" l="194" t="2242" r="939" b="2281"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#253;ch potrav&#237;n. &#268;o sa vtedy vyskytlo re&#269;&#237;,</formatting></line>
<line baseline="2312" l="195" t="2281" r="941" b="2320"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nespokojnosti a ned&#244;very! Ale vl&#225;da vtedy</formatting></line>
<line baseline="2351" l="195" t="2321" r="941" b="2359"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bez oh&#318;adu na tak&#233;to psychologick&#233; sprie&#172;</formatting></line>
<line baseline="2390" l="195" t="2359" r="942" b="2398"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vodn&#233; zjavy s energiou zapla do pr&#225;ce cel&#253;</formatting></line>
<line baseline="2429" l="197" t="2399" r="942" b="2437"><formatting lang="Slovak" ff="Times New Roman" fs="6.">hospod&#225;rsky organiza&#269;n&#253; apar&#225;t a vyko&#172;</formatting></line>
<line baseline="2467" l="196" t="2437" r="940" b="2474"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nala radik&#225;lne z&#225;sahy do n&#225;&#353;ho hospod&#225;r&#172;</formatting></line>
<line baseline="2504" l="195" t="2475" r="774" b="2512"><formatting lang="Slovak" ff="Times New Roman" fs="6.">stva, distrib&#250;cie, ba aj v&#253;roby.   .</formatting></line></par>
<par align="Justified" leftIndent="2" rightIndent="21" startIndent="65" lineSpacing="39" l="194" t="2511" r="946" b="2710" type="fulltext">
<line baseline="2543" l="259" t="2511" r="946" b="2551"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#193;no, predov&#353;etk&#253;m tomu m&#244;&#382;eme by&#357;</formatting></line>
<line baseline="2581" l="194" t="2550" r="942" b="2589"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pov&#271;a&#269;n&#237;, &#382;e urobil sa poriadok od sam&#233;ho</formatting></line>
<line baseline="2621" l="196" t="2590" r="941" b="2629"><formatting lang="Slovak" ff="Times New Roman" fs="6.">za&#237;&#269;iatku. A&#382; potom pristupuj&#250; tu &#271;al&#353;&#237; f ak-</formatting></line>
<line baseline="2660" l="195" t="2629" r="941" b="2669"><formatting lang="Slovak" ff="Times New Roman" fs="6.">tori, ako je na&#353;a dobr&#225; zem, starostliv&#253;</formatting></line>
<line baseline="2699" l="194" t="2668" r="845" b="2710"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ro&#318;n&#237;k, pracovit&#253; robotn&#237;k a &#250;radn&#237;k.</formatting></line></par>
<par align="Justified" rightIndent="26" startIndent="60" lineSpacing="39" l="192" t="2715" r="941" b="3307" type="fulltext">
<line baseline="2745" l="253" t="2715" r="941" b="2753"><formatting lang="Slovak" ff="Times New Roman" fs="6.">O tento poriadok ide aj teraiz. </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Vojnov&#283;</formatting></line>
<line baseline="2784" l="193" t="2754" r="941" b="2793"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pomery n&#250;tia n&#225;s azda viac ako predt&#253;m</formatting></line>
<line baseline="2824" l="193" t="2794" r="939" b="2832"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pop&#250;&#353;&#357;af zo svojich n&#225;rokov. Bolo by ne&#172;</formatting></line>
<line baseline="2864" l="194" t="2834" r="939" b="2872"><formatting lang="Slovak" ff="Times New Roman" fs="6.">rozumn&#233; nebra&#357; ako hotov&#250; vec, &#382;e postup&#172;</formatting></line>
<line baseline="2904" l="193" t="2874" r="940" b="2907"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ne nedost&#225;va sa n&#225;m azda na trhu a v ob&#172;</formatting></line>
<line baseline="2944" l="194" t="2913" r="941" b="2951"><formatting lang="Slovak" ff="Times New Roman" fs="6.">chodoch to, alebo to&#318;ko, &#269;o a v akej miere</formatting></line>
<line baseline="2983" l="193" t="2952" r="940" b="2991"><formatting lang="Slovak" ff="Times New Roman" fs="6.">by sme chceli ma&#357;. Bolo by to nerozumn&#233;</formatting></line>
<line baseline="3023" l="193" t="2992" r="940" b="3031"><formatting lang="Slovak" ff="Times New Roman" fs="6.">najm&#228; preto, lebo vieme, &#382;e ani keby sme</formatting></line>
<line baseline="3063" l="193" t="3032" r="940" b="3070"><formatting lang="Slovak" ff="Times New Roman" fs="6.">veci brali najpesimistickej&#353;ie, nehrozia n&#225;m</formatting></line>
<line baseline="3102" l="194" t="3071" r="939" b="3110"><formatting lang="Slovak" ff="Times New Roman" fs="6.">tak&#233; pomery, ktor&#233; by sme s ist&#253;m seba&#172;</formatting></line>
<line baseline="3142" l="194" t="3112" r="940" b="3149"><formatting lang="Slovak" ff="Times New Roman" fs="6.">zapren&#237;m predsa pomerne &#318;ahko nemohli</formatting></line>
<line baseline="3181" l="192" t="3150" r="938" b="3189"><formatting lang="Slovak" ff="Times New Roman" fs="6.">prekona&#357;. Je tu teda len probl&#233;m a &#250;loha,</formatting></line>
<line baseline="3221" l="193" t="3190" r="940" b="3229"><formatting lang="Slovak" ff="Times New Roman" fs="6.">rozde&#318;ova&#357; &#382;ivotn&#233; potreby tak, aby sa</formatting></line>
<line baseline="3261" l="193" t="3226" r="938" b="3269"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ka&#382;d&#233;mu u&#353;lo spravodliv&#233;. To je poriadok,</formatting></line>
<line baseline="3300" l="194" t="3268" r="731" b="3307"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ktor&#253; si vy&#382;aduje dne&#353;n&#253; stav.</formatting></line></par>
<par align="Justified" leftIndent="1" rightIndent="26" startIndent="59" lineSpacing="39" l="193" t="3309" r="941" b="3784" type="fulltext">
<line baseline="3340" l="252" t="3309" r="939" b="3348"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Pre vykonanie tejto &#250;lohy odhlasoval v</formatting></line>
<line baseline="3379" l="193" t="3348" r="940" b="3388"><formatting lang="Slovak" ff="Times New Roman" fs="6.">uplynul&#253;ch d&#328;och Snem Najvy&#353;&#353;&#237; &#250;rad pre</formatting></line>
<line baseline="3419" l="194" t="3388" r="939" b="3427"><formatting lang="Slovak" ff="Times New Roman" fs="6.">z&#225;sobovanie, ktor&#253; u&#382; aj za&#269;al fungova&#357;.</formatting></line>
<line baseline="3459" l="196" t="3427" r="940" b="3467"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Je to in&#353;tit&#250;cia, ktor&#250; si nielen &#382;e vynucuj&#250;</formatting></line>
<line baseline="3498" l="193" t="3467" r="939" b="3507"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pomery, ale zriadenie ktorej d&#225;va nov&#253; d&#244;&#172;</formatting></line>
<line baseline="3538" l="193" t="3507" r="940" b="3545"><formatting lang="Slovak" ff="Times New Roman" fs="6.">kaz o na&#353;ej organiz&#225;cii a usporiadanosti</formatting></line>
<line baseline="3577" l="194" t="3547" r="941" b="3584"><formatting lang="Slovak" ff="Times New Roman" fs="6.">na&#353;ich pomerov v z&#225;sobovan&#237;. S&#225;m Vodca</formatting></line>
<line baseline="3617" l="194" t="3586" r="940" b="3624"><formatting lang="Slovak" ff="Times New Roman" fs="6.">a prezident Dr. Jozef Tiso vystihol jeho</formatting></line>
<line baseline="3657" l="193" t="3625" r="938" b="3664"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#250;lohu vo v&#253;zve na obyvate&#318;stvo Republiky,</formatting></line>
<line baseline="3697" l="193" t="3665" r="941" b="3704"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ke&#271; povedal, &#382;e m&#225; vyl&#250;&#269;i&#357;, pokia&#318; mo&#382;no</formatting></line>
<line baseline="3736" l="193" t="3706" r="939" b="3744"><formatting lang="Slovak" ff="Times New Roman" fs="6.">najviac, rozli&#269;n&#233; poruchy v z&#225;sobovan&#237;</formatting></line>
<line baseline="3776" l="194" t="3744" r="695" b="3784"><formatting lang="Slovak" ff="Times New Roman" fs="6.">brannej moci a obyvate&#318;stva.</formatting></line></par>
<par align="Justified" leftIndent="1" rightIndent="27" startIndent="60" lineSpacing="39" l="193" t="3783" r="940" b="4498" type="fulltext">
<line baseline="3816" l="253" t="3783" r="939" b="3823"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#218;loha tohto &#250;radu je teda v&#253;znamn&#225;</formatting></line>
<line baseline="3855" l="193" t="3824" r="938" b="3863"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nielen pre z&#225;zemie, ale menovite pre front.</formatting></line>
<line baseline="3895" l="195" t="3863" r="939" b="3903"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Discipl&#237;na, a len discipl&#237;na v &#353;t&#225;te, presn&#233;</formatting></line>
<line baseline="3934" l="196" t="3903" r="939" b="3942"><formatting lang="Slovak" ff="Times New Roman" fs="6.">dodr&#382;iavanie nariaden&#237; Najvy&#353;&#353;ieho &#250;radu</formatting></line>
<line baseline="3974" l="193" t="3943" r="940" b="3982"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pre z&#225;sobovanie s&#250; z&#225;kladnou po&#382;iadavkou</formatting></line>
<line baseline="4014" l="196" t="3983" r="939" b="4021"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#271;al&#353;ieho &#250;spe&#353;n&#233;ho boja na&#353;ich vojakov na</formatting></line>
<line baseline="4054" l="196" t="4023" r="939" b="4062"><formatting lang="Slovak" ff="Times New Roman" fs="6.">fronte, lebo len tak, ke&#271; sa uplatnia z&#225;sady</formatting></line>
<line baseline="4094" l="195" t="4062" r="938" b="4101"><formatting lang="Slovak" ff="Times New Roman" fs="6.">star&#233;ho vojensk&#233;ho riaden&#233;ho hospod&#225;rstva,</formatting></line>
<line baseline="4133" l="195" t="4102" r="939" b="4142"><formatting lang="Slovak" ff="Times New Roman" fs="6.">budeme m&#244;c&#357; zabezpe&#269;i&#357; chlieb a potraviny</formatting></line>
<line baseline="4173" l="194" t="4143" r="939" b="4180"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pre z&#225;zemie a menovite pre front. Tu me&#172;</formatting></line>
<line baseline="4212" l="194" t="4182" r="939" b="4219"><formatting lang="Slovak" ff="Times New Roman" fs="6.">novite platia &#271;al&#353;ie slov&#225; Vodcove: &#8222;Mier</formatting></line>
<line baseline="4252" l="195" t="4221" r="939" b="4260"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ob&#269;anov nez&#225;vis&#237; len od obilia, ale predo&#172;</formatting></line>
<line baseline="4291" l="194" t="4260" r="939" b="4299"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v&#353;etk&#253;m od spravodlivej de&#318;by toho, &#269;o</formatting></line>
<line baseline="4331" l="194" t="4299" r="939" b="4339"><formatting lang="Slovak" ff="Times New Roman" fs="6.">m&#225;me." Preto na dodr&#382;iavanie poriadku m&#225;</formatting></line>
<line baseline="4371" l="198" t="4339" r="939" b="4376"><formatting lang="Slovak" ff="Times New Roman" fs="6.">dba&#357; ka&#382;d&#253; ob&#269;an &#353;t&#225;tu. Preto sa tie&#382; k dis&#172;</formatting></line>
<line baseline="4411" l="194" t="4379" r="940" b="4418"><formatting lang="Slovak" ff="Times New Roman" fs="6.">poz&#237;cii Najvy&#353;&#353;ieho &#250;radu pre z&#225;sobovanie</formatting></line>
<line baseline="4451" l="198" t="4419" r="938" b="4452"><formatting lang="Slovak" ff="Times New Roman" fs="6.">dali z Nemecka sa </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">vr&#225;tiv&#353;&#237; </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">vodcovsk&#237; &#269;aka&#172;</formatting></line>
<line baseline="4489" l="195" t="4458" r="789" b="4498"><formatting lang="Slovak" ff="Times New Roman" fs="6.">telia Slovenskej pracovnej slu&#382;by.</formatting></line></par>
<par align="Justified" leftIndent="3" rightIndent="28" startIndent="59" lineSpacing="39" l="195" t="4498" r="939" b="4897" type="fulltext">
<line baseline="4529" l="254" t="4498" r="939" b="4538"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Zd&#244;raznili sme u&#382;, &#382;e na&#353;e hospod&#225;rske</formatting></line>
<line baseline="4570" l="195" t="4538" r="938" b="4578"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pomery v z&#225;sobovan&#237; s&#250; podstatne priazni&#172;</formatting></line>
<line baseline="4609" l="197" t="4579" r="938" b="4617"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vej&#353;ie, ne&#382; v mnoh&#253;ch cudz&#237;ch krajin&#225;ch.</formatting></line>
<line baseline="4648" l="197" t="4618" r="939" b="4657"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Napriek tomu v&#353;ak mus&#237; by&#357; snahou Naj&#172;</formatting></line>
<line baseline="4688" l="196" t="4657" r="939" b="4696"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vy&#353;&#353;ieho &#250;radu pre z&#225;sobovanie, aby vo ve&#172;</formatting></line>
<line baseline="4728" l="198" t="4697" r="938" b="4737"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ciach organiz&#225;cie z&#225;sobovania postupne pri&#172;</formatting></line>
<line baseline="4767" l="197" t="4736" r="936" b="4776"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bl&#237;&#382;il sa k dobr&#253;m cudz&#237;m vzorom, aby aj</formatting></line>
<line baseline="4807" l="197" t="4777" r="939" b="4816"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v z&#225;sobovan&#237;, v tomto po&#269;as vojny najd&#244;le&#172;</formatting></line>
<line baseline="4848" l="199" t="4817" r="939" b="4856"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#382;itej&#353;om odvetv&#237; verejn&#233;ho hospod&#225;rstva</formatting></line>
<line baseline="4888" l="197" t="4856" r="785" b="4897"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Mplaita&#237;l sa princfp&#237; spraTOdl&#237;vosti.</formatting></line></par>
</block>
<block blockType="Text" l="980" t="790" r="3320" b="1274" type="text"><par leftIndent="7" lineSpacing="260" l="996" t="832" r="3292" b="1068" type="heading">
<line baseline="1028" l="996" t="832" r="3292" b="1068"><formatting lang="Slovak" ff="Arial" fs="42.">Churchill znova vo </formatting><formatting lang="Czech" ff="Arial" fs="42.">Washingtone</formatting></line></par>
<par leftIndent="1" lineSpacing="96" l="989" t="1099" r="3303" b="1270" type="heading">
<line baseline="1160" l="989" t="1099" r="3296" b="1175"><formatting lang="Slovak" ff="Times New Roman" fs="14." spacing="-5">Posledn&#253; z&#250;fal&#253; krok Churchillov &#8212; No&#269;n&#225; porada v Bielom dome &#8212; Kruh</formatting></line>
<line baseline="1256" l="990" t="1184" r="3303" b="1270"><formatting lang="Slovak" ff="Times New Roman" fs="14.">okolo Sevastopolu a Tobruku st&#225;le u&#382;&#353;&#237; &#8212; &#270;al&#353;ie &#250;spechy v sever. Afrike</formatting></line></par>
</block>
<block blockType="Text" l="978" t="1312" r="1740" b="2222"><par leftIndent="321" lineSpacing="39" l="1306" t="1318" r="1729" b="1354" type="fulltext">
<line baseline="1345" l="1306" t="1318" r="1729" b="1354"><formatting lang="Slovak" ff="Times New Roman" fs="6.">EP. Washington,  19. j&#250;na.</formatting></line></par>
<par align="Justified" leftIndent="1" startIndent="35" lineSpacing="39" l="986" t="1357" r="1730" b="1863" type="fulltext">
<line baseline="1385" l="1022" t="1357" r="1729" b="1392"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Anglick&#253; ministersk&#253; predseda pod&#318;a &#250;rad&#172;</formatting></line>
<line baseline="1424" l="987" t="1397" r="1730" b="1431"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#233;ho ozn&#225;menia Bieleho domu pri&#353;iel op&#228;&#357; na</formatting></line>
<line baseline="1463" l="987" t="1435" r="1730" b="1471"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#225;v&#353;tevu do Spojen&#253;ch &#353;t&#225;tov. V jeho sprie&#172;</formatting></line>
<line baseline="1503" l="987" t="1475" r="1729" b="1509"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vode je &#353;&#233;f gener&#225;lneho &#353;t&#225;bu britsk&#233;ho Im&#172;</formatting></line>
<line baseline="1542" l="986" t="1514" r="1730" b="1548"><formatting lang="Slovak" ff="Times New Roman" fs="6.">p&#233;ria, </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Sir Allan </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">Brooke a tajomn&#237;k &#353;t&#225;bneho</formatting></line>
<line baseline="1582" l="988" t="1553" r="1730" b="1589"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#353;&#233;fa britsk&#253;ch arm&#225;dnych &#269;ast&#237;, gener&#225;l-major</formatting></line>
<line baseline="1621" l="988" t="1592" r="1728" b="1628"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ismay. &#218;&#269;elom tejto druhej n&#225;v&#353;tevy Churchil-</formatting></line>
<line baseline="1660" l="987" t="1632" r="1730" b="1666"><formatting lang="Slovak" ff="Times New Roman" fs="6.">lovej v USA od vypuknutia vojny s&#250;, ako to</formatting></line>
<line baseline="1699" l="987" t="1672" r="1728" b="1706"><formatting lang="Slovak" ff="Times New Roman" fs="6.">uv&#225;dza &#250;radn&#233; ozn&#225;menie, &#8222;Porady s </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Roose&#172;</formatting></line>
<line baseline="1739" l="986" t="1711" r="1729" b="1745"><formatting lang="Czech" ff="Times New Roman" fs="6.">veltem </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">o pokra&#269;ovan&#237; vo vojne". V Bielom do&#172;</formatting></line>
<line baseline="1778" l="986" t="1750" r="1728" b="1785"><formatting lang="Slovak" ff="Times New Roman" fs="6.">me e&#353;te po polnoci zadr&#382;ali nov&#250; konferenciu.</formatting></line>
<line baseline="1817" l="987" t="1790" r="1730" b="1824"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Doteraz v&#353;ak e&#353;te neozin&#225;mili, &#269;i sa Churchill</formatting></line>
<line baseline="1856" l="988" t="1829" r="1491" b="1863"><formatting lang="Slovak" ff="Times New Roman" fs="6.">tejto konferencie tie&#382; z&#250;&#269;astnil.</formatting></line></par>
<par align="Justified" startIndent="36" lineSpacing="39" l="985" t="1868" r="1730" b="2218" type="fulltext">
<line baseline="1896" l="1021" t="1868" r="1730" b="1902"><formatting lang="Slovak" ff="Times New Roman" fs="6.">V tla&#269;ov&#253;ch kruhoch americk&#233;ho hlavn&#233;ho</formatting></line>
<line baseline="1935" l="985" t="1908" r="1730" b="1942"><formatting lang="Slovak" ff="Times New Roman" fs="6.">mesta vyvolala t&#225;to nov&#225; n&#225;v&#353;teva Churchilla</formatting></line>
<line baseline="1975" l="987" t="1947" r="1728" b="1981"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ve&#318;k&#253; rozruch. Rooseveltov tajomn&#237;k, Early,</formatting></line>
<line baseline="2014" l="986" t="1986" r="1730" b="2021"><formatting lang="Slovak" ff="Times New Roman" fs="6.">prijal tla&#269;ov&#253;ch z&#225;stupcov, ktor&#237; sa objavili v</formatting></line>
<line baseline="2053" l="987" t="2025" r="1730" b="2060"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Bielom dome vo ve&#318;mi neobvyklej hodine a</formatting></line>
<line baseline="2092" l="990" t="2065" r="1730" b="2099"><formatting lang="Czech" ff="Times New Roman" fs="6.">sd&#283;lit </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">im, &#382;e v&#353;etky podrobnosti Churchillo-</formatting></line>
<line baseline="2132" l="987" t="2104" r="1730" b="2139"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vej n&#225;v&#353;tevy bud&#250; dr&#382;a&#357; v tajnosti. Ani od</formatting></line>
<line baseline="2171" l="989" t="2144" r="1729" b="2180"><formatting lang="Czech" ff="Times New Roman" fs="6.">Roosevelta, </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">ani od Churchilla nemo&#382;no vraj</formatting></line>
<line baseline="2211" l="988" t="2183" r="1728" b="2218"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v tomto t&#253;&#382;dni o&#269;ak&#225;va&#357; ak&#253;chko&#318;vek vyhl&#225;&#172;</formatting></line></par>
</block>
<block blockType="Text" l="1766" t="1314" r="2526" b="2214"><par align="Justified" leftIndent="1" rightIndent="2" lineSpacing="40" l="1776" t="1321" r="2515" b="1470" type="fulltext">
<line baseline="1348" l="1777" t="1321" r="2514" b="1355"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sen&#237; o svojich porad&#225;ch. Odpove&#271; na ot&#225;zky,</formatting></line>
<line baseline="1388" l="1778" t="1360" r="2515" b="1394"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#269;i prekvapuj&#250;ca n&#225;v&#353;teva Churchillova stoj&#237;</formatting></line>
<line baseline="1427" l="1776" t="1399" r="2515" b="1433"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v s&#250;vislosti s n&#225;v&#353;tevou Molotovovou, Early</formatting></line>
<line baseline="1466" l="1778" t="1438" r="1917" b="1470"><formatting lang="Slovak" ff="Times New Roman" fs="6.">odmietol,</formatting></line></par>
<par align="Justified" startIndent="320" lineSpacing="40" l="1775" t="1478" r="2517" b="2173" type="fulltext">
<line baseline="1505" l="2132" t="1478" r="2514" b="1512"><formatting lang="Slovak" ff="Times New Roman" fs="6.">EP. &#352;tokholm, 19. j&#250;na.</formatting></line>
<line baseline="1544" l="1812" t="1517" r="2516" b="1551"><formatting lang="Slovak" ff="Times New Roman" fs="6.">O nov&#353;ej ceste Churchilla do </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtonu</formatting></line>
<line baseline="1584" l="1777" t="1557" r="2516" b="1591"><formatting lang="Czech" ff="Times New Roman" fs="6.">nedo&#353;ly </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">e&#353;te &#353;v&#233;dskej tla&#269;i ob&#353;&#237;rnej&#353;ie komen&#172;</formatting></line>
<line baseline="1623" l="1779" t="1596" r="2516" b="1630"><formatting lang="Slovak" ff="Times New Roman" fs="6.">t&#225;re z Lond&#253;na, av&#353;ak z nieko&#318;ko do&#353;l&#253;ch</formatting></line>
<line baseline="1663" l="1777" t="1636" r="2515" b="1669"><formatting lang="Czech" ff="Times New Roman" fs="6.">zpr&#225;v </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">d&#225; sa vyvodzova&#357; predsa ur&#269;it&#233; z&#225;ve&#172;</formatting></line>
<line baseline="1702" l="1777" t="1675" r="2515" b="1710"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ry. D&#244;vod n&#225;hlej cesty anglick&#233;ho minister&#172;</formatting></line>
<line baseline="1741" l="1777" t="1714" r="2515" b="1748"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sk&#233;ho predsedu do USA spo&#269;&#237;vaj&#250; asi v ne&#172;</formatting></line>
<line baseline="1781" l="1776" t="1753" r="2516" b="1788"><formatting lang="Slovak" ff="Times New Roman" fs="6.">priaznivom v&#253;voji vojensk&#233;ho polo&#382;enia v </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Li&#172;</formatting></line>
<line baseline="1820" l="1776" t="1793" r="2517" b="1828"><formatting lang="Czech" ff="Times New Roman" fs="6.">byi </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">a v nebezpe&#269;&#237;, ktor&#233; sa za nimi rysuje a</formatting></line>
<line baseline="1863" l="1776" t="1836" r="2515" b="1871"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ktor&#233; ohrozuje cel&#233; anglo-americk&#233; postave&#172;</formatting></line>
<line baseline="1908" l="1776" t="1881" r="2516" b="1915"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nie na &#270;alekom v&#253;chode. &#381;e t&#225;to cesta m&#225;</formatting></line>
<line baseline="1950" l="1778" t="1923" r="2516" b="1958"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sl&#250;&#382;i&#357; hlavne vojensk&#253;m porad&#225;m a pl&#225;nom,</formatting></line>
<line baseline="1994" l="1775" t="1965" r="2515" b="2002"><formatting lang="Slovak" ff="Times New Roman" fs="6.">na to poukazuj&#250; u&#382; aj Churchillovi sprievodci,</formatting></line>
<line baseline="2036" l="1776" t="2007" r="2515" b="2044"><formatting lang="Czech" ff="Times New Roman" fs="6.">Sir Allan </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">Brooke a gener&#225;l-major Ismay, z kto&#172;</formatting></line>
<line baseline="2081" l="1777" t="2054" r="2516" b="2090"><formatting lang="Slovak" ff="Times New Roman" fs="6.">r&#253;ch posledn&#253; s Churchillom &#269;o naju&#382;&#353;ie spo&#172;</formatting></line>
<line baseline="2123" l="1777" t="2094" r="2516" b="2133"><formatting lang="Slovak" ff="Times New Roman" fs="6.">lupracuje a pre mnoh&#233; z jeho &#8222;strategick&#253;ch</formatting></line>
<line baseline="2164" l="1777" t="2133" r="2516" b="2173"><formatting lang="Slovak" ff="Times New Roman" fs="6.">rozhodnut&#237;" pova&#382;uj&#250; ho za jedine zodpoved-</formatting></line></par>
</block>
<block blockType="Text" l="2554" t="1314" r="3322" b="2214"><par align="Justified" startIndent="35" lineSpacing="42" l="2564" t="1322" r="3304" b="1788" type="fulltext">
<line baseline="1350" l="2599" t="1322" r="3300" b="1357"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#268;o sa t&#253;ka bezprostredn&#253;ch vn&#250;tropolitic&#172;</formatting></line>
<line baseline="1392" l="2564" t="1364" r="3301" b="1400"><formatting lang="Slovak" ff="Times New Roman" fs="6.">k&#253;ch &#250;&#269;inkov tejto novej Churchillovej cesty,</formatting></line>
<line baseline="1435" l="2564" t="1408" r="3302" b="1442"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pod&#318;a n&#225;znakov, poch&#225;dzaj&#250;cich z Lond&#253;na,</formatting></line>
<line baseline="1478" l="2565" t="1451" r="3302" b="1485"><formatting lang="Slovak" ff="Times New Roman" fs="6.">d&#225; sa vyvodzova&#357;, &#382;e udalos&#357;ami v L&#237;byi vy&#172;</formatting></line>
<line baseline="1521" l="2566" t="1494" r="3304" b="1528"><formatting lang="Slovak" ff="Times New Roman" fs="6.">volan&#225; siln&#225; vlna kritick&#253;ch hlasov proti</formatting></line>
<line baseline="1564" l="2567" t="1537" r="3303" b="1571"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#8222;strat&#233;govi a </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zpravodajsk&#233;mu </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">politikovi Chur-</formatting></line>
<line baseline="1607" l="2566" t="1580" r="3302" b="1614"><formatting lang="Slovak" ff="Times New Roman" fs="6.">chillo'i' aspo&#328; v tomto okam&#382;iku je uml&#269;an&#225;.</formatting></line>
<line baseline="1650" l="2567" t="1622" r="3304" b="1658"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Dokonca je vraj aj to mo&#382;n&#233;, &#382;e t&#225;to kritika</formatting></line>
<line baseline="1693" l="2566" t="1665" r="3304" b="1701"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bude &#250;pine udusen&#225;, ke&#271; Churchillova cesta</formatting></line>
<line baseline="1736" l="2567" t="1709" r="3303" b="1742"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bude mat za n&#225;sledok ak&#233;ko&#318;vek pozit&#237;vne</formatting></line>
<line baseline="1779" l="2565" t="1752" r="3231" b="1788"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v&#253;sledky o zriaden&#237;  &#8222;druh&#233;ho frontu"(l),</formatting></line></par>
<par leftIndent="178" l="2742" t="1814" r="3122" b="1846" type="fulltext">
<line baseline="1841" l="2742" t="1814" r="3122" b="1846"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Churchill u </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Roosevelta,</formatting></line></par>
<par align="Justified" startIndent="266" lineSpacing="43" l="2564" t="1869" r="3304" b="2210" type="fulltext">
<line baseline="1896" l="2864" t="1869" r="3302" b="1905"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. Amsterdam, 19. j&#250;na.</formatting></line>
<line baseline="1939" l="2598" t="1911" r="3302" b="1946"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ako hl&#225;si britsk&#225; </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zpravodajsk&#225; </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">slu&#382;ba oso&#172;</formatting></line>
<line baseline="1982" l="2566" t="1954" r="3302" b="1991"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bitnou zpi&#225;vou, v Lond&#253;ne &#250;radne ozn&#225;mili,</formatting></line>
<line baseline="2026" l="2565" t="1999" r="3303" b="2034"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#382;e Churchill pri&#353;iel do Spojen&#253;ch &#353;t&#225;tov seve&#172;</formatting></line>
<line baseline="2069" l="2569" t="2041" r="3304" b="2077"><formatting lang="Slovak" ff="Times New Roman" fs="6.">roamerick&#253;ch. Churchilla. sprev&#225;dzaj&#250; </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">sir</formatting></line>
<line baseline="2112" l="2564" t="2083" r="3304" b="2122"><formatting lang="Czech" ff="Times New Roman" fs="6.">Alan </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">Brooke, &#353;&#233;f gener&#225;lneho &#353;t&#225;bu Imp&#233;ria</formatting></line>
<line baseline="2155" l="2566" t="2125" r="3304" b="2165"><formatting lang="Slovak" ff="Times New Roman" fs="6.">a gener&#225;.-major Ismay, sekret&#225;r &#353;&#233;fa &#353;t&#225;bneho</formatting></line>
<line baseline="2202" l="2564" t="2175" r="2681" b="2210"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v&#253;boru.</formatting></line></par>
</block>
<block blockType="Text" l="1046" t="2242" r="3244" b="2366" type="text"><par lineSpacing="104" l="1060" t="2258" r="3228" b="2362" type="heading">
<line baseline="2353" l="1060" t="2258" r="3228" b="2362"><formatting lang="Czech" ff="Times New Roman" fs="21.">Roosevelt </formatting><formatting lang="Slovak" ff="Times New Roman" fs="21.">a Churchill si bud&#250; l&#225;ma&#357; hlavy</formatting></line></par>
</block>
<block blockType="Text" l="978" t="2396" r="1742" b="3398"><par leftIndent="308" lineSpacing="39" l="1295" t="2403" r="1731" b="2436" type="fulltext">
<line baseline="2429" l="1295" t="2403" r="1731" b="2436"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. Amsterdam, 19. j&#250;la.</formatting></line></par>
<par align="Justified" leftIndent="1" startIndent="36" lineSpacing="39" l="988" t="2441" r="1733" b="2666" type="fulltext">
<line baseline="2468" l="1024" t="2441" r="1731" b="2475"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Britsk&#225; </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zpravodajsk&#225; </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">slu&#382;ba hl&#225;si z </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Was&#172;</formatting></line>
<line baseline="2508" l="988" t="2480" r="1733" b="2514"><formatting lang="Czech" ff="Times New Roman" fs="6.">hingtonu, </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#382;e Biely dom ozn&#225;mil, &#382;e Churchill</formatting></line>
<line baseline="2545" l="988" t="2519" r="1730" b="2553"><formatting lang="Slovak" ff="Times New Roman" fs="6.">je op&#228;&#357; v Spojen&#253;ch &#353;t&#225;toch, aby s Roosevel-</formatting></line>
<line baseline="2584" l="991" t="2557" r="1732" b="2592"><formatting lang="Slovak" ff="Times New Roman" fs="6.">tom hne&#271; nadviazal rozhovory </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">o </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">tom, ako</formatting></line>
<line baseline="2624" l="989" t="2596" r="1730" b="2631"><formatting lang="Slovak" ff="Times New Roman" fs="6.">treba viest vojnu &#271;alej a ako ju mo&#382;no &#8222;vy&#172;</formatting></line>
<line baseline="2662" l="988" t="2635" r="1079" b="2666"><formatting lang="Slovak" ff="Times New Roman" fs="6.">hra&#357;".</formatting></line></par>
<par leftIndent="312" lineSpacing="39" l="1299" t="2674" r="1730" b="2707" type="fulltext">
<line baseline="2700" l="1299" t="2674" r="1730" b="2707"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. Amsterdam, 19. j&#250;na.</formatting></line></par>
<par align="Justified" rightIndent="2" startIndent="35" lineSpacing="39" l="987" t="2712" r="1731" b="2823" type="fulltext">
<line baseline="2740" l="1022" t="2712" r="1731" b="2747"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Podl&#225; </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zpr&#225;vy </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">britskej zpravodajskej slu&#382;by</formatting></line>
<line baseline="2780" l="987" t="2752" r="1730" b="2787"><formatting lang="Slovak" ff="Times New Roman" fs="6.">z Washmgtona, vo &#353;tvrtok v noci na 12. hod.</formatting></line>
<line baseline="2819" l="989" t="2792" r="1589" b="2823"><formatting lang="Czech" ff="Times New Roman" fs="6.">svolali </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">konferenciu do Bieleho domu.</formatting></line></par>
<par leftIndent="41" l="1028" t="2860" r="1691" b="2891" type="fulltext">
<line baseline="2885" l="1028" t="2860" r="1691" b="2891"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Strach zahnal Churchilla do </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtonu.</formatting></line></par>
<par align="Justified" leftIndent="6" rightIndent="5" startIndent="315" lineSpacing="35" l="993" t="2916" r="1728" b="3203" type="fulltext">
<line baseline="2944" l="1361" t="2916" r="1724" b="2951"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. &#381;eneva, 19, j&#250;na.</formatting></line>
<line baseline="2980" l="1046" t="2948" r="1724" b="2987"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ako z </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtonu </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">oznamuj&#250;, ihne&#271; po</formatting></line>
<line baseline="3016" l="994" t="2992" r="1724" b="3023"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pr&#237;chode Churchilla do </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtonu boly </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">roz&#172;</formatting></line>
<line baseline="3052" l="993" t="3028" r="1724" b="3060"><formatting lang="Slovak" ff="Times New Roman" fs="6.">hovory medzi n&#237;m a Rooseveltom. Ako vo</formatting></line>
<line baseline="3088" l="993" t="3063" r="1725" b="3095"><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtone </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">hovoria, prekvapuj&#250;cu cestu</formatting></line>
<line baseline="3124" l="994" t="3100" r="1724" b="3131"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Churchilla do USA treba privies&#357; v s&#250;vislos&#357;</formatting></line>
<line baseline="3159" l="993" t="3135" r="1728" b="3167"><formatting lang="Slovak" ff="Times New Roman" fs="6.">s ve&#318;k&#253;m nedostatkom ton&#225;&#382;e a so situ&#225;ciou,'</formatting></line>
<line baseline="3195" l="993" t="3171" r="1688" b="3203"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ktor&#250; </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">vytvo&#345;ily </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">najnov&#353;ie vojensk&#233; udalosti.</formatting></line></par>
<par leftIndent="5" l="992" t="3230" r="1723" b="3262" type="fulltext">
<line baseline="3254" l="992" t="3230" r="1723" b="3262"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Churchillova cesta zahalen&#225; r&#250;&#353;kom tajomstva.</formatting></line></par>
<par align="Right" rightIndent="11" lineSpacing="36" l="1286" t="3290" r="1722" b="3321" type="fulltext">
<line baseline="3314" l="1286" t="3290" r="1722" b="3321"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. Amsterdam, 19. j&#250;na.</formatting></line></par>
<par align="Right" rightIndent="9" lineSpacing="36" l="1044" t="3326" r="1724" b="3358" type="fulltext">
<line baseline="3351" l="1044" t="3326" r="1724" b="3358"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Lond&#253;nsky   rozhlas   oznamuje   k   n&#225;v&#353;teve</formatting></line></par>
<par align="Right" rightIndent="10" lineSpacing="36" l="994" t="3361" r="1723" b="3393" type="fulltext">
<line baseline="3386" l="994" t="3361" r="1723" b="3393"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Churchilla v USA, &#382;e </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zpr&#225;va </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">o ceste Churchilla</formatting></line></par>
</block>
<block blockType="Text" l="1772" t="2394" r="2528" b="2650"><par align="Justified" lineSpacing="35" l="1784" t="2401" r="2517" b="2646" type="fulltext">
<line baseline="2427" l="1785" t="2401" r="2513" b="2434"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sa stala zn&#225;ma v Anglicku o 2. hodine r&#225;no</formatting></line>
<line baseline="2462" l="1784" t="2436" r="2513" b="2469"><formatting lang="Slovak" ff="Times New Roman" fs="6.">britsk&#233;ho letn&#233;ho &#269;asu a vyvolala obrovsk&#233;</formatting></line>
<line baseline="2497" l="1889" t="2472" r="2513" b="2505"><formatting lang="Slovak" ff="Times New Roman" fs="6.">penie. O tejto ceste boli informovan&#237;</formatting></line>
<line baseline="2532" l="1785" t="2507" r="2512" b="2542"><formatting lang="Slovak" ff="Times New Roman" fs="6.">iba najvy&#353;&#353;&#237; d&#244;stojn&#237;ci a &#269;lenovia kabinetu.</formatting></line>
<line baseline="2568" l="1784" t="2542" r="2512" b="2571"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Churchill e&#353;te v utorok bol na audiencii u kr&#225;&#172;</formatting></line>
<line baseline="2603" l="1786" t="2577" r="2517" b="2611"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#318;a. Vo </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtone </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">zpravodajcov &#269;asopisov &#8212;</formatting></line>
<line baseline="2639" l="1784" t="2612" r="2513" b="2646"><formatting lang="Slovak" ff="Times New Roman" fs="6.">tak hovor&#237; rozhlas &#271;alej &#8212; povolali na kon&#172;</formatting></line></par>
</block>
<block blockType="Text" l="2560" t="2388" r="3318" b="2640"><par align="Justified" lineSpacing="35" l="2571" t="2393" r="3302" b="2605" type="fulltext">
<line baseline="2418" l="2572" t="2393" r="3301" b="2423"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ferenciu k Rooseveltovmu sekret&#225;rovi Early*</formatting></line>
<line baseline="2454" l="2572" t="2429" r="3301" b="2462"><formatting lang="Slovak" ff="Times New Roman" fs="6.">mu, o tomto ich upovedomili v&#353;ak len 10 mi&#172;</formatting></line>
<line baseline="2490" l="2573" t="2464" r="3301" b="2500"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#250;t pred za&#269;at&#237;m konferencie Early im potom</formatting></line>
<line baseline="2524" l="2573" t="2495" r="3300" b="2530"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ozn&#225;mil n&#225;v&#353;tevu ChurchiUa. Early report&#233;rom</formatting></line>
<line baseline="2561" l="2571" t="2535" r="3302" b="2570"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vyhl&#225;sil, &#382;e od </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Roosevelta </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">a Churchilla v tom&#172;</formatting></line>
<line baseline="2596" l="2572" t="2570" r="3302" b="2605"><formatting lang="Slovak" ff="Times New Roman" fs="6.">to   t&#253;&#382;dni   nemo&#382;no   o&#269;ak&#225;va&#357;   nijak&#233;   vyhla-</formatting></line></par>
</block>
<block blockType="Text" l="1820" t="2670" r="3266" b="2796" type="text"><par lineSpacing="105" l="1835" t="2687" r="3250" b="2792" type="heading">
<line baseline="2774" l="1835" t="2687" r="3250" b="2792"><formatting lang="Slovak" ff="Times New Roman" fs="21.">Berl&#237;n k Churchillovej ceste</formatting></line></par>
</block>
<block blockType="Text" l="1770" t="2810" r="2524" b="3396"><par leftIndent="376" lineSpacing="36" l="2156" t="2818" r="2512" b="2849" type="fulltext">
<line baseline="2843" l="2156" t="2818" r="2512" b="2849"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. Berl&#237;n, 19. j&#250;na.</formatting></line></par>
<par align="Justified" leftIndent="1" rightIndent="1" startIndent="54" lineSpacing="36" l="1781" t="2854" r="2513" b="3141" type="fulltext">
<line baseline="2880" l="1835" t="2854" r="2512" b="2889"><formatting lang="Slovak" ff="Times New Roman" fs="6.">K n&#225;hlej ceste Churchilla do Ameriky vy&#172;</formatting></line>
<line baseline="2916" l="1781" t="2891" r="2512" b="2925"><formatting lang="Slovak" ff="Times New Roman" fs="6.">hlasuj&#250; v berl&#237;nskych politick&#253;ch kruhoch, &#382;e</formatting></line>
<line baseline="2952" l="1783" t="2926" r="2513" b="2962"><formatting lang="Slovak" ff="Times New Roman" fs="6.">op&#228;&#357; dokazuje slabos&#357; Anglicka, &#382;e zo &#353;tyroch</formatting></line>
<line baseline="2987" l="1783" t="2961" r="2513" b="2998"><formatting lang="Slovak" ff="Times New Roman" fs="6.">probl&#233;mov, ktor&#233; diplomatick&#253; dopisovate&#318;</formatting></line>
<line baseline="3024" l="1783" t="2997" r="2512" b="3028"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Reutera uviedol v s&#250;vislosti s touto cestou, naj&#172;</formatting></line>
<line baseline="3059" l="1783" t="3034" r="2512" b="3068"><formatting lang="Slovak" ff="Times New Roman" fs="6.">d&#244;le&#382;itej&#353;&#237; je probl&#233;m lodn&#233;ho priestoru. T&#225;to</formatting></line>
<line baseline="3096" l="1783" t="3070" r="2513" b="3103"><formatting lang="Slovak" ff="Times New Roman" fs="6.">cesta s&#250;&#269;asne dokazuje, &#382;e Angli&#269;ania nena&#172;</formatting></line>
<line baseline="3132" l="1782" t="3107" r="2296" b="3141"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ch&#225;dzaj&#250; viac nijak&#233; v&#253;chodisko.</formatting></line></par>
<par align="Justified" startIndent="53" lineSpacing="36" l="1780" t="3141" r="2514" b="3249" type="fulltext">
<line baseline="3168" l="1835" t="3141" r="2514" b="3176"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Cestu treba pova&#382;ova&#357; za alarmuj&#250;ci v&#253;krik</formatting></line>
<line baseline="3203" l="1782" t="3178" r="2513" b="3213"><formatting lang="Slovak" ff="Times New Roman" fs="6.">najkrajnej&#353;ej nemoh&#250;cnosti, v ktorej sa spo&#172;</formatting></line>
<line baseline="3241" l="1780" t="3217" r="2050" b="3249"><formatting lang="Slovak" ff="Times New Roman" fs="6.">jenci nach&#225;dzaj&#250;.</formatting></line></par>
<par align="Justified" leftIndent="1" startIndent="51" lineSpacing="36" l="1781" t="3249" r="2514" b="3392" type="fulltext">
<line baseline="3275" l="1832" t="3249" r="2512" b="3281"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Situ&#225;ciu dostato&#269;ne charakterizuje vyhl&#225;se&#172;</formatting></line>
<line baseline="3311" l="1781" t="3285" r="2512" b="3320"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nie anglickej zpravodajskej slu&#382;by, &#382;e Chur&#172;</formatting></line>
<line baseline="3347" l="1782" t="3321" r="2514" b="3351"><formatting lang="Slovak" ff="Times New Roman" fs="6.">chill nebude mat v Amerike &#269;as k vyst&#250;peniu</formatting></line>
<line baseline="3383" l="1782" t="3357" r="2513" b="3392"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pred  verejnos&#357; a  nebude  mat nijak&#233;  rozhla-</formatting></line></par>
</block>
<block blockType="Text" l="1268" t="3420" r="2250" b="3552" type="text"><par lineSpacing="124" l="1284" t="3424" r="2234" b="3548" type="heading">
<line baseline="3526" l="1284" t="3424" r="2234" b="3548"><formatting lang="Slovak" ff="Times New Roman" fs="21.">&#352;tyri ve&#318;k&#233; ot&#225;zky</formatting></line></par>
</block>
</page>
</document>"""
        desired_xml="""<document xmlns="http://www.abbyy.com/FineReader_xml/FineReader6-schema-v1.xml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="1.0" producer="FineReader 8.0" pagesCount="10" mainLanguage="Slovak" languages="Slovak,Czech,EnglishUnitedStates">
<page width="3488" height="5003" resolution="400">
<block blockType="Text" l="186" t="124" r="584" b="188" type="text"><par l="203" t="136" r="567" b="184" type="heading">
<line baseline="184" l="203" t="136" r="567" b="184"><formatting lang="Czech" ff="Arial" fs="11.">Cena </formatting><formatting lang="Slovak" ff="Arial" fs="11.">80 </formatting><formatting lang="Czech" ff="Arial" fs="11.">hal.</formatting></line></par>
</block>
<block blockType="Text" l="184" t="236" r="588" b="550"><par align="Justified" lineSpacing="30" l="199" t="242" r="570" b="546" type="fulltext">
<line baseline="269" l="201" t="242" r="568" b="269"><formatting lang="Czech" ff="Times New Roman" fs="6.">Adres? </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">redakcie </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">a </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">ad.</formatting></line>
<line baseline="297" l="201" t="275" r="567" b="299"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ministracie: </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Bratislava.</formatting></line>
<line baseline="330" l="200" t="305" r="570" b="335"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ulica </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Ro&#271;obrany &#269;&#237;elo</formatting></line>
<line baseline="361" l="200" t="337" r="570" b="362"><formatting lang="Slovak" ff="Times New Roman" fs="6.">12, </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Telefon </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">redakcie </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">a</formatting></line>
<line baseline="391" l="200" t="368" r="567" b="396"><formatting lang="Slovak" ff="Times New Roman" fs="6.">administr&#225;cie: 6820, 6821,</formatting></line>
<line baseline="422" l="199" t="399" r="567" b="427"><formatting lang="Slovak" ff="Times New Roman" fs="6.">6822, 2313, 3223, 2062.</formatting></line>
<line baseline="453" l="200" t="430" r="565" b="459"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Veci t&#253;kaj&#250;ce sa pred&#172;</formatting></line>
<line baseline="484" l="200" t="460" r="565" b="490"><formatting lang="Slovak" ff="Times New Roman" fs="6.">platn&#233;ho a inzer&#225;tov vy&#172;</formatting></line>
<line baseline="514" l="200" t="490" r="565" b="518"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bavuje ten admini&#172;</formatting></line>
<line baseline="545" l="306" t="523" r="451" b="546"><formatting lang="Slovak" ff="Times New Roman" fs="6." spacing="15">str&#225;cia.</formatting></line></par>
</block>
<block blockType="Text" l="212" t="628" r="984" b="688" type="text"><par l="228" t="637" r="969" b="683" type="heading">
<line baseline="673" l="228" t="637" r="969" b="683"><formatting lang="Slovak" ff="Arial" fs="9." spacing="-2">Bratislava, v sobotu 20. j&#250;na 1942</formatting></line></par>
</block>
<block blockType="Picture" l="632" t="80" r="2892" b="628" type="separator"/>
<block blockType="Text" l="1284" t="628" r="2128" b="688" type="text"><par l="1300" t="638" r="2124" b="684" type="heading">
<line baseline="674" l="1300" t="638" r="2124" b="684"><formatting lang="Slovak" ff="Arial" fs="9.">Zaklad&#225;f&#233;&#318; a vodca t Andrej Hlinka</formatting></line></par>
</block>
<block blockType="Text" l="2920" t="122" r="3312" b="186" type="text"><par l="2935" t="134" r="3295" b="181" type="heading">
<line baseline="181" l="2935" t="134" r="3295" b="181"><formatting lang="Slovak" ff="Arial" fs="11." spacing="-3">Ro&#269;n&#237;k </formatting><formatting lang="EnglishUnitedStates" ff="Arial" fs="11." spacing="-3">XXIV.</formatting></line></par>
</block>
<block blockType="Text" l="2916" t="236" r="3314" b="560"><par align="Justified" lineSpacing="32" l="2933" t="242" r="3298" b="555" type="fulltext">
<line baseline="266" l="2935" t="242" r="3296" b="271"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Predplatn&#233;: </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">y </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">Bratisl&#225;v*</formatting></line>
<line baseline="298" l="2934" t="273" r="3297" b="298"><formatting lang="Slovak" ff="Times New Roman" fs="6.">s don&#225;&#353;kou do domu 14</formatting></line>
<line baseline="330" l="2935" t="306" r="3297" b="335"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ks, postoa 20 Ks. Slo&#172;</formatting></line>
<line baseline="361" l="2936" t="337" r="3297" b="362"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vensko a Protektor&#225;t me&#172;</formatting></line>
<line baseline="393" l="2935" t="369" r="3297" b="398"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sa&#269;ne 20 Ks, &#353;tvxtro&#269;n*</formatting></line>
<line baseline="425" l="2933" t="401" r="3298" b="430"><formatting lang="Slovak" ff="Times New Roman" fs="6.">60 Ks, polro&#269;ne 120 Ks,</formatting></line>
<line baseline="458" l="2933" t="433" r="3297" b="458"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ro&#269;ne 240 Ks. Pre Fran&#172;</formatting></line>
<line baseline="489" l="2933" t="465" r="3298" b="491"><formatting lang="Slovak" ff="Times New Roman" fs="6.">c&#250;zsko, Nemecko a Ma&#172;</formatting></line>
<line baseline="522" l="2933" t="498" r="3298" b="523"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#271;arsko ro&#269;ne 300 Ks. In&#225;</formatting></line>
<line baseline="554" l="2933" t="529" r="3297" b="555"><formatting lang="Slovak" ff="Times New Roman" fs="6.">cudzina   rodne   433   K*.</formatting></line></par>
</block>
<block blockType="Text" l="3072" t="634" r="3290" b="684"><par l="3087" t="642" r="3274" b="679" type="fulltext">
<line baseline="678" l="3087" t="642" r="3274" b="679"><formatting lang="Slovak" ff="Arial" fs="8." spacing="-1">&#268;&#237;slo 138</formatting></line></par>
</block>
<block blockType="Text" l="176" t="766" r="972" b="4902" type="text"><par leftIndent="41" l="233" t="784" r="891" b="880" type="heading">
<line baseline="859" l="233" t="784" r="891" b="880"><formatting lang="Slovak" ff="Arial" fs="16.">Vojna a z&#225;sobovanie</formatting></line></par>
<par leftIndent="276" lineSpacing="39" l="468" t="888" r="967" b="943" type="fulltext">
<line baseline="930" l="468" t="888" r="967" b="943"><formatting lang="Slovak" ff="Times New Roman" fs="6.">(R. T.) Bratislava,   19. j&#250;na  |</formatting></line></par>
<par align="Justified" leftIndent="3" startIndent="61" lineSpacing="39" l="195" t="939" r="967" b="1808" type="fulltext">
<line baseline="972" l="259" t="939" r="966" b="981"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ka&#382;d&#225; vojna v dejin&#225;ch vy&#382;iadala si '</formatting></line>
<line baseline="1011" l="198" t="978" r="966" b="1026"><formatting lang="Slovak" ff="Times New Roman" fs="6.">obete a &#250;stupky aj od civiln&#233;ho obyvate&#318;- j</formatting></line>
<line baseline="1051" l="199" t="1011" r="967" b="1066"><formatting lang="Slovak" ff="Times New Roman" fs="6.">stva bojuj&#250;ceho &#353;t&#225;tu. Tieto sa </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">stup&#328;ovaly </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">J</formatting></line>
<line baseline="1090" l="198" t="1057" r="967" b="1100"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v pomere, ako sa vojna predl&#382;ovala. My |</formatting></line>
<line baseline="1129" l="198" t="1097" r="938" b="1132"><formatting lang="Slovak" ff="Times New Roman" fs="6.">dnes v &#353;tvrtom roku samostatn&#233;ho sloven&#172;</formatting></line>
<line baseline="1168" l="199" t="1135" r="940" b="1177"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sk&#233;ho &#353;t&#225;tu stoj&#237;me vlastne v &#353;tvrtom roku</formatting></line>
<line baseline="1207" l="196" t="1176" r="936" b="1218"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vojny a a&#382; dosia&#318; pochva&#318;ujeme si, &#382;e jej</formatting></line>
<line baseline="1246" l="197" t="1214" r="940" b="1257"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#225;sledky nedo&#318;ahly na n&#225;s tak tiesnivo, ako</formatting></line>
<line baseline="1286" l="198" t="1254" r="938" b="1293"><formatting lang="Slovak" ff="Times New Roman" fs="6.">azda inde. Ba ch&#253;r o na&#353;ich dobr&#253;ch ho&#172;</formatting></line>
<line baseline="1325" l="197" t="1293" r="940" b="1335"><formatting lang="Slovak" ff="Times New Roman" fs="6.">spod&#225;rskych pomeroch dostal sa a&#382; za hra&#172;</formatting></line>
<line baseline="1365" l="198" t="1334" r="941" b="1373"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nice, neh&#318;adiac na to, &#382;e &#269;asom </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">ud&#345;ely </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">tieto</formatting></line>
<line baseline="1404" l="195" t="1369" r="940" b="1414"><formatting lang="Slovak" ff="Times New Roman" fs="6.">priazniv&#233; a usporiadan&#233; pomery aj do o&#269;&#250;</formatting></line>
<line baseline="1443" l="199" t="1412" r="941" b="1447"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sam&#233;ho n&#225;&#353;ho ob&#269;ianstva, ktor&#233; nevedelo</formatting></line>
<line baseline="1482" l="197" t="1451" r="940" b="1492"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sa </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zprvu </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">v&#382;i&#357; do vojnovej situ&#225;cie, reptalo</formatting></line>
<line baseline="1522" l="198" t="1486" r="941" b="1531"><formatting lang="Slovak" ff="Times New Roman" fs="6.">a neuzn&#225;valo nijak&#250; vis major, do&#382;aduj&#250;c</formatting></line>
<line baseline="1561" l="197" t="1530" r="938" b="1570"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sa bez oh&#318;adu aj v z&#225;sobovan&#237; podmienok,</formatting></line>
<line baseline="1601" l="197" t="1570" r="940" b="1610"><formatting lang="Slovak" ff="Times New Roman" fs="6.">na ak&#233; bolo zvyknut&#233; v pokoji. T&#237;to oby&#172;</formatting></line>
<line baseline="1641" l="195" t="1610" r="940" b="1648"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vatelia &#353;t&#225;tu kone&#269;ne pochopili prav&#253; stav</formatting></line>
<line baseline="1680" l="197" t="1649" r="939" b="1689"><formatting lang="Slovak" ff="Times New Roman" fs="6.">a venovali svoju d&#244;veru zodpovedn&#253;m &#353;t&#225;t&#172;</formatting></line>
<line baseline="1719" l="195" t="1690" r="940" b="1729"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nym &#269;inite&#318;om. Preto dnes m&#244;&#382;eme s uspo&#172;</formatting></line>
<line baseline="1759" l="195" t="1728" r="940" b="1768"><formatting lang="Slovak" ff="Times New Roman" fs="6.">kojen&#237;m kon&#353;tatova&#357; u n&#225;s konsolid&#225;ciu</formatting></line>
<line baseline="1799" l="197" t="1770" r="618" b="1808"><formatting lang="Slovak" ff="Times New Roman" fs="6.">hospod&#225;rskych pomerov.</formatting></line></par>
<par align="Justified" leftIndent="2" rightIndent="25" startIndent="57" lineSpacing="39" l="194" t="1807" r="942" b="2512" type="fulltext">
<line baseline="1838" l="255" t="1807" r="938" b="1845"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#268;omu za to &#271;akova&#357;? </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Nepochybn&#233; </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">pre&#172;</formatting></line>
<line baseline="1877" l="198" t="1849" r="939" b="1885"><formatting lang="Slovak" ff="Times New Roman" fs="6.">dov&#353;etk&#253;m tomu, &#382;e sme sa v prav&#253; &#269;as</formatting></line>
<line baseline="1917" l="195" t="1886" r="940" b="1925"><formatting lang="Slovak" ff="Times New Roman" fs="6.">neb&#225;li pozrie&#357; tvrdej skuto&#269;nosti rovno do</formatting></line>
<line baseline="1956" l="197" t="1926" r="941" b="1963"><formatting lang="Slovak" ff="Times New Roman" fs="6.">o&#269;&#250;. Nesna&#382;ili sme sa uk&#225;ja&#357; sa m&#225;rnymi</formatting></line>
<line baseline="1995" l="195" t="1965" r="938" b="2004"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#225;dejami na nejak&#253; n&#225;hly vojensk&#253; obrat,</formatting></line>
<line baseline="2035" l="199" t="2004" r="941" b="2042"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ale s rozvahou, rozumne sme sa </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">vystrojili</formatting></line>
<line baseline="2074" l="199" t="2043" r="939" b="2083"><formatting lang="Slovak" ff="Times New Roman" fs="6.">a pripravili na cel&#253; priebeh vojny. Obyva&#172;</formatting></line>
<line baseline="2114" l="196" t="2085" r="938" b="2122"><formatting lang="Slovak" ff="Times New Roman" fs="6.">te&#318;stvu odkryli sme v prav&#253; &#269;as prav&#253; stav,</formatting></line>
<line baseline="2154" l="199" t="2119" r="939" b="2162"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Wci prv&#233; oper&#225;cie </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">boly </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">trocha bolestn&#233;.</formatting></line>
<line baseline="2193" l="197" t="2162" r="941" b="2201"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Pam&#228;tajme sa na prvotn&#253; z&#225;sah do distrib&#250;&#172;</formatting></line>
<line baseline="2233" l="195" t="2201" r="939" b="2242"><formatting lang="Slovak" ff="Times New Roman" fs="6.">cie m&#250;ky, cukru, m&#228;sa a in&#253;ch ka&#382;doden&#172;</formatting></line>
<line baseline="2272" l="194" t="2242" r="939" b="2281"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#253;ch potrav&#237;n. &#268;o sa vtedy vyskytlo re&#269;&#237;,</formatting></line>
<line baseline="2312" l="195" t="2281" r="941" b="2320"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nespokojnosti a ned&#244;very! Ale vl&#225;da vtedy</formatting></line>
<line baseline="2351" l="195" t="2321" r="941" b="2359"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bez oh&#318;adu na tak&#233;to psychologick&#233; sprie&#172;</formatting></line>
<line baseline="2390" l="195" t="2359" r="942" b="2398"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vodn&#233; zjavy s energiou zapla do pr&#225;ce cel&#253;</formatting></line>
<line baseline="2429" l="197" t="2399" r="942" b="2437"><formatting lang="Slovak" ff="Times New Roman" fs="6.">hospod&#225;rsky organiza&#269;n&#253; apar&#225;t a vyko&#172;</formatting></line>
<line baseline="2467" l="196" t="2437" r="940" b="2474"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nala radik&#225;lne z&#225;sahy do n&#225;&#353;ho hospod&#225;r&#172;</formatting></line>
<line baseline="2504" l="195" t="2475" r="774" b="2512"><formatting lang="Slovak" ff="Times New Roman" fs="6.">stva, distrib&#250;cie, ba aj v&#253;roby.   .</formatting></line></par>
<par align="Justified" leftIndent="2" rightIndent="21" startIndent="65" lineSpacing="39" l="194" t="2511" r="946" b="2710" type="fulltext">
<line baseline="2543" l="259" t="2511" r="946" b="2551"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#193;no, predov&#353;etk&#253;m tomu m&#244;&#382;eme by&#357;</formatting></line>
<line baseline="2581" l="194" t="2550" r="942" b="2589"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pov&#271;a&#269;n&#237;, &#382;e urobil sa poriadok od sam&#233;ho</formatting></line>
<line baseline="2621" l="196" t="2590" r="941" b="2629"><formatting lang="Slovak" ff="Times New Roman" fs="6.">za&#237;&#269;iatku. A&#382; potom pristupuj&#250; tu &#271;al&#353;&#237; f ak-</formatting></line>
<line baseline="2660" l="195" t="2629" r="941" b="2669"><formatting lang="Slovak" ff="Times New Roman" fs="6.">tori, ako je na&#353;a dobr&#225; zem, starostliv&#253;</formatting></line>
<line baseline="2699" l="194" t="2668" r="845" b="2710"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ro&#318;n&#237;k, pracovit&#253; robotn&#237;k a &#250;radn&#237;k.</formatting></line></par>
<par align="Justified" rightIndent="26" startIndent="60" lineSpacing="39" l="192" t="2715" r="941" b="3307" type="fulltext">
<line baseline="2745" l="253" t="2715" r="941" b="2753"><formatting lang="Slovak" ff="Times New Roman" fs="6.">O tento poriadok ide aj teraiz. </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Vojnov&#283;</formatting></line>
<line baseline="2784" l="193" t="2754" r="941" b="2793"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pomery n&#250;tia n&#225;s azda viac ako predt&#253;m</formatting></line>
<line baseline="2824" l="193" t="2794" r="939" b="2832"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pop&#250;&#353;&#357;af zo svojich n&#225;rokov. Bolo by ne&#172;</formatting></line>
<line baseline="2864" l="194" t="2834" r="939" b="2872"><formatting lang="Slovak" ff="Times New Roman" fs="6.">rozumn&#233; nebra&#357; ako hotov&#250; vec, &#382;e postup&#172;</formatting></line>
<line baseline="2904" l="193" t="2874" r="940" b="2907"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ne nedost&#225;va sa n&#225;m azda na trhu a v ob&#172;</formatting></line>
<line baseline="2944" l="194" t="2913" r="941" b="2951"><formatting lang="Slovak" ff="Times New Roman" fs="6.">chodoch to, alebo to&#318;ko, &#269;o a v akej miere</formatting></line>
<line baseline="2983" l="193" t="2952" r="940" b="2991"><formatting lang="Slovak" ff="Times New Roman" fs="6.">by sme chceli ma&#357;. Bolo by to nerozumn&#233;</formatting></line>
<line baseline="3023" l="193" t="2992" r="940" b="3031"><formatting lang="Slovak" ff="Times New Roman" fs="6.">najm&#228; preto, lebo vieme, &#382;e ani keby sme</formatting></line>
<line baseline="3063" l="193" t="3032" r="940" b="3070"><formatting lang="Slovak" ff="Times New Roman" fs="6.">veci brali najpesimistickej&#353;ie, nehrozia n&#225;m</formatting></line>
<line baseline="3102" l="194" t="3071" r="939" b="3110"><formatting lang="Slovak" ff="Times New Roman" fs="6.">tak&#233; pomery, ktor&#233; by sme s ist&#253;m seba&#172;</formatting></line>
<line baseline="3142" l="194" t="3112" r="940" b="3149"><formatting lang="Slovak" ff="Times New Roman" fs="6.">zapren&#237;m predsa pomerne &#318;ahko nemohli</formatting></line>
<line baseline="3181" l="192" t="3150" r="938" b="3189"><formatting lang="Slovak" ff="Times New Roman" fs="6.">prekona&#357;. Je tu teda len probl&#233;m a &#250;loha,</formatting></line>
<line baseline="3221" l="193" t="3190" r="940" b="3229"><formatting lang="Slovak" ff="Times New Roman" fs="6.">rozde&#318;ova&#357; &#382;ivotn&#233; potreby tak, aby sa</formatting></line>
<line baseline="3261" l="193" t="3226" r="938" b="3269"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ka&#382;d&#233;mu u&#353;lo spravodliv&#233;. To je poriadok,</formatting></line>
<line baseline="3300" l="194" t="3268" r="731" b="3307"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ktor&#253; si vy&#382;aduje dne&#353;n&#253; stav.</formatting></line></par>
<par align="Justified" leftIndent="1" rightIndent="26" startIndent="59" lineSpacing="39" l="193" t="3309" r="941" b="3784" type="fulltext">
<line baseline="3340" l="252" t="3309" r="939" b="3348"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Pre vykonanie tejto &#250;lohy odhlasoval v</formatting></line>
<line baseline="3379" l="193" t="3348" r="940" b="3388"><formatting lang="Slovak" ff="Times New Roman" fs="6.">uplynul&#253;ch d&#328;och Snem Najvy&#353;&#353;&#237; &#250;rad pre</formatting></line>
<line baseline="3419" l="194" t="3388" r="939" b="3427"><formatting lang="Slovak" ff="Times New Roman" fs="6.">z&#225;sobovanie, ktor&#253; u&#382; aj za&#269;al fungova&#357;.</formatting></line>
<line baseline="3459" l="196" t="3427" r="940" b="3467"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Je to in&#353;tit&#250;cia, ktor&#250; si nielen &#382;e vynucuj&#250;</formatting></line>
<line baseline="3498" l="193" t="3467" r="939" b="3507"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pomery, ale zriadenie ktorej d&#225;va nov&#253; d&#244;&#172;</formatting></line>
<line baseline="3538" l="193" t="3507" r="940" b="3545"><formatting lang="Slovak" ff="Times New Roman" fs="6.">kaz o na&#353;ej organiz&#225;cii a usporiadanosti</formatting></line>
<line baseline="3577" l="194" t="3547" r="941" b="3584"><formatting lang="Slovak" ff="Times New Roman" fs="6.">na&#353;ich pomerov v z&#225;sobovan&#237;. S&#225;m Vodca</formatting></line>
<line baseline="3617" l="194" t="3586" r="940" b="3624"><formatting lang="Slovak" ff="Times New Roman" fs="6.">a prezident Dr. Jozef Tiso vystihol jeho</formatting></line>
<line baseline="3657" l="193" t="3625" r="938" b="3664"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#250;lohu vo v&#253;zve na obyvate&#318;stvo Republiky,</formatting></line>
<line baseline="3697" l="193" t="3665" r="941" b="3704"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ke&#271; povedal, &#382;e m&#225; vyl&#250;&#269;i&#357;, pokia&#318; mo&#382;no</formatting></line>
<line baseline="3736" l="193" t="3706" r="939" b="3744"><formatting lang="Slovak" ff="Times New Roman" fs="6.">najviac, rozli&#269;n&#233; poruchy v z&#225;sobovan&#237;</formatting></line>
<line baseline="3776" l="194" t="3744" r="695" b="3784"><formatting lang="Slovak" ff="Times New Roman" fs="6.">brannej moci a obyvate&#318;stva.</formatting></line></par>
<par align="Justified" leftIndent="1" rightIndent="27" startIndent="60" lineSpacing="39" l="193" t="3783" r="940" b="4498" type="fulltext">
<line baseline="3816" l="253" t="3783" r="939" b="3823"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#218;loha tohto &#250;radu je teda v&#253;znamn&#225;</formatting></line>
<line baseline="3855" l="193" t="3824" r="938" b="3863"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nielen pre z&#225;zemie, ale menovite pre front.</formatting></line>
<line baseline="3895" l="195" t="3863" r="939" b="3903"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Discipl&#237;na, a len discipl&#237;na v &#353;t&#225;te, presn&#233;</formatting></line>
<line baseline="3934" l="196" t="3903" r="939" b="3942"><formatting lang="Slovak" ff="Times New Roman" fs="6.">dodr&#382;iavanie nariaden&#237; Najvy&#353;&#353;ieho &#250;radu</formatting></line>
<line baseline="3974" l="193" t="3943" r="940" b="3982"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pre z&#225;sobovanie s&#250; z&#225;kladnou po&#382;iadavkou</formatting></line>
<line baseline="4014" l="196" t="3983" r="939" b="4021"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#271;al&#353;ieho &#250;spe&#353;n&#233;ho boja na&#353;ich vojakov na</formatting></line>
<line baseline="4054" l="196" t="4023" r="939" b="4062"><formatting lang="Slovak" ff="Times New Roman" fs="6.">fronte, lebo len tak, ke&#271; sa uplatnia z&#225;sady</formatting></line>
<line baseline="4094" l="195" t="4062" r="938" b="4101"><formatting lang="Slovak" ff="Times New Roman" fs="6.">star&#233;ho vojensk&#233;ho riaden&#233;ho hospod&#225;rstva,</formatting></line>
<line baseline="4133" l="195" t="4102" r="939" b="4142"><formatting lang="Slovak" ff="Times New Roman" fs="6.">budeme m&#244;c&#357; zabezpe&#269;i&#357; chlieb a potraviny</formatting></line>
<line baseline="4173" l="194" t="4143" r="939" b="4180"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pre z&#225;zemie a menovite pre front. Tu me&#172;</formatting></line>
<line baseline="4212" l="194" t="4182" r="939" b="4219"><formatting lang="Slovak" ff="Times New Roman" fs="6.">novite platia &#271;al&#353;ie slov&#225; Vodcove: &#8222;Mier</formatting></line>
<line baseline="4252" l="195" t="4221" r="939" b="4260"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ob&#269;anov nez&#225;vis&#237; len od obilia, ale predo&#172;</formatting></line>
<line baseline="4291" l="194" t="4260" r="939" b="4299"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v&#353;etk&#253;m od spravodlivej de&#318;by toho, &#269;o</formatting></line>
<line baseline="4331" l="194" t="4299" r="939" b="4339"><formatting lang="Slovak" ff="Times New Roman" fs="6.">m&#225;me." Preto na dodr&#382;iavanie poriadku m&#225;</formatting></line>
<line baseline="4371" l="198" t="4339" r="939" b="4376"><formatting lang="Slovak" ff="Times New Roman" fs="6.">dba&#357; ka&#382;d&#253; ob&#269;an &#353;t&#225;tu. Preto sa tie&#382; k dis&#172;</formatting></line>
<line baseline="4411" l="194" t="4379" r="940" b="4418"><formatting lang="Slovak" ff="Times New Roman" fs="6.">poz&#237;cii Najvy&#353;&#353;ieho &#250;radu pre z&#225;sobovanie</formatting></line>
<line baseline="4451" l="198" t="4419" r="938" b="4452"><formatting lang="Slovak" ff="Times New Roman" fs="6.">dali z Nemecka sa </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">vr&#225;tiv&#353;&#237; </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">vodcovsk&#237; &#269;aka&#172;</formatting></line>
<line baseline="4489" l="195" t="4458" r="789" b="4498"><formatting lang="Slovak" ff="Times New Roman" fs="6.">telia Slovenskej pracovnej slu&#382;by.</formatting></line></par>
<par align="Justified" leftIndent="3" rightIndent="28" startIndent="59" lineSpacing="39" l="195" t="4498" r="939" b="4897" type="fulltext">
<line baseline="4529" l="254" t="4498" r="939" b="4538"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Zd&#244;raznili sme u&#382;, &#382;e na&#353;e hospod&#225;rske</formatting></line>
<line baseline="4570" l="195" t="4538" r="938" b="4578"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pomery v z&#225;sobovan&#237; s&#250; podstatne priazni&#172;</formatting></line>
<line baseline="4609" l="197" t="4579" r="938" b="4617"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vej&#353;ie, ne&#382; v mnoh&#253;ch cudz&#237;ch krajin&#225;ch.</formatting></line>
<line baseline="4648" l="197" t="4618" r="939" b="4657"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Napriek tomu v&#353;ak mus&#237; by&#357; snahou Naj&#172;</formatting></line>
<line baseline="4688" l="196" t="4657" r="939" b="4696"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vy&#353;&#353;ieho &#250;radu pre z&#225;sobovanie, aby vo ve&#172;</formatting></line>
<line baseline="4728" l="198" t="4697" r="938" b="4737"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ciach organiz&#225;cie z&#225;sobovania postupne pri&#172;</formatting></line>
<line baseline="4767" l="197" t="4736" r="936" b="4776"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bl&#237;&#382;il sa k dobr&#253;m cudz&#237;m vzorom, aby aj</formatting></line>
<line baseline="4807" l="197" t="4777" r="939" b="4816"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v z&#225;sobovan&#237;, v tomto po&#269;as vojny najd&#244;le&#172;</formatting></line>
<line baseline="4848" l="199" t="4817" r="939" b="4856"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#382;itej&#353;om odvetv&#237; verejn&#233;ho hospod&#225;rstva</formatting></line>
<line baseline="4888" l="197" t="4856" r="785" b="4897"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Mplaita&#237;l sa princfp&#237; spraTOdl&#237;vosti.</formatting></line></par>
</block>
<block blockType="Text" l="980" t="790" r="3320" b="1274" type="text"><par leftIndent="7" lineSpacing="260" l="996" t="832" r="3292" b="1068" type="heading">
<line baseline="1028" l="996" t="832" r="3292" b="1068"><formatting lang="Slovak" ff="Arial" fs="42.">Churchill znova vo </formatting><formatting lang="Czech" ff="Arial" fs="42.">Washingtone</formatting></line></par>
<par leftIndent="1" lineSpacing="96" l="989" t="1099" r="3303" b="1270" type="heading">
<line baseline="1160" l="989" t="1099" r="3296" b="1175"><formatting lang="Slovak" ff="Times New Roman" fs="14." spacing="-5">Posledn&#253; z&#250;fal&#253; krok Churchillov &#8212; No&#269;n&#225; porada v Bielom dome &#8212; Kruh</formatting></line>
<line baseline="1256" l="990" t="1184" r="3303" b="1270"><formatting lang="Slovak" ff="Times New Roman" fs="14.">okolo Sevastopolu a Tobruku st&#225;le u&#382;&#353;&#237; &#8212; &#270;al&#353;ie &#250;spechy v sever. Afrike</formatting></line></par>
</block>
<block blockType="Text" l="978" t="1312" r="1740" b="2222"><par leftIndent="321" lineSpacing="39" l="1306" t="1318" r="1729" b="1354" type="fulltext">
<line baseline="1345" l="1306" t="1318" r="1729" b="1354"><formatting lang="Slovak" ff="Times New Roman" fs="6.">EP. Washington,  19. j&#250;na.</formatting></line></par>
<par align="Justified" leftIndent="1" startIndent="35" lineSpacing="39" l="986" t="1357" r="1730" b="1863" type="fulltext">
<line baseline="1385" l="1022" t="1357" r="1729" b="1392"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Anglick&#253; ministersk&#253; predseda pod&#318;a &#250;rad&#172;</formatting></line>
<line baseline="1424" l="987" t="1397" r="1730" b="1431"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#233;ho ozn&#225;menia Bieleho domu pri&#353;iel op&#228;&#357; na</formatting></line>
<line baseline="1463" l="987" t="1435" r="1730" b="1471"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#225;v&#353;tevu do Spojen&#253;ch &#353;t&#225;tov. V jeho sprie&#172;</formatting></line>
<line baseline="1503" l="987" t="1475" r="1729" b="1509"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vode je &#353;&#233;f gener&#225;lneho &#353;t&#225;bu britsk&#233;ho Im&#172;</formatting></line>
<line baseline="1542" l="986" t="1514" r="1730" b="1548"><formatting lang="Slovak" ff="Times New Roman" fs="6.">p&#233;ria, </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Sir Allan </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">Brooke a tajomn&#237;k &#353;t&#225;bneho</formatting></line>
<line baseline="1582" l="988" t="1553" r="1730" b="1589"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#353;&#233;fa britsk&#253;ch arm&#225;dnych &#269;ast&#237;, gener&#225;l-major</formatting></line>
<line baseline="1621" l="988" t="1592" r="1728" b="1628"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ismay. &#218;&#269;elom tejto druhej n&#225;v&#353;tevy Churchil-</formatting></line>
<line baseline="1660" l="987" t="1632" r="1730" b="1666"><formatting lang="Slovak" ff="Times New Roman" fs="6.">lovej v USA od vypuknutia vojny s&#250;, ako to</formatting></line>
<line baseline="1699" l="987" t="1672" r="1728" b="1706"><formatting lang="Slovak" ff="Times New Roman" fs="6.">uv&#225;dza &#250;radn&#233; ozn&#225;menie, &#8222;Porady s </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Roose&#172;</formatting></line>
<line baseline="1739" l="986" t="1711" r="1729" b="1745"><formatting lang="Czech" ff="Times New Roman" fs="6.">veltem </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">o pokra&#269;ovan&#237; vo vojne". V Bielom do&#172;</formatting></line>
<line baseline="1778" l="986" t="1750" r="1728" b="1785"><formatting lang="Slovak" ff="Times New Roman" fs="6.">me e&#353;te po polnoci zadr&#382;ali nov&#250; konferenciu.</formatting></line>
<line baseline="1817" l="987" t="1790" r="1730" b="1824"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Doteraz v&#353;ak e&#353;te neozin&#225;mili, &#269;i sa Churchill</formatting></line>
<line baseline="1856" l="988" t="1829" r="1491" b="1863"><formatting lang="Slovak" ff="Times New Roman" fs="6.">tejto konferencie tie&#382; z&#250;&#269;astnil.</formatting></line></par>
<par align="Justified" startIndent="36" lineSpacing="39" l="985" t="1868" r="1730" b="2218" type="fulltext">
<line baseline="1896" l="1021" t="1868" r="1730" b="1902"><formatting lang="Slovak" ff="Times New Roman" fs="6.">V tla&#269;ov&#253;ch kruhoch americk&#233;ho hlavn&#233;ho</formatting></line>
<line baseline="1935" l="985" t="1908" r="1730" b="1942"><formatting lang="Slovak" ff="Times New Roman" fs="6.">mesta vyvolala t&#225;to nov&#225; n&#225;v&#353;teva Churchilla</formatting></line>
<line baseline="1975" l="987" t="1947" r="1728" b="1981"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ve&#318;k&#253; rozruch. Rooseveltov tajomn&#237;k, Early,</formatting></line>
<line baseline="2014" l="986" t="1986" r="1730" b="2021"><formatting lang="Slovak" ff="Times New Roman" fs="6.">prijal tla&#269;ov&#253;ch z&#225;stupcov, ktor&#237; sa objavili v</formatting></line>
<line baseline="2053" l="987" t="2025" r="1730" b="2060"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Bielom dome vo ve&#318;mi neobvyklej hodine a</formatting></line>
<line baseline="2092" l="990" t="2065" r="1730" b="2099"><formatting lang="Czech" ff="Times New Roman" fs="6.">sd&#283;lit </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">im, &#382;e v&#353;etky podrobnosti Churchillo-</formatting></line>
<line baseline="2132" l="987" t="2104" r="1730" b="2139"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vej n&#225;v&#353;tevy bud&#250; dr&#382;a&#357; v tajnosti. Ani od</formatting></line>
<line baseline="2171" l="989" t="2144" r="1729" b="2180"><formatting lang="Czech" ff="Times New Roman" fs="6.">Roosevelta, </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">ani od Churchilla nemo&#382;no vraj</formatting></line>
<line baseline="2211" l="988" t="2183" r="1728" b="2218"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v tomto t&#253;&#382;dni o&#269;ak&#225;va&#357; ak&#253;chko&#318;vek vyhl&#225;&#172;</formatting></line></par>
</block>
<block blockType="Text" l="1766" t="1314" r="2526" b="2214"><par align="Justified" leftIndent="1" rightIndent="2" lineSpacing="40" l="1776" t="1321" r="2515" b="1470" type="fulltext">
<line baseline="1348" l="1777" t="1321" r="2514" b="1355"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sen&#237; o svojich porad&#225;ch. Odpove&#271; na ot&#225;zky,</formatting></line>
<line baseline="1388" l="1778" t="1360" r="2515" b="1394"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#269;i prekvapuj&#250;ca n&#225;v&#353;teva Churchillova stoj&#237;</formatting></line>
<line baseline="1427" l="1776" t="1399" r="2515" b="1433"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v s&#250;vislosti s n&#225;v&#353;tevou Molotovovou, Early</formatting></line>
<line baseline="1466" l="1778" t="1438" r="1917" b="1470"><formatting lang="Slovak" ff="Times New Roman" fs="6.">odmietol,</formatting></line></par>
<par align="Justified" startIndent="320" lineSpacing="40" l="1775" t="1478" r="2517" b="2173" type="fulltext">
<line baseline="1505" l="2132" t="1478" r="2514" b="1512"><formatting lang="Slovak" ff="Times New Roman" fs="6.">EP. &#352;tokholm, 19. j&#250;na.</formatting></line>
<line baseline="1544" l="1812" t="1517" r="2516" b="1551"><formatting lang="Slovak" ff="Times New Roman" fs="6.">O nov&#353;ej ceste Churchilla do </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtonu</formatting></line>
<line baseline="1584" l="1777" t="1557" r="2516" b="1591"><formatting lang="Czech" ff="Times New Roman" fs="6.">nedo&#353;ly </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">e&#353;te &#353;v&#233;dskej tla&#269;i ob&#353;&#237;rnej&#353;ie komen&#172;</formatting></line>
<line baseline="1623" l="1779" t="1596" r="2516" b="1630"><formatting lang="Slovak" ff="Times New Roman" fs="6.">t&#225;re z Lond&#253;na, av&#353;ak z nieko&#318;ko do&#353;l&#253;ch</formatting></line>
<line baseline="1663" l="1777" t="1636" r="2515" b="1669"><formatting lang="Czech" ff="Times New Roman" fs="6.">zpr&#225;v </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">d&#225; sa vyvodzova&#357; predsa ur&#269;it&#233; z&#225;ve&#172;</formatting></line>
<line baseline="1702" l="1777" t="1675" r="2515" b="1710"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ry. D&#244;vod n&#225;hlej cesty anglick&#233;ho minister&#172;</formatting></line>
<line baseline="1741" l="1777" t="1714" r="2515" b="1748"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sk&#233;ho predsedu do USA spo&#269;&#237;vaj&#250; asi v ne&#172;</formatting></line>
<line baseline="1781" l="1776" t="1753" r="2516" b="1788"><formatting lang="Slovak" ff="Times New Roman" fs="6.">priaznivom v&#253;voji vojensk&#233;ho polo&#382;enia v </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Li&#172;</formatting></line>
<line baseline="1820" l="1776" t="1793" r="2517" b="1828"><formatting lang="Czech" ff="Times New Roman" fs="6.">byi </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">a v nebezpe&#269;&#237;, ktor&#233; sa za nimi rysuje a</formatting></line>
<line baseline="1863" l="1776" t="1836" r="2515" b="1871"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ktor&#233; ohrozuje cel&#233; anglo-americk&#233; postave&#172;</formatting></line>
<line baseline="1908" l="1776" t="1881" r="2516" b="1915"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nie na &#270;alekom v&#253;chode. &#381;e t&#225;to cesta m&#225;</formatting></line>
<line baseline="1950" l="1778" t="1923" r="2516" b="1958"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sl&#250;&#382;i&#357; hlavne vojensk&#253;m porad&#225;m a pl&#225;nom,</formatting></line>
<line baseline="1994" l="1775" t="1965" r="2515" b="2002"><formatting lang="Slovak" ff="Times New Roman" fs="6.">na to poukazuj&#250; u&#382; aj Churchillovi sprievodci,</formatting></line>
<line baseline="2036" l="1776" t="2007" r="2515" b="2044"><formatting lang="Czech" ff="Times New Roman" fs="6.">Sir Allan </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">Brooke a gener&#225;l-major Ismay, z kto&#172;</formatting></line>
<line baseline="2081" l="1777" t="2054" r="2516" b="2090"><formatting lang="Slovak" ff="Times New Roman" fs="6.">r&#253;ch posledn&#253; s Churchillom &#269;o naju&#382;&#353;ie spo&#172;</formatting></line>
<line baseline="2123" l="1777" t="2094" r="2516" b="2133"><formatting lang="Slovak" ff="Times New Roman" fs="6.">lupracuje a pre mnoh&#233; z jeho &#8222;strategick&#253;ch</formatting></line>
<line baseline="2164" l="1777" t="2133" r="2516" b="2173"><formatting lang="Slovak" ff="Times New Roman" fs="6.">rozhodnut&#237;" pova&#382;uj&#250; ho za jedine zodpoved-</formatting></line></par>
</block>
<block blockType="Text" l="2554" t="1314" r="3322" b="2214"><par align="Justified" startIndent="35" lineSpacing="42" l="2564" t="1322" r="3304" b="1788" type="fulltext">
<line baseline="1350" l="2599" t="1322" r="3300" b="1357"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#268;o sa t&#253;ka bezprostredn&#253;ch vn&#250;tropolitic&#172;</formatting></line>
<line baseline="1392" l="2564" t="1364" r="3301" b="1400"><formatting lang="Slovak" ff="Times New Roman" fs="6.">k&#253;ch &#250;&#269;inkov tejto novej Churchillovej cesty,</formatting></line>
<line baseline="1435" l="2564" t="1408" r="3302" b="1442"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pod&#318;a n&#225;znakov, poch&#225;dzaj&#250;cich z Lond&#253;na,</formatting></line>
<line baseline="1478" l="2565" t="1451" r="3302" b="1485"><formatting lang="Slovak" ff="Times New Roman" fs="6.">d&#225; sa vyvodzova&#357;, &#382;e udalos&#357;ami v L&#237;byi vy&#172;</formatting></line>
<line baseline="1521" l="2566" t="1494" r="3304" b="1528"><formatting lang="Slovak" ff="Times New Roman" fs="6.">volan&#225; siln&#225; vlna kritick&#253;ch hlasov proti</formatting></line>
<line baseline="1564" l="2567" t="1537" r="3303" b="1571"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#8222;strat&#233;govi a </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zpravodajsk&#233;mu </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">politikovi Chur-</formatting></line>
<line baseline="1607" l="2566" t="1580" r="3302" b="1614"><formatting lang="Slovak" ff="Times New Roman" fs="6.">chillo'i' aspo&#328; v tomto okam&#382;iku je uml&#269;an&#225;.</formatting></line>
<line baseline="1650" l="2567" t="1622" r="3304" b="1658"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Dokonca je vraj aj to mo&#382;n&#233;, &#382;e t&#225;to kritika</formatting></line>
<line baseline="1693" l="2566" t="1665" r="3304" b="1701"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bude &#250;pine udusen&#225;, ke&#271; Churchillova cesta</formatting></line>
<line baseline="1736" l="2567" t="1709" r="3303" b="1742"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bude mat za n&#225;sledok ak&#233;ko&#318;vek pozit&#237;vne</formatting></line>
<line baseline="1779" l="2565" t="1752" r="3231" b="1788"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v&#253;sledky o zriaden&#237;  &#8222;druh&#233;ho frontu"(l),</formatting></line></par>
<par leftIndent="178" l="2742" t="1814" r="3122" b="1846" type="fulltext">
<line baseline="1841" l="2742" t="1814" r="3122" b="1846"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Churchill u </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Roosevelta,</formatting></line></par>
<par align="Justified" startIndent="266" lineSpacing="43" l="2564" t="1869" r="3304" b="2210" type="fulltext">
<line baseline="1896" l="2864" t="1869" r="3302" b="1905"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. Amsterdam, 19. j&#250;na.</formatting></line>
<line baseline="1939" l="2598" t="1911" r="3302" b="1946"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ako hl&#225;si britsk&#225; </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zpravodajsk&#225; </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">slu&#382;ba oso&#172;</formatting></line>
<line baseline="1982" l="2566" t="1954" r="3302" b="1991"><formatting lang="Slovak" ff="Times New Roman" fs="6.">bitnou zpi&#225;vou, v Lond&#253;ne &#250;radne ozn&#225;mili,</formatting></line>
<line baseline="2026" l="2565" t="1999" r="3303" b="2034"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#382;e Churchill pri&#353;iel do Spojen&#253;ch &#353;t&#225;tov seve&#172;</formatting></line>
<line baseline="2069" l="2569" t="2041" r="3304" b="2077"><formatting lang="Slovak" ff="Times New Roman" fs="6.">roamerick&#253;ch. Churchilla. sprev&#225;dzaj&#250; </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">sir</formatting></line>
<line baseline="2112" l="2564" t="2083" r="3304" b="2122"><formatting lang="Czech" ff="Times New Roman" fs="6.">Alan </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">Brooke, &#353;&#233;f gener&#225;lneho &#353;t&#225;bu Imp&#233;ria</formatting></line>
<line baseline="2155" l="2566" t="2125" r="3304" b="2165"><formatting lang="Slovak" ff="Times New Roman" fs="6.">a gener&#225;.-major Ismay, sekret&#225;r &#353;&#233;fa &#353;t&#225;bneho</formatting></line>
<line baseline="2202" l="2564" t="2175" r="2681" b="2210"><formatting lang="Slovak" ff="Times New Roman" fs="6.">v&#253;boru.</formatting></line></par>
</block>
<block blockType="Text" l="1046" t="2242" r="3244" b="2366" type="text"><par lineSpacing="104" l="1060" t="2258" r="3228" b="2362" type="heading">
<line baseline="2353" l="1060" t="2258" r="3228" b="2362"><formatting lang="Czech" ff="Times New Roman" fs="21.">Roosevelt </formatting><formatting lang="Slovak" ff="Times New Roman" fs="21.">a Churchill si bud&#250; l&#225;ma&#357; hlavy</formatting></line></par>
</block>
<block blockType="Text" l="978" t="2396" r="1742" b="3398"><par leftIndent="308" lineSpacing="39" l="1295" t="2403" r="1731" b="2436" type="fulltext">
<line baseline="2429" l="1295" t="2403" r="1731" b="2436"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. Amsterdam, 19. j&#250;la.</formatting></line></par>
<par align="Justified" leftIndent="1" startIndent="36" lineSpacing="39" l="988" t="2441" r="1733" b="2666" type="fulltext">
<line baseline="2468" l="1024" t="2441" r="1731" b="2475"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Britsk&#225; </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zpravodajsk&#225; </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">slu&#382;ba hl&#225;si z </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Was&#172;</formatting></line>
<line baseline="2508" l="988" t="2480" r="1733" b="2514"><formatting lang="Czech" ff="Times New Roman" fs="6.">hingtonu, </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#382;e Biely dom ozn&#225;mil, &#382;e Churchill</formatting></line>
<line baseline="2545" l="988" t="2519" r="1730" b="2553"><formatting lang="Slovak" ff="Times New Roman" fs="6.">je op&#228;&#357; v Spojen&#253;ch &#353;t&#225;toch, aby s Roosevel-</formatting></line>
<line baseline="2584" l="991" t="2557" r="1732" b="2592"><formatting lang="Slovak" ff="Times New Roman" fs="6.">tom hne&#271; nadviazal rozhovory </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">o </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">tom, ako</formatting></line>
<line baseline="2624" l="989" t="2596" r="1730" b="2631"><formatting lang="Slovak" ff="Times New Roman" fs="6.">treba viest vojnu &#271;alej a ako ju mo&#382;no &#8222;vy&#172;</formatting></line>
<line baseline="2662" l="988" t="2635" r="1079" b="2666"><formatting lang="Slovak" ff="Times New Roman" fs="6.">hra&#357;".</formatting></line></par>
<par leftIndent="312" lineSpacing="39" l="1299" t="2674" r="1730" b="2707" type="fulltext">
<line baseline="2700" l="1299" t="2674" r="1730" b="2707"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. Amsterdam, 19. j&#250;na.</formatting></line></par>
<par align="Justified" rightIndent="2" startIndent="35" lineSpacing="39" l="987" t="2712" r="1731" b="2823" type="fulltext">
<line baseline="2740" l="1022" t="2712" r="1731" b="2747"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Podl&#225; </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zpr&#225;vy </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">britskej zpravodajskej slu&#382;by</formatting></line>
<line baseline="2780" l="987" t="2752" r="1730" b="2787"><formatting lang="Slovak" ff="Times New Roman" fs="6.">z Washmgtona, vo &#353;tvrtok v noci na 12. hod.</formatting></line>
<line baseline="2819" l="989" t="2792" r="1589" b="2823"><formatting lang="Czech" ff="Times New Roman" fs="6.">svolali </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">konferenciu do Bieleho domu.</formatting></line></par>
<par leftIndent="41" l="1028" t="2860" r="1691" b="2891" type="fulltext">
<line baseline="2885" l="1028" t="2860" r="1691" b="2891"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Strach zahnal Churchilla do </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtonu.</formatting></line></par>
<par align="Justified" leftIndent="6" rightIndent="5" startIndent="315" lineSpacing="35" l="993" t="2916" r="1728" b="3203" type="fulltext">
<line baseline="2944" l="1361" t="2916" r="1724" b="2951"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. &#381;eneva, 19, j&#250;na.</formatting></line>
<line baseline="2980" l="1046" t="2948" r="1724" b="2987"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Ako z </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtonu </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">oznamuj&#250;, ihne&#271; po</formatting></line>
<line baseline="3016" l="994" t="2992" r="1724" b="3023"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pr&#237;chode Churchilla do </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtonu boly </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">roz&#172;</formatting></line>
<line baseline="3052" l="993" t="3028" r="1724" b="3060"><formatting lang="Slovak" ff="Times New Roman" fs="6.">hovory medzi n&#237;m a Rooseveltom. Ako vo</formatting></line>
<line baseline="3088" l="993" t="3063" r="1725" b="3095"><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtone </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">hovoria, prekvapuj&#250;cu cestu</formatting></line>
<line baseline="3124" l="994" t="3100" r="1724" b="3131"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Churchilla do USA treba privies&#357; v s&#250;vislos&#357;</formatting></line>
<line baseline="3159" l="993" t="3135" r="1728" b="3167"><formatting lang="Slovak" ff="Times New Roman" fs="6.">s ve&#318;k&#253;m nedostatkom ton&#225;&#382;e a so situ&#225;ciou,'</formatting></line>
<line baseline="3195" l="993" t="3171" r="1688" b="3203"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ktor&#250; </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">vytvo&#345;ily </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">najnov&#353;ie vojensk&#233; udalosti.</formatting></line></par>
<par leftIndent="5" l="992" t="3230" r="1723" b="3262" type="fulltext">
<line baseline="3254" l="992" t="3230" r="1723" b="3262"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Churchillova cesta zahalen&#225; r&#250;&#353;kom tajomstva.</formatting></line></par>
<par align="Right" rightIndent="11" lineSpacing="36" l="1286" t="3290" r="1722" b="3321" type="fulltext">
<line baseline="3314" l="1286" t="3290" r="1722" b="3321"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. Amsterdam, 19. j&#250;na.</formatting></line></par>
<par align="Right" rightIndent="9" lineSpacing="36" l="1044" t="3326" r="1724" b="3358" type="fulltext">
<line baseline="3351" l="1044" t="3326" r="1724" b="3358"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Lond&#253;nsky   rozhlas   oznamuje   k   n&#225;v&#353;teve</formatting></line></par>
<par align="Right" rightIndent="10" lineSpacing="36" l="994" t="3361" r="1723" b="3393" type="fulltext">
<line baseline="3386" l="994" t="3361" r="1723" b="3393"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Churchilla v USA, &#382;e </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">zpr&#225;va </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">o ceste Churchilla</formatting></line></par>
</block>
<block blockType="Text" l="1772" t="2394" r="2528" b="2650"><par align="Justified" lineSpacing="35" l="1784" t="2401" r="2517" b="2646" type="fulltext">
<line baseline="2427" l="1785" t="2401" r="2513" b="2434"><formatting lang="Slovak" ff="Times New Roman" fs="6.">sa stala zn&#225;ma v Anglicku o 2. hodine r&#225;no</formatting></line>
<line baseline="2462" l="1784" t="2436" r="2513" b="2469"><formatting lang="Slovak" ff="Times New Roman" fs="6.">britsk&#233;ho letn&#233;ho &#269;asu a vyvolala obrovsk&#233;</formatting></line>
<line baseline="2497" l="1889" t="2472" r="2513" b="2505"><formatting lang="Slovak" ff="Times New Roman" fs="6.">penie. O tejto ceste boli informovan&#237;</formatting></line>
<line baseline="2532" l="1785" t="2507" r="2512" b="2542"><formatting lang="Slovak" ff="Times New Roman" fs="6.">iba najvy&#353;&#353;&#237; d&#244;stojn&#237;ci a &#269;lenovia kabinetu.</formatting></line>
<line baseline="2568" l="1784" t="2542" r="2512" b="2571"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Churchill e&#353;te v utorok bol na audiencii u kr&#225;&#172;</formatting></line>
<line baseline="2603" l="1786" t="2577" r="2517" b="2611"><formatting lang="Slovak" ff="Times New Roman" fs="6.">&#318;a. Vo </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Washingtone </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">zpravodajcov &#269;asopisov &#8212;</formatting></line>
<line baseline="2639" l="1784" t="2612" r="2513" b="2646"><formatting lang="Slovak" ff="Times New Roman" fs="6.">tak hovor&#237; rozhlas &#271;alej &#8212; povolali na kon&#172;</formatting></line></par>
</block>
<block blockType="Text" l="2560" t="2388" r="3318" b="2640"><par align="Justified" lineSpacing="35" l="2571" t="2393" r="3302" b="2605" type="fulltext">
<line baseline="2418" l="2572" t="2393" r="3301" b="2423"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ferenciu k Rooseveltovmu sekret&#225;rovi Early*</formatting></line>
<line baseline="2454" l="2572" t="2429" r="3301" b="2462"><formatting lang="Slovak" ff="Times New Roman" fs="6.">mu, o tomto ich upovedomili v&#353;ak len 10 mi&#172;</formatting></line>
<line baseline="2490" l="2573" t="2464" r="3301" b="2500"><formatting lang="Slovak" ff="Times New Roman" fs="6.">n&#250;t pred za&#269;at&#237;m konferencie Early im potom</formatting></line>
<line baseline="2524" l="2573" t="2495" r="3300" b="2530"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ozn&#225;mil n&#225;v&#353;tevu ChurchiUa. Early report&#233;rom</formatting></line>
<line baseline="2561" l="2571" t="2535" r="3302" b="2570"><formatting lang="Slovak" ff="Times New Roman" fs="6.">vyhl&#225;sil, &#382;e od </formatting><formatting lang="Czech" ff="Times New Roman" fs="6.">Roosevelta </formatting><formatting lang="Slovak" ff="Times New Roman" fs="6.">a Churchilla v tom&#172;</formatting></line>
<line baseline="2596" l="2572" t="2570" r="3302" b="2605"><formatting lang="Slovak" ff="Times New Roman" fs="6.">to   t&#253;&#382;dni   nemo&#382;no   o&#269;ak&#225;va&#357;   nijak&#233;   vyhla-</formatting></line></par>
</block>
<block blockType="Text" l="1820" t="2670" r="3266" b="2796" type="text"><par lineSpacing="105" l="1835" t="2687" r="3250" b="2792" type="heading">
<line baseline="2774" l="1835" t="2687" r="3250" b="2792"><formatting lang="Slovak" ff="Times New Roman" fs="21.">Berl&#237;n k Churchillovej ceste</formatting></line></par>
</block>
<block blockType="Text" l="1770" t="2810" r="2524" b="3396"><par leftIndent="376" lineSpacing="36" l="2156" t="2818" r="2512" b="2849" type="fulltext">
<line baseline="2843" l="2156" t="2818" r="2512" b="2849"><formatting lang="Slovak" ff="Times New Roman" fs="6.">STK. Berl&#237;n, 19. j&#250;na.</formatting></line></par>
<par align="Justified" leftIndent="1" rightIndent="1" startIndent="54" lineSpacing="36" l="1781" t="2854" r="2513" b="3141" type="fulltext">
<line baseline="2880" l="1835" t="2854" r="2512" b="2889"><formatting lang="Slovak" ff="Times New Roman" fs="6.">K n&#225;hlej ceste Churchilla do Ameriky vy&#172;</formatting></line>
<line baseline="2916" l="1781" t="2891" r="2512" b="2925"><formatting lang="Slovak" ff="Times New Roman" fs="6.">hlasuj&#250; v berl&#237;nskych politick&#253;ch kruhoch, &#382;e</formatting></line>
<line baseline="2952" l="1783" t="2926" r="2513" b="2962"><formatting lang="Slovak" ff="Times New Roman" fs="6.">op&#228;&#357; dokazuje slabos&#357; Anglicka, &#382;e zo &#353;tyroch</formatting></line>
<line baseline="2987" l="1783" t="2961" r="2513" b="2998"><formatting lang="Slovak" ff="Times New Roman" fs="6.">probl&#233;mov, ktor&#233; diplomatick&#253; dopisovate&#318;</formatting></line>
<line baseline="3024" l="1783" t="2997" r="2512" b="3028"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Reutera uviedol v s&#250;vislosti s touto cestou, naj&#172;</formatting></line>
<line baseline="3059" l="1783" t="3034" r="2512" b="3068"><formatting lang="Slovak" ff="Times New Roman" fs="6.">d&#244;le&#382;itej&#353;&#237; je probl&#233;m lodn&#233;ho priestoru. T&#225;to</formatting></line>
<line baseline="3096" l="1783" t="3070" r="2513" b="3103"><formatting lang="Slovak" ff="Times New Roman" fs="6.">cesta s&#250;&#269;asne dokazuje, &#382;e Angli&#269;ania nena&#172;</formatting></line>
<line baseline="3132" l="1782" t="3107" r="2296" b="3141"><formatting lang="Slovak" ff="Times New Roman" fs="6.">ch&#225;dzaj&#250; viac nijak&#233; v&#253;chodisko.</formatting></line></par>
<par align="Justified" startIndent="53" lineSpacing="36" l="1780" t="3141" r="2514" b="3249" type="fulltext">
<line baseline="3168" l="1835" t="3141" r="2514" b="3176"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Cestu treba pova&#382;ova&#357; za alarmuj&#250;ci v&#253;krik</formatting></line>
<line baseline="3203" l="1782" t="3178" r="2513" b="3213"><formatting lang="Slovak" ff="Times New Roman" fs="6.">najkrajnej&#353;ej nemoh&#250;cnosti, v ktorej sa spo&#172;</formatting></line>
<line baseline="3241" l="1780" t="3217" r="2050" b="3249"><formatting lang="Slovak" ff="Times New Roman" fs="6.">jenci nach&#225;dzaj&#250;.</formatting></line></par>
<par align="Justified" leftIndent="1" startIndent="51" lineSpacing="36" l="1781" t="3249" r="2514" b="3392" type="fulltext">
<line baseline="3275" l="1832" t="3249" r="2512" b="3281"><formatting lang="Slovak" ff="Times New Roman" fs="6.">Situ&#225;ciu dostato&#269;ne charakterizuje vyhl&#225;se&#172;</formatting></line>
<line baseline="3311" l="1781" t="3285" r="2512" b="3320"><formatting lang="Slovak" ff="Times New Roman" fs="6.">nie anglickej zpravodajskej slu&#382;by, &#382;e Chur&#172;</formatting></line>
<line baseline="3347" l="1782" t="3321" r="2514" b="3351"><formatting lang="Slovak" ff="Times New Roman" fs="6.">chill nebude mat v Amerike &#269;as k vyst&#250;peniu</formatting></line>
<line baseline="3383" l="1782" t="3357" r="2513" b="3392"><formatting lang="Slovak" ff="Times New Roman" fs="6.">pred  verejnos&#357; a  nebude  mat nijak&#233;  rozhla-</formatting></line></par>
</block>
<block blockType="Text" l="1268" t="3420" r="2250" b="3552" type="text"><par lineSpacing="124" l="1284" t="3424" r="2234" b="3548" type="heading">
<line baseline="3526" l="1284" t="3424" r="2234" b="3548"><formatting lang="Slovak" ff="Times New Roman" fs="21.">&#352;tyri ve&#318;k&#233; ot&#225;zky</formatting></line></par>
</block>
</page>
</document>"""

        actual_xml = etree.fromstring(original_xml)
        actual_xml = SeparatorId.discriminant_separators(actual_xml)
        desired_xml = etree.fromstring(desired_xml)
        self.assertEqual(
            re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(desired_xml)
                   .decode('utf-8')),
            re.sub("[\a\f\n\r\t\v ]", '', etree.tostring(actual_xml)
                   .decode('utf-8')))

