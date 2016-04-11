import logging, sys, os

class state(object):
    def __init__(self, algo_name, rates, out, log_level, num_slices, num_recs, num_users=0):
        self.name = algo_name
        self._rates = rates
        self.log_level = log_level
        self.out = out
        self.num_slices = num_slices
        self.num_recs = num_recs
        self.num_users = num_users
        self.cur_slice = 0
        # Keep in mind that this is going to delete whatever was in this
        # file string before.
        os.remove("./out/" + out)
        logging.basicConfig(filename="./out/" + out, format="%(message)s", level=logging.INFO)
        self.logger = logging.getLogger('State')
        if(self.num_users == 0):
            self.logger.info("%s\nAlgo:%s\t Num_slices:%d\t Num_recs: %d\t" % \
                ('-'*100, self.name, self.num_slices, self.num_recs))
        else:
            self.logger.info("%s\nAlgo:%s\t Num_slices:%d\t Num_recs: %d\t Num_users: %d\t" % \
                ('-'*100, self.name, self.num_slices, self.num_recs, self.num_users))

    def __str__(self):
        return "%s\nAlgo:%s\t Iteration:%d\t Num_slices:%d\t Num_recs: %d\t Overall Success: %f\t\n%s" % \
            ('-'*100, self.name, len(self._rates), self.num_slices, self.num_recs, self.calRate(), "-"*100)

    def term(self):
        if(self.num_users == 0):
            self.logger.info('%s\nFINAL: \nALGO: %s\nOVERALL_SUCCESS_RATE: %f\nNUM_SLICES: %d\nNUM_RECS: %d\n%s' % \
                ('-'*100, self.name, self.calRate(), self.num_slices, self.num_recs, '-'*100))
        else:
            self.logger.info('%s\nFINAL: \nALGO: %s\nOVERALL_SUCCESS_RATE: %f\nNUM_SLICES: %d\nNUM_RECS: %d\nNUM_USERS: %d\n%s' % \
                ('-'*100, self.name, self.calRate(), self.num_slices, self.num_recs, self.num_users, '-'*100))

    def calRate(self):
        aggregator_total = 0
        aggregator_success = 0
        for success,total in self._rates:
          # print "success: " + str(success) + " total: " + str(total)
          aggregator_success += float(success)
          aggregator_total += float(total)
        overall_success_rate = aggregator_success/aggregator_total
        # print "overall success rate: ", overall_success_rate
        return overall_success_rate

    @property
    def rates(self):
      return self._rates
    @rates.setter
    def rates(self, val):
      print(val)
      self._rates.append(val)
      self.logger.info("Slice:%d\tSuccess:%d\tTotal:%d\tRate:%f" % \
      (self.cur_slice, val[0], val[1], float(val[0])/float(val[1])))
