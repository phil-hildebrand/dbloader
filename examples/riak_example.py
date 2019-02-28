from dbloader import dbloader as dbl
import time

dbl.setup_logs('./dbloader.log', False)
ldr = dbl.r.RiakLoader()
ldr.protocol = 'http'
ldr.host = '192.168.2.11'
ldr.port = 8098
ldr.inserts = 50
ldr.deletes = 2
ldr.updates = 2
ldr.selects = 2
ldr.concurrency = 5
ldr.itterations = 5
ldr.buckets = ['rb_1', 'rb_2']
inserted = ldr.insert_some()
deleted = ldr.delete_some()
dbl.logger.info("Inserted %d records in %4.3f sec for an avg insert time of %4.2f" % (len(inserted),
                                                                                      sum(inserted),
                                                                                      sum(inserted) / len(inserted)))
dbl.logger.info("Deleted %d record in %4.3f secs for an avg delete time of %4.2f" % ( len(deleted),
                                                                                      sum(inserted),
                                                                                      sum(deleted) / len(deleted)))
x = time.time()
inserted, deleted, updated, selected = ldr.load_run()
y = time.time()
dbl.logger.info("Total Run Time: %4.3f" % (y-x))

dbl.logger.info("Run: Inserted %d record in %4.3f secs for an avg insert time of %4.2f" % (len(inserted),
                                                                                      sum(inserted),
                                                                                      sum(inserted) / len(inserted)))
dbl.logger.info("Run: Deleted %d record in %4.3f secs for an avg deleted time of %4.2f" % (len(deleted), 
                                                                                      sum(inserted),
                                                                                      sum(deleted) / len(deleted)))
dbl.logger.info("Run: Updated %d record in %4.3f secs for an avg updated time of %4.2f" % (len(updated), 
                                                                                      sum(inserted),
                                                                                      sum(updated) / len(updated)))
dbl.logger.info("Run: Selected %d record in %4.3f secs for an avg selected time of %4.2f" % (len(selected), 
                                                                                      sum(inserted),
                                                                                      sum(selected) / len(selected)))
