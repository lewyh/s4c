from __future__ import print_function, division
import urllib2
from bs4 import BeautifulSoup as bs 
import string

def get_rtmp(pid):
    html = urllib2.urlopen("http://beta.s4c.co.uk/clic/e_level2.shtml?"\
                           "programme_id={0}".format(pid))
    soup = bs(html.read())
    player_script = soup('script')[-3]
    fn = player_script.contents[0].split('file:')[1].split("\"")[1]
    url = ("rtsp://ec2-46-51-181-116.eu-west-1.compute.amazonaws.com/"\
            "httpl/_definst_/mp4:amazons3/bsmvid/{0}.mp4".format(fn))
    return url

def more_episodes(soup):
    lst_prgs = soup.findAll(attrs={'class':'latest programme-list-container'})
    more_eps = lst_prgs[0]
    eps_arr = more_eps.find_all('li')
    titles = []
    pids = []
    for ep in eps_arr:
        titles.append(ep.find('p').contents[0])
        pidline = ep.findAll('a')[-1]
        pid = str(pidline).split('=')[2].split('\"')[0]
        pids.append(pid)
    return pids, titles

def scrape_showinfo(showpid):
    info = {}
    html = urllib2.urlopen("http://beta.s4c.co.uk/clic/e_level2.shtml?"\
                           "programme_id={0}".format(showpid))
    soup = bs(html.read())

    titlediv = soup.find_all(attrs={'class':'prog-title clearfix'})
    titleh1 = titlediv[0].find_all('h1')
    info['title'] = str(titleh1).split('>')[1].split('|')[0].split('<')[0].strip()
    eptitle = str(soup.find_all('span')).split('-')[1].split('<')[0].strip()
    print(info['title'])
    multiep = 'episodes' in str(soup.contents)
    if multiep:
        info['flat'] = False
        # Code to fetch "more episodes" PIDs
        pids, titles = more_episodes(soup)
        info['pids'] = [showpid] + pids
        info['eptitles'] = [eptitle] + titles
    else:
        info['flat'] = True
        info['pids'] = [showpid]
        info['eptitles'] = [eptitle]

    return info


def scrape_epinfo(pid):
    return

class episode():
     def __init__(self, pid):
        """docstring for fname"""
        self.pid = pid 
        self.title = None
        self.synopsis = None
        self.expiry = None
        self.airdate = None
        self.duration = None
        self.ipblock = None
        self.rtmp = get_rtmp(pid) 


class show():
    def __init__(self, showpid):
        """docstring for __init__"""
        info = scrape_showinfo(showpid)
        self.flat = info['flat']
        self.title = info['title']
        self.pids = info['pids']
        self.episodes = {}
        self.eptitles = info['eptitles']
        for pid in self.pids:
            self.episodes[pid] = episode(pid)
        

d = {}
html = urllib2.urlopen('http://beta.s4c.co.uk/clic/e_a2z.shtml?l=A-Z')
soup = bs(html.read())
lst = soup.body.findAll(attrs = {'class' : 'large-list-programmes-list'})
lst_splt = lst[0].findAll(attrs = {'class' : 'switch closed'})
id_splt = lst[0].findAll(attrs = {'class' : 'switched-content clearfix'})
n = len(lst_splt)
n_i_dict = {}
for i in range(len(lst_splt)):
    ln = lst_splt[i].find_all('h3')
#    show = str(ln).split('>')[1].split('<')[0].strip()

    showid = str(id_splt[i]).split('programme_id=')[1].split('\">')[0]
    d[show] = ""
    n_i_dict[i] = show(showid)
