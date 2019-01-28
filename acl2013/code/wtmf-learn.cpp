#include "wtmf-learn.hpp"
#include "pre_calcs.hpp"
#include "utils.hpp"
#include <thread>
#include <string>
using namespace std;
/*
 * Perform all rank. 
 */
void calculate_qq(wtmf_corpus *corpus, wtmf_model *model, PreCalcs* preCalcs){
  int no_sents = corpus->sent_data.cols();
  Mat<double> ppte = preCalcs->ppte;
  Mat<double> lambdaI = preCalcs->lambdaI;
  Mat<double>* pvs = preCalcs->pvs;
  Mat<double>* pvElemMults = preCalcs->pvElemMults;
  Vec<double>* pwxs = preCalcs->pwxs;
  Vec<double> qj;
  for (int j = 0; j < no_sents; j++) {
    if (corpus->r4s[j].size() == 0) 
    {
      model->q.set_col(j, zeros(model->dim));
      continue;
    }
    Mat<double> pv = preCalcs->pvs[j];
    if (corpus->syn.cols() == 0 || model->delta == 0) 
    {
      model->q.set_col(j, preCalcs->qjsFirstCase[j]);
      continue;
    }

    Mat<double> qnv = model->q.get_cols(corpus->syn.get_col(j).get_nz_indices()); // vectors of neighbors
    Vec<double> values = preCalcs->qlen->get(corpus->syn.get_col(j).get_nz_indices()) * ((*preCalcs->qlen)(j)); // the product of reciprocal length of neighbor vector and current vector
    
    if (qnv.cols() == 0) 
    {
      model->q.set_col(j, preCalcs->qjsFirstCase[j]);
    } else {
      model->q.set_col(j, 
        inv(ppte + 
          preCalcs->pvElemMults[j]
           + model->delta*qnv*qnv.transpose() 
           + model->lambda*eye(model->dim))  *  
            (pv*elem_mult(corpus->r4s[j],corpus->w4s[j]) + model->delta*qnv*values)
        );
    }
    ((*preCalcs->qlen)(j)) = 1/sqrt(sum_sqr(model->q.get_col(j)));
  }
}

void calculate_q(wtmf_corpus &corpus, wtmf_model &model, Vec<double>* qlen){
  int no_sents = corpus.sent_data.cols();
  PreCalcs* preCalcs = new PreCalcs;
  preCalcs->qlen = qlen;

  MyTimer::start();
  do_pre_calculate_q(corpus, model, preCalcs, no_sents);
  cout<<"Q Pre Calculation Time: "<<MyTimer::stop()<<endl;
  cout<<"Pre Q calculation done!"<<endl;

  MyTimer::start();
  calculate_qq(&corpus,&model,preCalcs);
  cout<<"Q Calculation Time: "<<MyTimer::stop()<<endl;

  cleanup(preCalcs);
  cout<<"Q calculation done!"<<endl;
}

void calculate_pp(wtmf_corpus *corpus, wtmf_model *model, int s, int e){
  cout<<"PT started starting from: "<<s<<endl;
  Mat<double> qqte = model->q * model->q.transpose() * model->wm;
  for (int i = s; i < e; i++) 
  {
    if (corpus->r4w[i].size() == 0) 
    {
      model->p.set_col(i, zeros(model->dim));
      continue;
    }
    Mat<double> qv = model->q.get_cols(corpus->word_data.get_col(i).get_nz_indices());
    model->p.set_col(i, inv(qqte + qv * elem_mult(repmat(corpus->w4w[i],1,model->dim)-model->wm,qv.transpose()) + model->lambda*eye(model->dim))  *  qv * elem_mult(corpus->r4w[i],corpus->w4w[i]));
  } 
}
void calculate_p(wtmf_corpus &corpus, wtmf_model &model){
  int no_words = corpus.sent_data.rows();
  vector<thread*> threads;
  int num_of_threads = getNumOfThreads();
  cout<<"Num Of Threads: "<<num_of_threads<<endl;
  int unit = no_words/num_of_threads;
  int i;
  for(i = 0; i < num_of_threads - 1; i++){
    int s = i * unit;
    int e = (i+1)*unit;
    threads.push_back(new thread(calculate_pp,&corpus,&model,s,e));
  }
  threads.push_back(new thread(calculate_pp,&corpus,&model,i*unit,no_words));
  for(int i = 0; i < threads.size(); i++){
    threads[i]->join();
    cout<<"PT"<<i<<" joined!"<<endl;
  }
  cout<<"P calculation done!"<<endl;
}

void wtmf_estimate(wtmf_corpus &corpus, wtmf_model &model, int maxiter) {
  int no_words = corpus.sent_data.rows();
  int no_sents = corpus.sent_data.cols();

  cout << "[wtmf-learn.cpp wtmf_estimate()]: model: dim=" << model.dim << " lambda=" << model.lambda << " wm=" << model.wm << " delta=" << model.delta << endl;
  cout << "[wtmf-learn.cpp wtmf_estimate()]: corpus: no_words=" << no_words << " no_sents=" << no_sents << endl;

  // reciprocal length of model.p
  //Vec<double> qlen = elem_div(1.0, sqrt(sum_sqr(model.q)));
  Vec<double> qlen = 1.0 / sqrt(sum_sqr(model.q));

  /* 2. iteration */
  for (int iter = 0; iter < maxiter; iter++) {
    /* 2.1 calculating p... */
    cout << "[wtmf-learn.cpp wtmf_estimate()]: iteration=" << iter << endl;
    cout << "[wtmf-learn.cpp wtmf_estimate()]: calculating p..." << endl;
    MyTimer::start();
    calculate_p(corpus, model);
    cout<<"P Calculation Time: "<<MyTimer::stop()<<endl;

    /* 2.2 calculating q... */
    cout << "[wtmf_learn.cpp wtmf_estimate()]: calculating q..." << endl;
    calculate_q(corpus, model, &qlen);
  }
}



void wtmf_inference(wtmf_corpus &corpus, wtmf_model &model, Mat<double> &q) {
  cout << "[wtmf-learn.cpp wtmf_inference()]: entries=" << corpus.sent_data.cols() << endl;
  Mat<double> ppte;
  ppte = model.p * model.p.transpose() * model.wm;
  q.set_size(model.dim, corpus.sent_data.cols());
  
  for (int i = 0; i < corpus.sent_data.cols(); i++) {
    if (corpus.sent_data.get_col(i).nnz() == 0) {
      q.set_col(i, zeros(model.dim));
      continue;
    }
    Mat<double> pv = model.p.get_cols(corpus.sent_data.get_col(i).get_nz_indices());
    q.set_col(i, inv(ppte + pv * elem_mult(repmat(corpus.w4s[i],1,model.dim)-model.wm,pv.transpose()) + model.lambda*eye(model.dim))  *  pv * elem_mult(corpus.r4s[i],corpus.w4s[i]));
  }
}
