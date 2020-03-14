/*
 * File: optimizer.cpp Author: Siomkos Date:2020.2.1
 */

#include <iostream>
#include <vector>
// #include "optimizer.h"
// #include "objfunc.h"
#include <fstream>
using namespace std;
#define M 5

/*
 * File: objfunc.h Author: Siomkos  Date: 2020.2.1
 */

#include <iostream>
using namespace std;
template<class T>
class ObjFunc
{
	T* x;			//自变量
	T* g;			//自变量x处的梯度向量
	T value; 		//函数值
	size_t fsize;	//函数维度
	T (*pfun)(T*, size_t); 	//目标函数指针
	void (*pdfun)(T*, size_t, T*);	//梯度函数指针

public:
	//构造函数
	ObjFunc(size_t size, T (*fun1)(T*, size_t), void(*fun2)(T*, size_t, T*))
	{
		pfun = fun1;
		pdfun = fun2;
		x = new T[size];
		g = new T[size];
		fsize = size;
		value = 0;
	}
	~ObjFunc(){delete[] x; delete[] g;}
	//获取自变量值
	void set_x(T* x1){
		for(int i = 0; i < fsize; ++i)
			x[i] = x1[i];
	}
	void set_g(){ pdfun(x, fsize, g);}
		//计算梯度值
	void set_value(){value = pfun(x, fsize);} //计算目标函数值
	size_t size(){return fsize;}	//返回维度
	void get_x(T* out){				//输出函数自变量
		for(int i = 0; i < fsize; ++i)
			out[i] = x[i];
	}
	void get_g(T* out){		//输出梯度值至out

		for(int i = 0; i < fsize; ++i)
			out[i] = g[i];
	}							
	friend ostream& operator<<(ostream &o, ObjFunc<float> &f);
	friend ostream& operator<<(ostream &o, ObjFunc<double> &f);

};

class Optimizer{
public:
	Optimizer(){}
	void lbfgs(ObjFunc<double>* f,		//目标函数类
				double* x0,				//初始值
				double gamma,		//步长
				const double err,	//最大允许误差
				const size_t max_it);//最大迭代次数
};


void Optimizer::lbfgs(ObjFunc<double>* f,		//目标函数类
			double* x0,				//初始值
			double gamma,		//步长
			const double err,	//最大允许误差
			const size_t max_it)//最大迭代次数
{	

	size_t dim = f->size();	//函数自变量的维度
	vector<double*> ps, py;			//存储sn ... sn-m+1, yn ... y_n-m+1
	
	//分配内存空间
	for(int i = 0; i < M; ++i){
		double* p1 = new double[dim];
		double* p2 = new double[dim];

		ps.push_back(p1);
		py.push_back(p2);
	}

	f->set_x(x0);	//初始化x0
	f->set_g();		//初始化g0

	double* xn = new double[dim];			//存储前一步的自变量值
	double* dn = new double[dim];			//存储前一步的更新方向
	double* xn_1 = new double[dim];			//存储当前的自变量值
	double* gn_1 = new double[dim];			//存储当前的梯度值
	double* gn = new double[dim];				//存储之前的梯度
	double* rho = new double[M];	//存储rho数组
	double* alpha = new double[M];	//存储后向循环中的alpha
	vector<double> error;
	

	f->get_g(dn);	//保存原函数的梯度信息
	for(size_t k = 0; k < max_it; ++k){
		//cout << *f << endl;
		f->get_x(xn);	//保存函数自变量值，深拷贝
		f->get_g(gn);	//保存当前梯度信息
		//更新自变量值
		for(int i = 0; i < dim; ++i){
			xn_1[i] = xn[i] - gamma * dn[i]; 
		}
		//校验是否结束迭代
		double ierr = 0;
		for(int i = 0; i < dim; ++i)
			ierr += (xn_1[i] - xn[i]) * (xn_1[i] - xn[i]);
		cout << "Error: " << ierr << " at " << k << " times." << endl;
		error.push_back(ierr);

		if(ierr < err) break;

		//更新函数
		f->set_x(xn_1);
		f->set_g();
		f->set_value();
		f->get_g(gn_1);	//保存当前梯度

		//更新ps, py
		if(k < M){
			for(int i = 0; i < dim; ++i){
				ps[k][i] = xn_1[i] - xn[i];
				py[k][i] = gn_1[i] - gn[i];
				rho[k] += ps[k][i] * py[k][i];
			}
			rho[k] = 1.0 / rho[k];
		}
		else{
			//更新sn
			double* p0 = ps[0];
			for(int i = 0; i < ps.size()-1; ++i){
				ps[i] = ps[i+1];
			}
			ps[M-1] = p0;

			//更新yn
			p0 = py[0];
			for(int i = 0; i < py.size()-1; ++i){
				py[i] = py[i+1];	
			}
			py[M-1] = p0;

			//更新当前的sk,yk
			//更新rho
			for(int i = 0; i < M-1; ++i){
				rho[i] = rho[i+1];
			}
			rho[M-1] = 0;
			for(int i = 0; i < dim; ++i){
				ps[M-1][i] = xn_1[i] - xn[i];
				py[M-1][i] = gn_1[i] - gn[i];
				rho[M-1] += ps[M-1][i] * py[M-1][i]; 
			}
			rho[M-1] = 1.0 / rho[M-1];		
		}
		//计算更新方向
		int L = k;
		if(k > M){
			L = M;
		}
		f->get_g(dn);	//初始化q,q与dn可以共用一个变量

		//后向循环
		int j = 0;
		for(int i = L-1; i >= 0; --i){
			alpha[i] = 0;
			for(int s = 0; s < dim; ++s){
				alpha[i] += ps[i][s] * dn[s];
			}
			alpha[i] = rho[i] * alpha[i];
			
			//更新q
			for(int s = 0; s < dim; ++s){
				dn[s] = dn[s] - alpha[i] * py[i][s];
			}
		}
		//前向循环
		double beta = 0;
		for(int i = 0; i < L; ++i){
			for(int s = 0; s < dim; ++s){
				beta += py[i][s] * dn[s];
			}
			beta = rho[i] * beta;
			//更新q
			for(int s = 0; s < dim; ++s){
				dn[s] = dn[s] + (alpha[i] - beta) * ps[i][s];
			}
		}
	}
	//写入txt文件
	ofstream out("error.txt");
	for(int i = 0; i < error.size(); ++i)
		out << error[i] << "\t";
	out.close();

	//释放内存
	for(int i = 0; i < ps.size(); ++i){
		delete[] ps[i];
		ps[i] = NULL;
		delete[] py[i];
		py[i] = NULL;
	}
	delete[] dn;
	dn = NULL;
	delete[] xn_1;
	xn_1 = NULL;
	delete[] xn;
	xn = NULL;
	delete[] gn;
	gn = NULL;
	delete[] rho;
	rho = NULL;
	delete[] alpha;
	alpha = NULL;
}



double q(double* x, size_t n)
{
	double result = 0;
	for(int i = 0; i < n; ++i)
		result += x[i] * x[i];
	return result;
} 

void gradient(double* x, size_t n, double* g)
{
	for(int i = 0; i < n; ++i)
		g[i] = 2 * x[i];
}


int main(){
	ObjFunc<double> f(5, q, gradient);

	double* x = new double[5];

	for(int i = 0; i < 5; ++i)
		x[i] = 10;

	f.set_x(x);
	f.set_g();
	f.set_value();
	cout << f << endl;
	cout << "优化" << endl;
	Optimizer op;
	op.lbfgs(&f, x, 0.1, 0.001, 100);
	cout << f << endl;
	delete[] x;
	x = NULL;
	return 0;

}