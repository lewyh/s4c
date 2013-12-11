from __future__ import print_function, division
#from bs4 import BeautifulSoup as bs
import urllib2

#import xbmc
#import xbmcgui

testurl = "http://www.s4c.co.uk/clic/e_level2.shtml?series_id=516193014"

def fetchURL(shtml):
    html = urllib2.urlopen(shtml)
    soup = bs(html.read())
    player_script = soup('script')[14]
    url_mp4 = player_script.contents[0].split('file:')[1].split("\"")[1]
    url_rtmp = player_script.contents[0].split('streamer:')[1].split("\"")[1]
    url = "{0}{1}".format(url_rtmp, url_mp4)
    return url

#class Main:
#    def __init__(self, url):
#        playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
#        playlist.clear()
#        playlist.add(fetchURL(url))
#        xbmc.Player().play(playlist)

#m = Main()
#playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
#playlist.clear()
#playlist.add(fetchURL(url))
xbmc.Player().play("rtmp://sfourc.fcod.llnwd.net/a7175/o45/s4c/uk/BSM/y_gwyll__pennod_2_2_o_2_cymraeg_dv50_b_r5b90r_001eacbdb4.mp4")