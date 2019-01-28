#include <ctime>
#include <string>
#include <iostream>

#define DEFAULT_NUM_OF_THREADS 1

using namespace std;

class MyTimer{
  static time_t begin;
public:
  static void start();
  static int stop();
};

int getNumOfThreads();