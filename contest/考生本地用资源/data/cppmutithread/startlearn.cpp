
#include <iostream>
#include <cstdlib>
#include <pthread.h>
#include <ctime>
 
using namespace std;
 
#define NUM_THREADS     2
 
void *PrintHello(void* id)
{  
   // 对传入的参数进行强制类型转换，由无类型指针变为整形数指针，然后再读取
//    int tid = *((int*)id);
    int *tid=(int*)id;
    int z=0;
    int start = clock();
    // *tid=*tid*10;
    for(int j=0;j<*tid;j++){
        z= z+1;
    } 
   cout << "Hello Runoob! 线程 ID, " <<*tid << "THis is the time cost:"<<(" %.3lf\n", double(clock() - start) / CLOCKS_PER_SEC)<<endl;
   pthread_exit(NULL);
}
 
int main ()
{
   pthread_t threads[NUM_THREADS];
   int indexes[NUM_THREADS];// 用数组来保存i的值
   int rc;
   int i;
    int start = clock();

    //solution one 
   for( i=0; i < NUM_THREADS; i++ ){      
      cout << "main() : 创建线程, " << i << endl;
      indexes[i] = 1000000000; //先保存i的值
      // 传入的时候必须强制转换为void* 类型，即无类型指针        
      rc = pthread_create(&threads[i], NULL, 
                          PrintHello,(void *)&indexes[i]); // 通过对内存操作的方案，对我们当前的系统的
      if (rc){
         cout << "Error:无法创建线程," << rc << endl;
         exit(-1);
      }
   }



   //solution two
//    int z=0;
//     for(int j=0;j<1000000000;j++){
//         z= z+1;
//     } 
//     z=0;
//       for(int j=0;j<1000000000;j++){
//         z= z+1;
//     }
//     z=0;

//       for(int j=0;j<1000000000;j++){
//         z= z+1;
//     } 
//     z=0;

//       for(int j=0;j<1000000000;j++){
//         z= z+1;
//     } 
//     z=0;

//       for(int j=0;j<1000000000;j++){
//         z= z+1;
//     } 








    cout<<" the  train time cost is"<<(" %.3lf\n", double(clock() - start) / CLOCKS_PER_SEC)<<endl;

   cout<<" "<<indexes[0]<<" "<<indexes[1]<<" "<<indexes[2]<<" "<<indexes[3]<<" "<<endl;
   pthread_exit(NULL);
}