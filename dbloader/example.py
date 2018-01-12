import sys
sys.path.insert(0, "./loader")
import loader as l

l.host = 'mine'
l.inserts = 50
l.deletes = 2
l.concurrency = 30
l.port = 3306
dbs = ['db1','db2']
tables = ['tab1','tab2']
inserted = l.Loader().insert_some(dbs,tables)
deleted = l.Loader().delete_some(dbs,tables)
print ("Inserted %d records for an avg insert time of %4.2f" % ( len(inserted), sum(inserted) / len(inserted)))
print ("Deleted %d records for an avg delete time of %4.2f" % ( len(deleted), sum(deleted) / len(deleted)))
inserted, deleted = l.Loader().load_run(dbs,tables, 5)
for run in inserted:
    print ("Run: Inserted %d records for an avg insert time of %4.2f" % ( len(run), sum(run) / len(run)))
for run in deleted:
    print ("Run: Deleted %d records for an avg deleted time of %4.2f" % ( len(run), sum(run) / len(run)))
