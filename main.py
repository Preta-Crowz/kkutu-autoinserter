import psycopg2
import json

files = {}
files['config'] = open('config.json','r')
files['words'] = open('words.json','r')

config = files['config'].read
config = json.loads(config)

words = files['words'].read
words = json.loads(words)

conn = psycopg2.connect("host='%s' port='%s' database='%s' user='%s' password='%s'" %(config['host'],config['port'],config['database'],config['user'],config['password']))

def inputWord(db,word,callback=None):
    global config
    try:
        print('new word data: ')
        print(word)
        i = db.execute('SELECT * FROM public.kkutu_ko WHERE _id = %s', %(word.id))
        dbword = i[0]
        print('default word data: ')
        print(dbword)

        if not dbword
            thisOffset = 0
            OffsetSetting = True
            while OffsetSetting:
                if word['mean'].find('/mean') == -1:
                    OffsetSetting = False
                else:
                    thisOffset += 1
                    if word['mean'].find('/mean') == 0:
                        word['mean'] = '"' + str(thisOffset) + '"' + word['mean'][5:]
                    else:
                        word['mean'] = word['mean'][:word['mean'].find('/mean')] + '"' + str(thisOffset) + '"' + word['mean'][word['mean'].find('/mean') + 5:]

            db.execute('INSERT INTO public.kkutu_ko (_id, type, mean, flag, theme) VALUES (%s, %s, %s, %s, %s)', %(word.id, word.type, word.mean, word.flag, word.theme))
            if config['test']: print('INSERT INTO public.kkutu_ko (_id, type, mean, flag, theme) VALUES (' + word.id + ', ' +word.type + ', ' + word.mean + ', ' + word.flag + ', ' + word.theme + ')')
        else:
            themeOffset = dbword['theme'].count(',')
            thisOffset = 1
            OffsetSetting = True
            while OffsetSetting:
                if word['mean'].find('/mean') == -1:
                    OffsetSetting = False
                else:
                    thisOffset += 1
                    if word['mean'].find('/mean') == 0:
                        word['mean'] = '"' + str(themeOffset + thisOffset) + '"' + word['mean'][5:]
                    else:
                        word['mean'] = word['mean'][:word['mean'].find('/mean')] + '"' + str(themeOffset + thisOffset) + '"' + word['mean'][word['mean'].find('/mean') + 5:]
            print(dbword['mean'] != word['mean'])
            if (dbword['type'] != word['type']) or (dbword['mean'] != word['mean']) or (dbword['theme'] != word['theme']):
                db.execute('UPDATE public.kkutu_ko SET type=%s, mean=%s, theme=%s WHERE _id = %s' %(dbword['type'] + ',' + word['type'],dbword['mean'] + '  ' + word['mean'],dbword['theme'] + ',' + word['theme'],word['id']))
                if config['test']: print('UPDATE public.kkutu_ko SET type=' + dbword['type'] + ',' + word['type'] + ', mean=' + dbword['mean'] + '  ' + word['mean'] + ', theme=' + dbword['theme'] + ',' + word['theme'] + ' WHERE _id = ' + word['id'])
            else: print('same word. not update.')
        return
    except:
        return raise Exception

try:
    for word in words:
        inputWord(conn,word)
    print('success')
    i = db.execute('SELECT * FROM public.kkutu_ko WHERE _id = %s' %(word.id))
    print('inputed data: ')
    print(dbword)
except: print('Warning : Error!')