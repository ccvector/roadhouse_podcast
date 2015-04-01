from __future__ import print_function
import os
import re
import urllib

def check(mp3name):
    if os.path.exists(mp3name):
        name = os.path.splitext(mp3name)[0]
        duplicate = []
        for filename in os.listdir('.'):
            pattern = r'{}_(\d+?)\.mp3'.format(name)
            match = re.search(pattern, filename)
            if match:
                duplicate.append(int(match.group(1)))
        if duplicate:
            max_number = max(duplicate)
        else:
            max_number = 1
        new_filename = '{}_{}.mp3'.format(name, max_number + 1)
    else:
        new_filename = mp3name
    return new_filename

def scrape():
    for year in range(2014, 2015):
        for month in range(1, 13):
            if year == 2014 and month <= 9:
                continue
            home = 'http://roadhousepodcast.com'
            archive = '{}/{}/{:02}/'.format(home, year, month)
            print(archive)
            try:
                text_archive = urllib.urlopen(archive).read()
            except IOError:
                print('I/O error! Skipped the url.')
                continue
            else:
                pattern = r'href="({}\d\d/.+?/)"'.format(archive)
                urls = re.findall(pattern, text_archive)
            for url in set(urls):
                print('\t{}'.format(url))
                try:
                    text_link = urllib.urlopen(url).read()
                except IOError:
                    print('\tI/O error! Skipped the url.')
                    continue
                else:
                    match = re.search(r'<a href="(http://[^"]+?\.mp3)">', text_link)
                if match:
                    mp3link = match.group(1)
                    print('\t\t{}'.format(mp3link))
                    mp3name = '{}_{:02}_{}'.format(year, month, os.path.split(mp3link)[1])
                    print('\t\t{}'.format(mp3name))
                    try:
                        mp3name = check(mp3name)
                        urllib.urlretrieve(mp3link, mp3name)
                    except IOError:
                        print('\t\tI/O error! Skipped the url.')
                        continue
                    else:
                        size = os.path.getsize(mp3name)
                        if size < 9000000:
                            os.remove(mp3name)
                            print('\t\tthe file is too small. deleted file.')
                else:
                    print('\t\tmp3 not found')
    return

def main():
    scrape()

if __name__ == '__main__':
    main()

