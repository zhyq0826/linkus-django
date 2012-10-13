#-*- coding:utf-8 -*-
from auth.models import User
from follow.models import check_user_follow

#当前用户信息和被访问用户信息
def user_info_proc(request):
	current='empty_current'
	current_nav=''
	title=dict_title(request.path)
	if request.path.endswith("ask") or request.path.endswith('question')  or request.path.startswith('answer'):
		current='ask_current'

	if request.path.endswith('blog'):
		current='blog_current'

	if request.path.endswith('topic') or request.path.endswith('topic/replyed'):
		current='topic_current'

	if request.path.endswith('follow') or request.path.endswith('follower'):
		current='follow_current'

	if request.path.endswith('profile'):
		current='profile_current'

	if request.path.startswith('/read/'):
		current_nav='read_current_nav'

	if request.path.startswith('/ask/'):
		current_nav='ask_current_nav'

	if request.path.startswith('/topic/'):
		current_nav = 'topic_current_nav'

	if request.path.startswith('/i/college/'):
		current_nav = 'college_current_nav'




	u = request.session['user']
	current_user = request.session['current_user']

	return {
	 current_nav:'current_nav',
	 'user':u,
	 current:'current',
	 'pagetitle':title,
	 'current_user':current_user,
	 'avatar_url':'/img/avatar/',
	 'avatar_url_temp':'/img/avatar/temp/',
	}

#登录用户和被访问用户url
def user_url_proc(request):
	u = request.session['user']
	current_user = request.session['current_user']

	if current_user.url:
		current_user_url = '/people/'+current_user.url
	else:
		current_user_url = '/people/'+str(current_user.id)

	if u.url:
		user_url = '/people/'+u.url
	else:
		user_url = '/people/'+str(u.id)

	return {
	 'user_url':user_url,
	 'current_user_url':current_user_url,
	}

#用户关注信息
def user_follow_proc(request):
	u = request.session['user']
	current_user = request.session['current_user']
	if check_user_follow(current_user.id,u.id):
		return{
		'followed':'true'
		}
	else:
		return{

		}


def dict_title(path_key):
	data={
		'/':'首页',
		'/i/ask/':'我的问题',
		'/i/iask/':'提问',
		'/i/ask/collect/':'我的收藏',
		'/i/answer/':'我的回答',
		'/i/question/':'问我',
		'/i/topic/':'我的话题',
		'/i/topic/replyed/':'我回应过的话题',
		'/i/topic/new/':'新话题',
		'/i/article/':'日志',
		'/i/article/write/':'新日志',
		'/i/setting/':'设置',
		'/i/setting/profile/':'个人资料',
		'/i/setting/school/':'院校',
		'/i/setting/password/':'修改密码',
		'/i/setting/account/':'修改账户',
	}

	try:
		return data[path_key]
	except KeyError:
		return ''
