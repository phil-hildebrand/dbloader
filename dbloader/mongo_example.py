import sys
sys.path.insert(0, "./mongo")
import mongo_loader as m

ldr = m.mongoLoader()
ldr.host = 'localhost'
ldr.port = 27017
ldr.inserts = 50
ldr.deletes = 2
ldr.concurrency = 5
ldr.itterations = 5
inserted = ldr.insert_some()
deleted = ldr.delete_some()
print ("Inserted %d records for an avg insert time of %4.2f" % ( len(inserted), sum(inserted) / len(inserted)))
print ("Deleted %d records for an avg delete time of %4.2f" % ( len(deleted), sum(deleted) / len(deleted)))
inserted, deleted = ldr.load_run()
print ("Run: Inserted %d records for an avg insert time of %4.2f" % ( len(inserted), sum(inserted) / len(inserted)))
print ("Run: Deleted %d records for an avg deleted time of %4.2f" % ( len(deleted), sum(deleted) / len(deleted)))
