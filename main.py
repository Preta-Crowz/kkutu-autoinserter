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
        print('default word data: ')
        print(i[0])

        if not i[0]
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
            themeOffset = i[0]['theme'].count(',')
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
            print(i[0]['mean'] != word['mean'])
            if (i[0]['type'] != word['type']) or (i[0]['mean'] != word['mean']) or (i[0]['theme'] != word['theme']):
                db.execute('UPDATE public.kkutu_ko SET type=%s, mean=%s, theme=%s WHERE _id = %s' %(i[0]['type'] + ',' + word['type'],i[0]['mean'] + '  ' + word['mean'],i[0]['theme'] + ',' + word['theme'],word['id']))
                if config['test']: print('UPDATE public.kkutu_ko SET type=' + i[0]['type'] + ',' + word['type'] + ', mean=' + i[0]['mean'] + '  ' + word['mean'] + ', theme=' + i[0]['theme'] + ',' + word['theme'] + ' WHERE _id = ' + word['id'])
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
    print(i[0])
except: print('Warning : Error!')