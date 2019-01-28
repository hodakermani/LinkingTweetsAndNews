#include "wtmf-learn.hpp"
#include <thread>
#include <vector>

struct PreCalcs {
  Mat<double> ppte;
  Mat<double> lambdaI;
  Vec<double>* qlen;
  Mat<double> lastPv;
  Mat<double>* pvs;
  Vec<double>* qjsFirstCase;
  Vec<double>* pwxs;
  Mat<double>* pvElemMults;
};

void pre_pre_calculate_q(wtmf_corpus *corpus, wtmf_model *model, PreCalcs* preCalcs);
void pre_calculate_q(wtmf_corpus *corpus, wtmf_model *model, PreCalcs* preCalcs, int s, int e);
void do_pre_calculate_q(wtmf_corpus &corpus, wtmf_model &model, PreCalcs* preCalcs, int no_sents);
void cleanup(PreCalcs* preCalcs);