#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <ctime>
#include <sstream>
#include <fcntl.h>
using namespace std;


const int MAXN = 10000000;
const int MAXS = 60 * 1024 * 1024;

float numbers[MAXN];
char buf[MAXS];

void test2()
{
	string filename = "./data/train_data.txt";
	fstream infile(filename);
	char buffer[65536];
	infile.rdbuf()->pubsetbuf(buffer, sizeof(buffer));
	string line;
	vector<string> splittedString;
	while (getline(infile, line)) {
		splittedString.clear();
		size_t last = 0, pos = 0;
		while ((pos = line.find(',', last)) != std::string::npos) {
			splittedString.emplace_back(line, last, pos - last);
			last = pos + 1;
		}
		if (last)
			splittedString.emplace_back(line, last);
		float a = stoi(splittedString[0]);
		cout<<'a'<<a<<endl;
		// I do some processing like this before some manipulation and calculations with the data
	}
}


void analyse(char *buf, int len = MAXS)
{
	string line,tmp;
	stringstream fin(buf);
	char ch;
	float dataV;
	int i,j;
	vector<float> feature;
// 	i = 0;
// 	//cout << "what is line "<<line << endl;

	//
	// cout<<buf<<endl;
	// getline(sin,line);
	// cout<<line<<endl;
	// cout<<"another"<<endl;
	// getline(sin,line);
	// cout<<line<<endl;
	i=0;
	j=0;
	feature.reserve(8000*10001);
	while (getline(fin,line)){
		istringstream sin(line);
		while (getline(sin,tmp,','))
		{
			feature.push_back(stof(tmp));
			/* code */
		}
		
	}
	cout<<"j"<<j<<endl;





//strtok solution  1.76s
	// const char *d = ",";
	// char *p;
	// p =strtok(buf, d);
	// feature.reserve(9000 * 1001);
	// while (p != NULL)
	// {	feature.push_back(stof(p));
	// 	p = strtok(NULL, d);
		
	// 	// cout << "p's " << p << endl;
		
	// }
	// cout << feature.size() << endl;

// internet  solution  1.74

	// for (char *p = buf; *p && p - buf < len; p++)
	// 	if (*p == ',') {
	// 		numbers[i] = stof(tmp);
	// 		/*numbers[++i] = 0;*/
	// 		tmp = "";
	// 	}
	// 	else {
	// 		tmp = tmp + *p;

	// 	}
// solution 2 


	// numbers[i=0]=0;
	// for (char *p=buf;*p && p-buf<len;p++)
	// if (*p == ','){
	// 	// numbers[i]=stof(tmp);
	// 	// numbers[i]=1.2;

	// 	// cout<<numbers[i]<<endl;
	// 	tmp = "";
	// 	i++;
	// 	// numbers[++i]=0;
	// }
	// else{
	// 	// cout<<"what is *p"<<*p<<endl;
	// 	tmp = tmp + *p;
	// 	// i++;

	// }

// mmp solution 



//
//
	// int t; char ch;
	// vector<float> arr;
	// bool status;
	

// data stream solution   time is  1.73571 seconds
   
    // feature.reserve(10000*1000);
    // while (sin) {
    //             sin >> dataV;
    //             // feature.push_back(dataV);
    //             sin >> ch;

    // }


//  getline solution
	// feature.reserve(9000*1001); //预留存储空间
	// ifstream infile(buf);


    // while (infile) {
    //     getline(infile, line);
	// 	ifstream sin(line);

	// 	while (getline(sin, tmp, ',')) { 

	// 		cout << tmp << endl;
	// 		feature.push_back(stof(tmp)); 
	// 	}
	// 	i++;
	// }


//	//arr.push_back(1.232);
//	//arr.push_back(1.444);
//
//	cout << arr[0] << endl;
//	cout << arr[1] << endl;
	
}

//	cout << "data" << numbers[i] << endl;


void fread_analyse()
{
	freopen("./data/train_data.txt","r",stdin);
	// freopen("data.txt", "r", stdin);
	int len = fread(buf, 1, MAXS, stdin);
	cout << "len" << len << endl;

	// cout <<"this is buff  "<<buf << endl;
	//buf[len] = '\0';
	analyse(buf, len);
}

void test(){

	string line,tmp;
	char ch;
	float dataV;
	int i=0;
	vector<float> feature;
	

	ifstream infile("train_data.txt");
    // string line;
	feature.reserve(9000*1001); //预留存储空间
    while (infile) {
        getline(infile, line);
		ifstream sin(line);
		while (getline(sin, tmp, ',')) { 
			cout << tmp << endl;
			feature.push_back(stof(tmp)); 
		}
		i++;
	}
	cout << "this is a new one "<<endl;
	cout<<i<<endl;
}



int main()
{

	int start = clock();
	//DO SOMETHING
	
	cout << "this is new" << endl;
	//fread_analyse();
	//test();
	test2();
	cout << "this is new  2222" << endl;

	cout<<" the time cost is"<<(" %.3lf\n", double(clock() - start) / CLOCKS_PER_SEC);
	return 0;


}