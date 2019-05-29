import sqlite3

conn = sqlite3.connect('catalog.db')
c = conn.cursor()

UserEntries = [
    ('Hyatt Whe','hy@inc.info',''),
    ('Anke Umst','ankut@arr.info',''),
    ('Cairistiona Heu','cairistione@autoc.info',''),
    ('Claudine Saff','claudf@aunc.info',''),
    ('Tony Her','tony@eglc.info',''),
    ('Karima Blou','karn@diak.com',''),
    ('Jamilah He','jamheue@autoz.info',''),
    ('Saudeep He','saude@eglnc.info',''),
    ('Nettie He','netti@egnc.info',''),
]

CatalogItemEntries = [
    ('Surfboard','Surfboarding','','netti@egnc.info','1'),
    ('Ice Skates','Winter Sports','','netti@egnc.info','2'),
    ('Snowboard','Winter Sports','','saude@eglnc.info','3'),
    ('Basketball','Basketball','','saude@eglnc.info','4'),
    ('Goggles','Scuba','','tony@eglc.info','5'),
    ('Air Tanks','Scuba','','tony@eglc.info','6'),
]

c.executemany('insert into users values(?,?,?)',UserEntries)
c.executemany('insert into catalog_items values(?,?,?,?,?)',CatalogItemEntries)
conn.commit()

print('Database entries entered\nCurrent Database:\n\nUsers:')
for row in c.execute('select * from users'):
    print(row)

print('\n\nCatalog Items:')
for row in c.execute('select * from catalog_items'):
    print(row)
