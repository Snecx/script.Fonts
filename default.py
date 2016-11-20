import os
import xbmc
import xbmcaddon
import sys
import ConfigParser
import io
import shutil

_addon = xbmcaddon.Addon()
_addon_path = _addon.getAddonInfo('path')

def CopyFont(source):
     for file in os.listdir(source):
       if file.endswith(".ttf"):
         xbmc.log('script.Fonts:' + file, level=xbmc.LOGNOTICE)
         path1 = xbmc.translatePath(_addon.getAddonInfo('path')).decode('utf-8')
         path2 = path1.replace("script.Fonts","")
         path3 = path2 + "skin.aeon.madnox/fonts/"
         try:
             shutil.copy2(source + "/" + file, path3 + file)
         except Exception , msg:
             xbmc.log("script.Font:" + str(msg), level=xbmc.LOGNOTICE)
             return False
         return True
     return False
 
def MakeNewFontXML(siz,filenam,asp,linesp,sty):
    path1 = xbmc.translatePath(_addon.getAddonInfo('path')).decode('utf-8')
    path2 = path1.replace("script.Fonts","")
    noxfontdir = path2 + "skin.aeon.madnox/1080i/font.xml"
    tempfile = path2 + "skin.aeon.madnox/1080i/temp"
    
    array = []
    count = 0
    fontxml = []
    start = 100
    try:
      with open(noxfontdir, "r") as ins:
       for line in ins:
        count = count + 1
        if count < 4:
            fontxml.append(line)
        if count == 4:
            fontxml.append("        <!-- script.Font -->\n")
            fontxml.append("        <font>\n")
            fontxml.append("            <name>MenubarFont</name>\n")
            fontxml.append("            <filename>"+ filenam + "</filename>\n")
            fontxml.append("            <linespacing>" + linesp + "</linespacing>\n")
            fontxml.append("            <aspect>" + asp +"</aspect>\n")
            fontxml.append("            <size>" + siz +"</size>\n")
            fontxml.append("            <style>" + sty +"</style>\n")
            fontxml.append("        </font>\n")
            fontxml.append("        <!-- script.Font -->\n")
            
            if "script.Font" in line:
                xbmc.log("t:found", level=xbmc.LOGNOTICE)
                start = 13
            else:
                fontxml.append(line)  
                start = 4
        if count > start:   
            fontxml.append(line)  
      f = open(tempfile,'w')
      for l in fontxml:
        f.write(l)
      f.close()
      return True
           
    except Exception , msg:
           xbmc.log("script.Font:" + str(msg), level=xbmc.LOGNOTICE)
           return False
           
        
def RenameFontfile(log):
    path1 = xbmc.translatePath(_addon.getAddonInfo('path')).decode('utf-8')
    path2 = path1.replace("script.Fonts","")
    noxfontdir = path2 + "skin.aeon.madnox/1080i/font.xml"
    tempfile = path2 + "skin.aeon.madnox/1080i/temp"
    #xbmc.log("script.Font:" + noxfontdir, level=xbmc.LOGNOTICE)
    #xbmc.log("script.Font:" + tempfile, level=xbmc.LOGNOTICE)
    
    try:
        shutil.copy2(tempfile, noxfontdir)
    except Exception , msg:
        xbmc.log("script.Font:" + str(msg), level=xbmc.LOGNOTICE)
        return False
    return True
    
if __name__ == '__main__':
    xbmc.log('script.Fonts:Trying to activate font from dir:' + sys.argv[1], level=xbmc.LOGNOTICE)
    fontdir = sys.argv[1]
    
    size = ""
    filename = ""
    aspect = ""
    linespacing = ""
    style = ""
    
    ret = CopyFont(fontdir)
    
    if ret == True:
        try:
           config = ConfigParser.RawConfigParser()
           config_file = fontdir + "/font.cfg"
           #xbmc.log("t:" + config_file, level=xbmc.LOGNOTICE)
           config.read(config_file)
        
           size = config.get("font", "size")
           filename = config.get("font", "filename")
           aspect = config.get("font", "aspect")
           linespacing = config.get("font", "linespacing")
           style = config.get("font", "style")
           
           ret = MakeNewFontXML(size,filename,aspect,linespacing,style)
           if ret == True:
               ret = RenameFontfile("")
               if ret == True:
                   xbmc.executebuiltin("ReloadSkin()")
               else:
                   xbmc.log("script.Font:Error renaming temp file to font.xml file", level=xbmc.LOGNOTICE)
           else:
              xbmc.log("script.Font:Error creating temp font file", level=xbmc.LOGNOTICE)
           
        except Exception , msg:
           xbmc.log("script.Font:" + str(msg), level=xbmc.LOGNOTICE)
        
    else:
       xbmc.log('script.Fonts: Error copying font! Setting to default.', level=xbmc.LOGNOTICE)
       ret = MakeNewFontXML("112","MC360.ttf","0.67","","bold uppercase")
       if ret == True:
            ret = RenameFontfile("")
            if ret == True:
                 xbmc.executebuiltin("ReloadSkin()")
            else:
                 xbmc.log("script.Font:Error renaming temp file to font.xml file", level=xbmc.LOGNOTICE)
       else:
            xbmc.log("script.Font:Error creating temp font file", level=xbmc.LOGNOTICE)
