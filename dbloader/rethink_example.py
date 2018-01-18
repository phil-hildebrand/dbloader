import dbloader as dbl

dbl.setup_logs('./dbloader.log', True)
ldr = dbl.rl.RethinkLoader()
ldr.host = 'localhost'
ldr.port = 28015
ldr.inserts = 50
ldr.deletes = 2
ldr.updates = 2
ldr.selects = 2
ldr.concurrency = 5
ldr.itterations = 5
ldr.databases = ['rt_db_1', 'rt_db_2']
ldr.tables = ['ltbl_1', 'ltbl_2']
ldr.insert_some()
ldr.conn = ldr.get_connection(ldr.host, ldr.port)
if ldr.create_if_not_exists(ldr.conn):
    inserted = ldr.insert_some()
    deleted = ldr.delete_some()
    dbl.logger.info("Inserted %d records in %4.3f sec for an avg insert time of %4.2f" % (len(inserted),
                                                                                      sum(inserted),
                                                                                      sum(inserted) / len(inserted)))
    dbl.logger.info("Deleted %d records in %4.3f sec for an avg delete time of %4.2f" % ( len(deleted),
                                                                                      sum(deleted),
                                                                                      sum(deleted) / len(deleted)))
    inserted, deleted, updated, selected = ldr.load_run()
    dbl.logger.info("Run: Inserted %d in %4.3f sec for an avg insert time of %4.2f" % (len(inserted),
                                                                                      sum(inserted),
                                                                                      sum(inserted) / len(inserted)))
    dbl.logger.info("Run: Deleted %d in %4.3f sec for an avg delete time of %4.2f" % (len(deleted),
                                                                                      sum(deleted),
                                                                                      sum(deleted) / len(deleted)))
    dbl.logger.info("Run: Updated %d in %4.3f sec for an avg update time of %4.2f" % (len(updated),
                                                                                      sum(updated),
                                                                                      sum(updated) / len(updated)))
    dbl.logger.info("Run: Selected %d in %4.3f sec for an avg select time of %4.2f" % (len(selected),
                                                                                      sum(selected),
                                                                                      sum(selected) / len(selected)))
else:
   dbl.logger.warning("Could not verify databases/tables")
