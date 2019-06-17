from dbloader import dbloader as dbl
import time

dbl.setup_logs('./dbloader.log', True)
# options = dbl.load_config('./etc/load.yml')
options = dbl.load_config('./riak_load.yml')
if not options:
    exit(1)
for server in options['server']:
    if server['type'] == 'riak':
        ldr = dbl.r.RiakLoader(server['protocol'], server['name'], server['port'])
        dbl.logger.info(server['protocol'])
        dbl.logger.info(server['name'])
        dbl.logger.info(server['port'])
        ldr.databases = ['rb_1', 'rb_2', 'rb_3']
        ldr.tables = []
        ldr.string_size = server.get('string_size', 250)
        ldr.inserts = server.get('inserts', 50)
        ldr.deletes = server.get('deletes', 5)
        ldr.updates = server.get('updates', 5)
        ldr.selects = server.get('selects', 5)
        ldr.concurrency = server.get('concurrency', 5)
        ldr.itterations = server.get('itterations', 5)
        custom = server.get('itterations', None)
        dbl.main(server['type'], ldr, custom)
inserted = ldr.insert_some()
deleted = ldr.delete_some()
dbl.logger.info("Inserted %d records in %4.3f sec for an avg insert time of %4.2f" % (len(inserted),
                                                                                      sum(inserted),
                                                                                      sum(inserted) / max(1, len(inserted))))
dbl.logger.info("Deleted %d record in %4.3f secs for an avg delete time of %4.2f" % ( len(deleted),
                                                                                      sum(inserted),
                                                                                      sum(deleted) / max(1, len(deleted))))
x = time.time()
inserted, deleted, updated, selected = ldr.load_run()
y = time.time()
dbl.logger.info("Total Run Time: %4.3f" % (y-x))

dbl.logger.info("Run: Inserted %d record in %4.3f secs for an avg insert time of %4.2f" % (len(inserted),
                                                                                      sum(inserted),
                                                                                      sum(inserted) / max(1, len(inserted))))
dbl.logger.info("Run: Deleted %d record in %4.3f secs for an avg deleted time of %4.2f" % (len(deleted), 
                                                                                      sum(inserted),
                                                                                      sum(deleted) / max(1, len(deleted))))
dbl.logger.info("Run: Updated %d record in %4.3f secs for an avg updated time of %4.2f" % (len(updated), 
                                                                                      sum(inserted),
                                                                                      sum(updated) / max(1, len(updated))))
dbl.logger.info("Run: Selected %d record in %4.3f secs for an avg selected time of %4.2f" % (len(selected), 
                                                                                      sum(inserted),
                                                                                      sum(selected) / max(1,len(selected))))
truncated = ldr.delete_all()
dbl.logger.info("Cleanup: Truncated %d records" % sum(truncated))
