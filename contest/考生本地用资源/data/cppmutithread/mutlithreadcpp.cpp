#include <iostream>

#include <thread>
#include <string>
#include <vector>
#include <sstream>
#include <fstream>
using namespace std;
thread::id main_thread_id = this_thread::get_id();

void hello(string *line) 
{

    vector<double>feature;
    string tmp;
   istringstream sin(*line);
//    cout<<"This is run this1"<<endl;
    while (getline(sin, tmp, ',')) { 
        // cout<<tmp<<endl;
        feature.push_back(stod(tmp)); 
    }

}
void hello2(string *line)  
{
    cout<<"we have run this2"<<endl;

  vector<double>feature;
    string tmp;
   istringstream sin(*line);
        while (getline(sin, tmp, ',')) { 
            cout<<tmp<<endl;
			feature.push_back(stod(tmp)); 
		}

}

void pause_thread(int n) {
    this_thread::sleep_for(chrono::seconds(n));
    cout << "pause of " << n << " seconds ended\n";
}

int main() {
    // char name[] = "./data/data_train_data.txt";
    ifstream infile("./data/train_data.txt");
    // ifstream infile("mydata.txt");

    string line1,line2,line3,line4,tmp,line;
    // char line[]="";
    int i = 0;
	vector<double> feature;
    int start=clock();
	
 
    cout<<"we are here1"<<endl;

    // string line;
	// feature.reserve(1001); //预留存储空间
    while (infile) {
        // cout<<"leixing"<< typeid(line).name()<<endl; 
        // if (line.size()==0){
        //     break;
        // }
        // feature.clear();

        //solution one 
        getline(infile, line1);
        thread t1(hello,&line1);
        // getline(infile, line2);
        // thread t2(hello,&line2);
        // getline(infile, line3);
        // thread t3(hello,&line3);
        // getline(infile, line4);
        // thread t4(hello,&line4);

        t1.join();
        // t2.join();
        // t3.join();
        // t4.join();


        //solution 2

		// getline(infile, line);

        // // if (i==1) {
        // //     i = 0 ;
        // //     continue;
        // // }
        // // else{ i = i + 1;

        // // }
            
        // if (line.size()==0){
        //     break;
        // }
        // feature.clear();
		// istringstream sin(line);
        // while (getline(sin, tmp, ',')) { 
		// 	feature.push_back(stod(tmp)); 
		// }


        //solution 3 截取字符串方案



        // int ftf;
        // ftf = (int)feature.back();
        // feature.pop_back();
        // trainDataSet.push_back(Data(feature, ftf));
    }
    infile.close();
    // cout<<"load lines"<<trainDataSet.size()<<endl;
    
    // return true;
    // thread t(hello);
    // thread t1(hello2);

    // t.join();
    // t1.join();
	cout<<" the time cost is"<<(" %.3lf\n", double(clock() - start) / CLOCKS_PER_SEC);

    return 0;
    
}
// #include <iostream>
// #include <thread>
 
// void foo(const int  &x,char *mychar)
// {
// 	std::cout << &x << "   " << &mychar << std::endl;
// 	std::cout << "正在运行的线程为：" << std::this_thread::get_id() << "线程的参数为： " << x <<"  "<<mychar<< std::endl;
// 	return;
// }
 
// int main()
// {
// 	std::cout << "主线程的线程id为： " << std::this_thread::get_id() << std::endl;
	
// 	int x = 1;
// 	char mybuff[] = "./data/train_data.txt";
// 	std::cout << &x << "   " << &mybuff << std::endl;
// 	std::thread second(foo, x, mybuff);
// 	second.join();
 
// 	std::cout << "主线程运行结束" << std::endl;
// 	return 0;
// }