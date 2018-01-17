import sys
sys.path.insert(0, "./loader")
import loader as l

ldr = l.Loader()
ldr.host = 'mine'
ldr.inserts = 50
ldr.deletes = 2
ldr.concurrency = 30
ldr.port = 3306
dbs = ['db1','db2']
tables = ['tab1','tab2']
inserted = ldr.insert_some(dbs,tables)
deleted = ldr.delete_some(dbs,tables)
print ("Inserted %d records for an avg insert time of %4.2f" % ( len(inserted), sum(inserted) / len(inserted)))
print ("Deleted %d records for an avg delete time of %4.2f" % ( len(deleted), sum(deleted) / len(deleted)))
inserted, deleted = ldr.load_run(dbs,tables, 5)
for run in inserted:
    print ("Run: Inserted %d records for an avg insert time of %4.2f" % ( len(run), sum(run) / len(run)))
for run in deleted:
    print ("Run: Deleted %d records for an avg deleted time of %4.2f" % ( len(run), sum(run) / len(run)))
