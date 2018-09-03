import psycopg2
import json

files = {}
files['config'] = open('config.json','r',1,'utf-8')
files['words'] = open('words.json','r',1,'utf-8')

config = files['config'].read()
config = json.loads(config)
config = config['sql']

words = files['words'].read()
words = json.loads(words)

conn = psycopg2.connect("host='%s' port='%s' dbname='%s' user='%s' password='%s'" %(config['host'],config['port'],config['database'],config['user'],config['password']))
cur = conn.cursor()

def inputWord(con,db,word,callback=None):
    global config
    con.commit()
    i,dbword = None, None
    # try:
    print('new word data: ')
    print(word)
    try:
        db.execute('SELECT * FROM public.kkutu_ko WHERE _id = \'%s\'' %(word['id']))
        i = db.fetchone()
        dbword = {"_id":i[0],"type":i[1],"mean":i[2],"hit":i[3],"flag":i[4],"theme":i[5]}
    except:
        dbword = False
    print('default word data: ')
    print(dbword)

    if not dbword:
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

        if word['mean'] == '':
            pass
        con.commit()
        db.execute('INSERT INTO public.kkutu_ko (_id, type, mean, flag, theme) VALUES (\'%s\', \'%s\', \'%s\', %s, \'%s\')' %(word['id'], word['type'], word['mean'], word['flag'], word['theme']))
        try:
            if config['test']: print('INSERT INTO public.kkutu_ko (_id, type, mean, flag, theme) VALUES (' + word['id'] + ', ' +word['type'] + ', ' + word['mean'] + ', ' + word['flag'] + ', ' + word['theme'] + ')')
        except KeyError:
            pass
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
        if (dbword['type'] != word['type']) or (dbword['theme'] != word['theme']):
            db.execute('UPDATE public.kkutu_ko SET type=\'%s\', mean=\'%s\', theme=\'%s\' WHERE _id = \'%s\'' %(dbword['type'] + ',' + word['type'],dbword['mean'] + '  ' + word['mean'],dbword['theme'] + ',' + word['theme'],word['id']))
            try:
                if config['test']: print('UPDATE public.kkutu_ko SET type=' + dbword['type'] + ',' + word['type'] + ', mean=' + dbword['mean'] + '  ' + word['mean'] + ', theme=' + dbword['theme'] + ',' + word['theme'] + ' WHERE _id = ' + word['id'])
            except KeyError:
                pass
        else: print('same word. not update.')
    return
    # except:
    #     raise Exception

# try:
for word in words:
    inputWord(conn,cur,word)
    print('success')
    conn.commit()
    dbword = cur.execute('SELECT * FROM public.kkutu_ko WHERE _id = \'%s\'' %(word['id']))
    print('inputed data: ')
    print(dbword)
    conn.commit()
# except: print('Warning : Error!')