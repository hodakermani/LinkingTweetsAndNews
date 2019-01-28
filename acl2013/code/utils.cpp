#include "utils.hpp"


time_t MyTimer::begin = 0;

void MyTimer::start(){
  begin = time(NULL);
}

int MyTimer::stop(){
  int end = time(NULL);
  int usedTime = difftime(end, begin);
  return usedTime;
}

int getNumOfThreads(){
	int num_of_threads = DEFAULT_NUM_OF_THREADS;
	if(getenv("NUM_OF_THREADS") != NULL)
		num_of_threads = stoi(getenv("NUM_OF_THREADS"));
	return num_of_threads;
}