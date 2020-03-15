#include <iostream>
#include <vector>
#include <sstream>
#include <fstream>
#include <cmath>
#include <cstdlib>
#include <thread>
using namespace std;
// #define TESTs
struct Data {
    vector<float> features;
    int label;
    Data(vector<float> f, int l) : features(f), label(l)
    {}
};
struct Param {
    vector<float> wtSet;
};


class LR {
public:
    void train();
    void predict();
    int loadModel();
    int storeModel();
    LR(string trainFile, string testFile, string predictOutFile);

private:
    vector<Data> trainDataSet;
    vector<Data> testDataSet;
    vector<int> predictVec;
    Param param;
    string trainFile;
    string testFile;
    string predictOutFile;
    string weightParamFile = "modelweight.txt";

private:
    bool init();
    bool loadTrainData();
    bool loadTestData();
    int storePredict(vector<int> &predict);
    void initParam();
    float wxbCalc(const Data &data);
    float sigmoidCalc(const float wxb);
    float lossCal();
    static float gradientSlope(const vector<Data> &dataSet, int index, const vector<float> &sigmoidVec);
    
    bool loadTrainDatamulti();
    static void dataload(int step,vector<Data> *trainset,string *filename);
    static void wtCalmulti(Param *param,int start,int end,const vector<Data> *trainset,const vector<float> *sigmodVec);

    static void sigmoidVecCalmulti(vector<float> *sigmoidVectmp,int start,int end,const vector<Data> *trainset,Param *param);
    static float wxbCalcmulti(const Data &data,Param param);
    static float sigmoidCalcmulti(const float wxb);
private:
    int featuresNum;
    const float wtInitV = 1.0;
    static constexpr  float stepSize=0.035;
    const int maxIterTimes = 300;
    const float predictTrueThresh = 0.5;
    const int train_show_step = 10;
};
// float LR::ste

LR::LR(string trainF, string testF, string predictOutF)
{
    trainFile = trainF;
    testFile = testF;
    predictOutFile = predictOutF;
    featuresNum = 0;
    // stepSize = 0.035;
    init();
}

bool LR::loadTrainData()
{
    ifstream infile(trainFile.c_str());
    string line,tmp;
    int i = 0;
	vector<float> feature;
	
    if (!infile) {
        cout << "打开训练文件失败" << endl;
        exit(0);
    }
    cout<<"we are here1"<<endl;

    // string line;
	// feature.reserve(1001); //预留存储空间
    while (infile) {
        getline(infile, line);

        // if (i==1) {
        //     i = 0 ;
        //     continue;
        // }
        // else{ i = i + 1;

        // }
            
        if (line.size()==0){
            break;
        }
        feature.clear();
		istringstream sin(line);
        while (getline(sin, tmp, ',')) { 
			feature.push_back(stod(tmp)); 
		}
        int ftf;
        ftf = (int)feature.back();
        feature.pop_back();
        trainDataSet.push_back(Data(feature, ftf));
    }
    infile.close();
    cout<<"load lines"<<trainDataSet.size()<<endl;
    
    return true;
}
void LR::dataload(int step,vector<Data> *trainset,string *filename)
{
    ifstream infile(*filename);
    // ifstream infile("mydata.txt");
    // ifstream infile("./data/train_data1.txt");
    vector<float> feature;
    // vector<float>feature;
    string line,tmp;
    int nums=0;
    int start=clock();
    for(int i=1;i<step;i++){
        getline(infile, line);
    }

    while (infile) {

        getline(infile, line);
        // if (i==1) {
        //     i = 0 ;
        //     continue;
        // }
        // else{ i = i + 1;

        // }
            
        if (line.size()==0){
            break;
        }
        feature.clear();
		istringstream sin(line);
        while (getline(sin, tmp, ',')) { 
			feature.push_back(stod(tmp)); 
		}
        int ftf;
        ftf = (int)feature.back();
        feature.pop_back();
        (*trainset).push_back(Data(feature,ftf));
        getline(infile, line);
        getline(infile, line);
        getline(infile, line);
    }

}


bool LR::loadTrainDatamulti()
{
    vector<Data> trainDataSet1;
    vector<Data> trainDataSet2;
    vector<Data> trainDataSet3;
    thread t1(dataload,1,&trainDataSet,&trainFile);
    thread t2(dataload,2,&trainDataSet1,&trainFile);
    thread t3(dataload,3,&trainDataSet2,&trainFile);
    thread t4(dataload,4,&trainDataSet3,&trainFile);
    t1.join();
    t2.join();
    t3.join();
    t4.join();


    // cout<<"Trainset 1 "<<trainDataSet.size()<<endl;
    // cout<<"Trainset 2 "<<trainDataSet1.size()<<endl;
    // cout<<"Trainset 3 "<<trainDataSet2.size()<<endl;
    // cout<<"Trainset 4 "<<trainDataSet3.size()<<endl;

    trainDataSet.insert(trainDataSet.end(),trainDataSet1.begin(),trainDataSet1.end());
    trainDataSet.insert(trainDataSet.end(),trainDataSet2.begin(),trainDataSet2.end());
    trainDataSet.insert(trainDataSet.end(),trainDataSet3.begin(),trainDataSet3.end());

    // cout<<"this is main "<<trainDataSet.size()<<endl;
   




    return true;
}
void newload(){
    string trainFile = "train_data.txt";

    ifstream infile(trainFile);
    string line,tmp;
	vector<float> feature;
	
    if (!infile) {
        cout << "打开训练文件失败" << endl;
        exit(0);
    }


    // string line;
	feature.reserve(1001); //预留存储空间
    while (infile) {
        feature.clear();
        getline(infile, line);
		ifstream sin(line);
		while (getline(sin, tmp, ',')) { 
			//cout << tmp << endl;
			feature.push_back(stof(tmp)); 
		}
        int ftf;
        ftf = (int)feature.back();
        feature.pop_back();
        // trainDataSet.push_back(Data(feature, ftf));
        }
	

        
    
    infile.close();
    // return true;
}


void LR::initParam()
{
    int i;
    for (i = 0; i < featuresNum; i++) {
        param.wtSet.push_back(wtInitV);
    }
}

bool LR::init()
{
    trainDataSet.clear();
    // bool status = loadTrainData();
    bool status = loadTrainDatamulti();

    if (status != true) {
        return false;
    }
    featuresNum = trainDataSet[0].features.size();
    param.wtSet.clear();
    initParam();
    return true;
}


float LR::wxbCalc(const Data &data)
{
    float mulSum = 0.0L;
    int i;
    float wtv, feav;
    for (i = 0; i < param.wtSet.size(); i++) {
        wtv = param.wtSet[i];
        feav = data.features[i];
        mulSum += wtv * feav;
    }

    return mulSum;
}
float LR::wxbCalcmulti(const Data &data,Param param)
{
    float mulSum = 0.0L;
    int i;
    float wtv, feav;
    for (i = 0; i < param.wtSet.size(); i++) {
        wtv = param.wtSet[i];
        feav = data.features[i];
        mulSum += wtv * feav;
    }

    return mulSum;
}


inline float LR::sigmoidCalc(const float wxb)
{
    float expv = exp(-1 * wxb);
    float expvInv = 1 / (1 + expv);
    return expvInv;
}
inline float LR::sigmoidCalcmulti(const float wxb)
{
    float expv = exp(-1 * wxb);
    float expvInv = 1 / (1 + expv);
    return expvInv;
}


float LR::lossCal()
{
    float lossV = 0.0L;
    int i;
    // cout<<"we are in loss cal"<<endl;

    for (i = 0; i < trainDataSet.size(); i++) {
        lossV -= trainDataSet[i].label * log(sigmoidCalc(wxbCalc(trainDataSet[i])));
        lossV -= (1 - trainDataSet[i].label) * log(1 - sigmoidCalc(wxbCalc(trainDataSet[i])));
    }
    lossV /= trainDataSet.size();
    return lossV;
}


float LR::gradientSlope(const vector<Data> &dataSet, int index, const vector<float> &sigmoidVec)
{
    float gsV = 0.0L;
    int i;
    float sigv, label;
    for (i = 0; i < dataSet.size(); i++) {
        sigv = sigmoidVec[i];
        label = dataSet[i].label;
        gsV += (label - sigv) * (dataSet[i].features[index]);
    }

    gsV = gsV / dataSet.size();
    return gsV;
}
void LR::wtCalmulti(Param *param,int start,int end,const vector<Data> *trainset,const vector<float> *sigmodVec)
{
    // float stepsizeee=0.035;
    // cout<<"This is param's size "<<(*param).wtSet.size()<<endl;
    // (*param).wtSet[0]=1;
    for (int j = start; j < end; j++){
        (*param).wtSet[j] += stepSize * gradientSlope(*trainset, j, *sigmodVec);
    }

    // cout<<"we have receive start and end are"<<start<<" "<<end<<endl; 
    // cout<<"THis is thread in wtcal and index is:"<<endl;
}

void LR::sigmoidVecCalmulti(vector<float> *sigmoidVectmp,int start,int end,const vector<Data> *trainset,Param *param)
{
    float sigmoidVal;
    float wxbVal;


    for (int j = start; j < end; j++) {  //this j 是表示的是第几个数据 这个地方我们分配到多核去
            wxbVal = wxbCalcmulti((*trainset)[j],*param);
            sigmoidVal = sigmoidCalcmulti(wxbVal);
            (*sigmoidVectmp).push_back(sigmoidVal);
        }
}

void LR::train()
{
    float sigmoidVal;
    float wxbVal;
    int i, j;
    int start,end;
    int datalength=trainDataSet.size();

    for (i = 0; i < maxIterTimes; i++) {
        vector<float> sigmoidVec;
        vector<float> sigmoidVec1;
        vector<float> sigmoidVec2;
        vector<float> sigmoidVec3;


        ///////////////////////////////////////////////////////////
        //singal thread solution 
    //     for (j = 0; j < trainDataSet.size(); j++) {  //this j 是表示的是第几个数据 这个地方我们分配到多核去
    //         wxbVal = wxbCalc(trainDataSet[j]);
    //         sigmoidVal = sigmoidCalc(wxbVal);
    //         sigmoidVec.push_back(sigmoidVal);
    //     }
    //     //这个是更新每个theta的地方，这个地方也是可以分配的多核去，不受到到相同的其他的影响
    // //    single thread solution 
    //     for (j = 0; j < param.wtSet.size(); j++){
    //         param.wtSet[j] += stepSize * gradientSlope(trainDataSet, j, sigmoidVec);
    //     }










        //muti thread solution  
        start=0;
        end =int(datalength/4);
        thread w1(sigmoidVecCalmulti,&sigmoidVec,start,end,&trainDataSet,&param);
        start=end;
        end =int(datalength/2);
        thread w2(sigmoidVecCalmulti,&sigmoidVec1,start,end,&trainDataSet,&param);
        start=end;
        end =int(datalength*3/4);
        thread w3(sigmoidVecCalmulti,&sigmoidVec2,start,end,&trainDataSet,&param);
        start = end;
        end = datalength;
        thread w4(sigmoidVecCalmulti,&sigmoidVec3,start,end,&trainDataSet,&param);
        w1.join();
        w2.join();
        w3.join();
        w4.join();
        // cout<<"sigmoid vec 0  "<<sigmoidVec.size()<<endl;
        // cout<<"sigmoid vec 1  "<<sigmoidVec1.size()<<endl;
        // cout<<"sigmoid vec 2  "<<sigmoidVec2.size()<<endl;
        // cout<<"sigmoid vec 3  "<<sigmoidVec3.size()<<endl;
        sigmoidVec.insert(sigmoidVec.end(),sigmoidVec1.begin(),sigmoidVec1.end());
        sigmoidVec.insert(sigmoidVec.end(),sigmoidVec2.begin(),sigmoidVec2.end());
        sigmoidVec.insert(sigmoidVec.end(),sigmoidVec3.begin(),sigmoidVec3.end());
        // cout<<"This is whole sigmoid veclegnth:"<<sigmoidVec.size()<<endl;
        
       
         //////////////////////////////////////////////////////////

        //multi thread solution 
        start=0;
        end= 250;
        // cout<<"进程前是wt0 是多少："<<param.wtSet[0]<<endl;
        thread t(wtCalmulti,&param,start,end,&trainDataSet,&sigmoidVec);
        start=250;
        end= 500;
        thread t1(wtCalmulti,&param,start,end,&trainDataSet,&sigmoidVec);
        start=500;
        end= 750;
        thread t2(wtCalmulti,&param,start,end,&trainDataSet,&sigmoidVec);
        start=750;
        end= 1000;
        thread t3(wtCalmulti,&param,start,end,&trainDataSet,&sigmoidVec);
        t.join();
        t1.join();
        t2.join();
        t3.join();
        ///////////////////////////////////////////////////////////////////////////////////
        // cout<<"进程后是wt0 是多少："<<param.wtSet[0]<<endl;

        // if (i % train_show_step == 0) {
            // cout << "iter " << i << ". updated weight value is : "<<lossCal()<<endl;
            
        //     // for (j = 0; j < param.wtSet.size(); j++) {
        //     //     cout << param.wtSet[j] << "  ";
        //     // }
        // }
    }
}

void LR::predict()
{
    float sigVal;
    int predictVal;

    loadTestData();
    for (int j = 0; j < testDataSet.size(); j++) {
        sigVal = sigmoidCalc(wxbCalc(testDataSet[j]));
        predictVal = sigVal >= predictTrueThresh ? 1 : 0;
        predictVec.push_back(predictVal);
    }

    storePredict(predictVec);
}

int LR::loadModel()
{
    string line;
    int i;
    vector<float> wtTmp;
    float dbt;

    ifstream fin(weightParamFile.c_str());
    if (!fin) {
        cout << "打开模型参数文件失败" << endl;
        exit(0);
    }

    getline(fin, line);
    stringstream sin(line);
    for (i = 0; i < featuresNum; i++) {
        char c = sin.peek();
        if (c == -1) {
            cout << "模型参数数量少于特征数量，退出" << endl;
            return -1;
        }
        sin >> dbt;
        wtTmp.push_back(dbt);
    }
    param.wtSet.swap(wtTmp);
    fin.close();
    return 0;
}

int LR::storeModel()
{
    string line;
    int i;

    ofstream fout(weightParamFile.c_str());
    if (!fout.is_open()) {
        cout << "打开模型参数文件失败" << endl;
    }
    if (param.wtSet.size() < featuresNum) {
        cout << "wtSet size is " << param.wtSet.size() << endl;
    }
    for (i = 0; i < featuresNum; i++) {
        fout << param.wtSet[i] << " ";
    }
    fout.close();
    return 0;
}


bool LR::loadTestData()
{
    ifstream infile(testFile.c_str());
    string line,tmp;
    int i = 0;
	vector<float> feature;
	
    if (!infile) {
        cout << "打开训练文件失败" << endl;
        exit(0);
    }

    // string line;
	// feature.reserve(1001); //预留存储空间
    while (infile) {
        getline(infile, line);
        if (line.size()==0){
            break;
        }
        feature.clear();
		istringstream sin(line);
        while (getline(sin, tmp, ',')) { 
			feature.push_back(stod(tmp)); 
		}
        testDataSet.push_back(Data(feature, 0));
        i++;
    }
    // cout<<"we have load the test data file"<<" and load lines"<<testDataSet.size()<<" and the  i is "<< i <<endl;

    infile.close();
    return true;
}

bool loadAnswerData(string awFile, vector<int> &awVec)
{
    ifstream infile(awFile.c_str());
    if (!infile) {
        cout << "打开答案文件失败" << endl;
        exit(0);
    }
    while (infile) {
        string line;
        int aw;
        getline(infile, line);
        if (line.size() > 0) {
            stringstream sin(line);
            sin >> aw;
            awVec.push_back(aw);
        }
    }
    cout<<"we have load the answer file "<<"and the lines loading is "<< awVec.size()<<endl;

    infile.close();
    return true;
}

int LR::storePredict(vector<int> &predict)
{
    string line;
    int i;

    ofstream fout(predictOutFile.c_str());
    if (!fout.is_open()) {
        cout << "打开预测结果文件失败" << endl;
    }
    for (i = 0; i < predict.size(); i++) {
        fout << predict[i] << endl;
    }
    fout.close();
    return 0;
}

int main(int argc, char *argv[])
{
    vector<int> answerVec;
    vector<int> predictVec;
    int correctCount;
    float accurate;
//cloud

    string trainFile = "/data/train_data.txt";
    string testFile = "/data/test_data.txt";
    string predictFile = "/projects/student/result.txt";

    string answerFile = "/projects/student/answer.txt";

//local 
    // string trainFile = "./data/train_data.txt";
    // // string trainFile = "./cppmutithread/data/train_data1.txt";

    // string testFile = "./data/test_data.txt";
    // string predictFile = "./projects/student/result.txt";

    // string answerFile = "./projects/student/answer.txt";






	//DO SOMETHING
	int start = clock();
	// cout << "this is start" << endl;
    LR logist(trainFile, testFile, predictFile);
	// cout<<" the  load file cost is"<<(" %.3lf\n", float(clock() - start) / CLOCKS_PER_SEC)<<endl;


    cout << "ready to train model" << endl;
    // start = clock();
    logist.train();
	// cout<<" the  train time cost is"<<(" %.3lf\n", float(clock() - start) / CLOCKS_PER_SEC)<<endl;
    // cout << "training ends, ready to store the model" << endl;
    logist.storeModel();

#ifdef TEST
    cout << "ready to load answer data" << endl;
    loadAnswerData(answerFile, answerVec);
#endif

    // cout << "let's have a prediction test" << endl;
    start = clock();
    logist.predict();
	// cout<<" the  preidct file  cost is"<<(" %.3lf\n", float(clock() - start) / CLOCKS_PER_SEC);

#ifdef TEST
    loadAnswerData(predictFile, predictVec);
    cout << "test data set size is " << predictVec.size() << endl;
    correctCount = 0;
    for (int j = 0; j < predictVec.size(); j++) {
        if (j < answerVec.size()) {
            if (answerVec[j] == predictVec[j]) {
                correctCount++;
            }
        } else {
            cout << "answer size less than the real predicted value" << endl;
        }
    }

    accurate = ((float)correctCount) / answerVec.size();
    cout << "the prediction accuracy is " << accurate << endl;
#endif

    return 0;
}