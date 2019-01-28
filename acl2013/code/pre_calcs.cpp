#include "utils.hpp"
#include "pre_calcs.hpp"

void pre_pre_calculate_q(wtmf_corpus *corpus, wtmf_model *model, PreCalcs* preCalcs){
  int no_sents = corpus->sent_data.cols();
  preCalcs->ppte = model->p * model->p.transpose() * model->wm;
  preCalcs->lambdaI = model->lambda*eye(model->dim);
  preCalcs->pvs = new Mat<double>[no_sents];
  preCalcs->qjsFirstCase = new Vec<double>[no_sents];
  preCalcs->pvElemMults = new Mat<double>[no_sents];
  preCalcs->pwxs = new Vec<double>[no_sents];
  cout<<"Q Pre Pre Calculation done!"<<endl;
}

void cleanup(PreCalcs* preCalcs){
  delete[] preCalcs->pvs;
  delete[] preCalcs->qjsFirstCase;
  delete[] preCalcs->pwxs;
  delete[] preCalcs->pvElemMults;
}

void pre_calculate_q(wtmf_corpus *corpus, wtmf_model *model, PreCalcs* preCalcs, int s, int e)
{
  cout<<"QPCT started from: "<<s<<endl;
  int no_sents = corpus->sent_data.cols();
  Vec<double>* pwxs = preCalcs->pwxs;
  for(int j = s; j < e; j++){
    if (corpus->r4s[j].size() == 0)
      continue;
    preCalcs->pvs[j] = model->p.get_cols(corpus->sent_data.get_col(j).get_nz_indices());
    preCalcs->pvElemMults[j] = preCalcs->pvs[j] * elem_mult(repmat(corpus->w4s[j],1,model->dim)-model->wm,preCalcs->pvs[j].transpose());
    preCalcs->qjsFirstCase[j] = inv(preCalcs->ppte + preCalcs->pvElemMults[j] + preCalcs->lambdaI)
     * preCalcs->pvs[j] * elem_mult(corpus->r4s[j],corpus->w4s[j]);
    if (corpus->syn.cols() == 0 || model->delta == 0) {   
      continue;
    }
    preCalcs->pwxs[j] = preCalcs->pvs[j]*elem_mult(corpus->r4s[j],corpus->w4s[j]); // PWjXTj;
  }
}

void do_pre_calculate_q(wtmf_corpus &corpus, wtmf_model &model, PreCalcs* preCalcs, int no_sents){
  pre_pre_calculate_q(&corpus, &model, preCalcs);
  vector<thread*> threads;
  int num_of_threads = getNumOfThreads();
  cout<<"Num Of Threads: "<<num_of_threads<<endl;
  int unit = no_sents/num_of_threads;
  int i;
  for(i = 0; i < num_of_threads - 1; i++){
    int s = i * unit;
    int e = (i+1)*unit;
    threads.push_back(new thread(pre_calculate_q,&corpus,&model, preCalcs,s,e));
  }
  threads.push_back(new thread(pre_calculate_q,&corpus,&model, preCalcs,i*unit,no_sents));
  for(int i = 0; i < threads.size(); i++){
    threads[i]->join();
    cout<<"QPCT"<<i<<" joined!"<<endl;
  }
}