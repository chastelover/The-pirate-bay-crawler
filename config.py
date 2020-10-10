MONGO_URL = 'localhost'
MONGO_DB  = 'magnetresult'
#MONGO_TABLE = 'magnet'

MODE = 'search' #search,recent
if(MODE=='recent'):
    CONTENT='Recent Torrents'
    FORMAT =''
if(MODE=='search'):
    CONTENT = 'The Avengers'  # search content
    FORMAT = 'apps' #all,audio,video,apps,games,pron,other
ISEXPLICIT = True

URL = 'https://thepiratebay.org/index.html'
RECENT_URL='https://thepiratebay.org/search.php?q=top100:recent'
#PATH = 'C:\\Users\\y\\Anaconda3\\Scripts\\chromedriver.exe'
MONGO_TABLE = CONTENT + '_' + FORMAT
FILENAME = CONTENT + '_' +FORMAT +'.json'

