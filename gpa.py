# -*- coding: utf-8 -*-  
#---------------------------------------  
#   程序：南京大学爬虫  
#   版本：1.0  
#   作者：lzx  
#   日期：2016-10-13  
#   语言：Python 3  
#   操作：输入学号、密码和学期  
#   功能：输出各科成绩与学期学分绩  
#--------------------------------------- 

import urllib.parse
import urllib.request
import http.cookiejar
import re
import sys
import io
from bs4 import BeautifulSoup
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')


class NJU_grade_spider:
	def __init__(self):
		self.loginUrl = 'http://jw.nju.edu.cn:8080/jiaowu/login.do'
		self.gradeUrl = 'http://jw.nju.edu.cn:8080/jiaowu/student/studentinfo/achievementinfo.do?method=searchTermList'
		self.cookie = http.cookiejar.CookieJar()    
		self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
		self.total_grade_all = 0
		self.total_weight_all = 0
		
	def nju_init(self):
		self.stu_num = input('请输入学号：')
		self.stu_pwd = input('请输入密码：')
		# self.stu_num = '141170028'
		# self.stu_pwd = '830317'
		self.post_login_data = urllib.parse.urlencode({'userName':self.stu_num,'password':self.stu_pwd,})
		login_request = urllib.request.Request( url = self.loginUrl, data = self.post_login_data.encode("utf-8") )
		login_result = self.opener.open(login_request)
		age = int(self.stu_num[0:2])
		term = int(input('请输入你要查询哪个学期的成绩(如第一学期请输入1，若要查询所有学期请输入0)：'))
		# term = 0
		if term == 0:
			total_term = (16-age)*2
			for i in range(1,total_term+2):
				self.get_grade(age,i)
			self.get_total_gpa(total_term)
		else:
			self.get_grade(age,term)
		
		# self.get_grade(age)
		
	def get_grade(self, age = 14, term = 1):
		# self.lesson_type_list = ['通修','平台','核心']
		
		term_tmp = term
		while term_tmp-2>0:
			age += 1
			term_tmp -= 2			
		term_str = '20'+str(age)+str(term_tmp)
		post_grade_data = urllib.parse.urlencode({'termCode':term_str})
		grade_request = urllib.request.Request( url = self.gradeUrl, data = post_grade_data.encode('utf-8') )
		grade_result = self.opener.open(grade_request)
		mygradepage = grade_result.read().decode('utf-8')
		soup = BeautifulSoup(mygradepage,'lxml')
		trs = soup.find_all('tr',class_=['TABLE_TR_02','TABLE_TR_01'])
		lesson_names = []
		lesson_type = []
		lesson_weights = []
		lesson_grades = []
		for j1 in range(len(trs)):
			_soup = BeautifulSoup(str(trs[j1]),'lxml')
			tds = _soup.find_all('td')
			# tds[2] = alignment(str(tds[2]),20)
			for j2 in range(len(tds)):
				tds[j2] = tds[j2].get_text().strip()
			# for td in tds:
				# td = td.get_text().strip()
			lesson_names.append(self.alignment(str(tds[2]),30))
			lesson_type.append(tds[4])
			tds[5] = int(float(tds[5]))
			lesson_weights.append(tds[5])
			# lesson_grades.append(str(int(tds[6])))
			tds[6] = int(float(tds[6]))
			lesson_grades.append(tds[6])
		print('第%d学期成绩如下：'%term)
		for j in range(len(trs)):
			print('%s %2s  %1d  %3d'%(lesson_names[j],lesson_type[j],lesson_weights[j],lesson_grades[j]))
		
		# total_grade = 0
		total_grade = 0
		total_weight = 0
		# total_weight = 0
		
		for j in range(len(trs)):
			# if lesson_type[j] in self.lesson_type_list:
				# total_grade += lesson_weights[j]*lesson_grades[j]
				# total_weight += lesson_weights[j]
			total_grade += lesson_weights[j]*lesson_grades[j]
			total_weight += lesson_weights[j]
		# gpa = total_grade/total_weight/20
		self.total_grade_all += total_grade
		self.total_weight_all += total_weight
		gpa = total_grade/total_weight/20
		print('第%d学期全部课程学分绩为：%f\n'%(term, gpa))
		# print('第%d学期全部课程学分绩为：%f   必修课程学分绩为：%f'%(term, gpa_all, gpa))

	def get_total_gpa(self,total_term):
		gpa_all = self.total_grade_all/self.total_weight_all/20
		print('%d学期总学分绩为%f'%(total_term,gpa_all))
			
	
	def alignment(self, str1, space, align = 'left'):
		length = len(str1.encode('gb2312'))
		space = space - length if space >=length else 0
		if align == 'left':
			str1 = str1 + ' ' * space
		elif align == 'right':
			str1 = ' '* space +str1
		elif align == 'center':
			str1 = ' ' * (space //2) +str1 + ' '* (space - space // 2)
		return str1
		
	
myspider = NJU_grade_spider()
myspider.nju_init()