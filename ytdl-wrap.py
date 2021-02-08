# 1. mktemp
# 2. zapis poznamku ze co robit
# 3. vyparsuj urlcka 
# 4. aktualizuj youtube-dl
# 5. zapni command
# 6. ?? post ffmpeg
# 7. oznam ze hotovo

from tempfile import NamedTemporaryFile
from subprocess import run
from sys import argv
from os import remove
import re

List = lambda X:X
#List = list

UrlRx = re.compile('(^|[\\s])(https?://[^\\s]+)[\\s]?')

YtdlParams = {
    'audio': ['--extract-audio','--audio-format','mp3'],
    'video': ['--merge-output-format','mp4']
}

def main(target_type):
    TMPF = NamedTemporaryFile(delete=False, mode='w')
    TMPF.write(
        '# Vloz odkazy na stiahnutie, na kazdy riadok jeden\n'
        + '# Nasledne editor zavri a uloz'
    )
    TMPF.close()
    run(['notepad',TMPF.name]) 
    run('pip install --upgrade youtube-dl')
    with open(TMPF.name) as f:
        Links = f.read()

    Links = Links.split('\n')
    Links = List(map(lambda X: X.split('#')[0], Links))
    Links = List(filter(lambda X: re.search(UrlRx, X), Links))
    Links = list(map(lambda X: re.search(UrlRx, X).group(2), Links))
    run(['youtube-dl']+YtdlParams[target_type]+Links)
    remove(TMPF.name)

if __name__ == '__main__':
    if not argv[1] in {'audio','video'}:
        raise ValueError('unknown download type')
    main(argv[1])
