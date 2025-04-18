




import os
from PIL import Image


from p_weather.openweathermap import OpenWeatherMap,OpenWeatherMapSettings
from p_weather.sprites import Sprites
from p_weather.draw_weather import DrawWeather

import secrets


class WeatherLandscape:

    TMP_DIR = "tmp"
    OUT_FILENAME = "output/test_"
    OUT_FILEEXT = ".bmp"
    TEMPLATE_FILENAME = "/Users/ryem/Desktop/Cornell_Tech/fun/Playing_with_CLUEboard/final_project/weather_landscape-main/p_weather/template.bmp"
    SPRITES_DIR="p_weather/sprite"
    DRAWOFFSET = 65
    bmp_index_WeatherLandscape = 0


    def __init__(self):
        assert secrets.OWM_KEY != "000000000000000000", "Set OWM_KEY variable to your OpenWeather API key in secrets.py"
        pass




    def MakeImage(self)->Image:
    
    
        cfg = OpenWeatherMapSettings.Fill( secrets, self.TMP_DIR )
        owm = OpenWeatherMap(cfg)
        owm.FromAuto()

        img = Image.open(self.TEMPLATE_FILENAME)

        spr = Sprites(self.SPRITES_DIR,img)

        art = DrawWeather(img,spr)
        art.Draw(self.DRAWOFFSET,owm)

        return img



    def SaveImage(self, bmp_index)->str:
        self.bmp_index_WeatherLandscape = bmp_index
        img = self.MakeImage()
        placekey = OpenWeatherMap.MakePlaceKey(secrets.OWM_LAT,secrets.OWM_LON)
        outfilepath = self.TmpFilePath(self.OUT_FILENAME+bmp_index+self.OUT_FILEEXT)
        img.save(outfilepath) 
        return outfilepath
        
        

    def TmpFilePath(self,filename):
        return os.path.join(self.TMP_DIR,filename)