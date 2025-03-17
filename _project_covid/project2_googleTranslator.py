import json
from googletrans import Translator

#json 형태로 저장/불러오기
#저장위치, 이름, 저장할 데이터, 저장/불러오기
def SaveLoad(path, name, data = None, w = False) :
    fullPath = "%s/%s.txt" %(path, name)
    if w :
        with open(fullPath, "w", encoding = "utf-8") as f :
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
            f.close()
    else :
        with open(fullPath, "r", encoding = "utf-8") as f :
            data = json.load(f)
            f.close()
            return data

popularCityList = SaveLoad("C:/py_temp/temp", "popularCity")

popularCityKoList = list()

for i in popularCityList :
    translator = Translator()
    result = translator.translate(i, src="en", dest="ko")
    popularCityKoList.append(result.text)

SaveLoad("C:/py_temp/temp", "popularCityKo", popularCityKoList, True)


#===============================================================================
tempList = SaveLoad("C:/py_temp/temp", "popularCityKo")
popularCityKoList = list()

for i in tempList :
    city = i.replace(" ", "").rstrip("도시")
    
    if city == "JohorBahru." : city = "조호르바루"
    elif city == "Zhuhai." : city = "주하이"
    elif city == "heraklion." : city = "헤라클리온"
    elif city == "무덤" : city = "물라"
    elif city == "심천" : city = "선전"
    elif city == "올랜" : city = "올랜도"
    elif city == "계곡" : city = "구이린"
    elif city == "서울" : continue
    elif city == "제주" : continue
    
    popularCityKoList.append(city)

SaveLoad("C:/py_temp/temp", "popularCityKo2", popularCityKoList, True)
popularCityKoList = SaveLoad("C:/py_temp/temp", "popularCityKo2")

#======================================
popularCityKoList
#======================================
#===============================================================================