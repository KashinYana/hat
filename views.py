# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from words.models import Words
from games.models import Games
from dataGames.models import DataGames
from forms import WordForm
from django.contrib.auth.models import User
import simplejson
import random
import datetime

from game.models import Game, Word, ReportGame, UserWord

def main(request):
	return render_to_response('base.html', {} , context_instance=RequestContext(request))

def save_words(request):
	if request.method == 'POST':
		form = WordForm(request.POST)
		if(form.is_valid()) :
			wordsInput = []
			for i in range(1, 11):
				word = form.cleaned_data["word" + str(i)].split()
				if(len(word) > 0):
					wordsInput.append(' '.join(word))
			for wordInput in wordsInput:
				if len(Word.objects.filter(word = wordInput)) == 0:
					wordNew = Word(word = wordInput)
					wordNew.save()
				word = Word.objects.get(word = wordInput)
				if len(UserWord.objects.filter(user = request.user, word = word)) == 0:
					userWordNew = UserWord(user = request.user, word = word)
					userWordNew.save()				
	return HttpResponseRedirect('/words/')


def delete_word(request):
	if request.method == "POST":
		wordsForDelete = request.POST.getlist('del_word')
		words = Word.objects.filter(word__in = wordsForDelete)
		wordsForDelete = UserWord.objects.filter(word__in = words, user = request.user)
		for word in wordsForDelete:
			if len(word.game.all()) == 0:
				if len(word.word.user.all()) <= 1:
					word.word.delete()
					word.delete()
	return HttpResponseRedirect('/words/')

def create_game(request):
	words = ""
	if request.method == "POST":
		words = []
		players = request.POST.getlist('player')
		players = map(int, players)
		numberWords = int(request.POST.get('number_words'))
		nameGame = request.POST.get('name_game')
		
		password = random.randint(1, 100)
		newGame = Game(name=nameGame, creator = request.user, password = password)
		newGame.save()
		
		for player in players:
			newGame.user.add(User.objects.get(id = player))
			words += UserWord.objects.filter(user = User.objects.get(id=player))[0:numberWords]
		
		for word in words:
			newGame.userword_set.add(word)
			
		#words = map(lambda x: {'word': x.word.word, 'id': x.id}, words)
		#json = simplejson.dumps({'gameId':newGame.id, 'words':words})
		gameId = newGame.id
	return request_words(request, gameId, password)


def request_words(request, gameId = 0, password = ""):
	users = User.objects.all()
	#if json == "":
	return render_to_response('request_words.html', {'users':users, 'answer':password, 'gameId': gameId}, context_instance=RequestContext(request))
	#else:
	#	return HttpResponse(json)

def new_result_game(request, accept = ""):
	return render_to_response('new_result_game.html', {'accept': accept}, context_instance=RequestContext(request))	

def send_result_game(request):
	accept = ""
	if request.method == "POST":
		dataGame = request.POST.get('data_game')
		gameId = int(simplejson.loads(dataGame)['gameId'])
		statistics = simplejson.loads(dataGame)['statistics']

		for explanation in statistics:
			newDataGame = ReportGame(gameId_id = gameId, word_id = int(explanation['wordId']), \
				userFrom_id = int(explanation['userFrom']), userTo_id = int(explanation['userTo']),\
				outcome = int(explanation['outcome']), duration = int(explanation['duration']), \
				tour = int(explanation['tour']) )
			newDataGame.save()
		accept = "Данные успешно сохранены."
	return new_result_game(request, accept)

def words(request):
	form = WordForm()
	if request.method == "POST":
		form = WordForm(request.POST)
	wordsUser = UserWord.objects.filter(user = request.user)
	return render_to_response('words.html', {'wordsUser': wordsUser, 'form':form}, context_instance=RequestContext(request))


def history(request):
	games = Game.objects.filter(user = request.user)
	return render_to_response('history.html', {'games':games}, context_instance=RequestContext(request))

def number_rounds(user, game):
	explanationTo = ReportGame.objects.filter(gameId = game, userTo = user)
	explanationFrom = ReportGame.objects.filter(gameId = game, userFrom = user)
	toursTo = filter(lambda x: x.tour, explanationTo)
	toursFrom = filter(lambda x: x.tour, explanationFrom)
	tours = list(set(toursFrom + toursTo))
	return len(tours)

def rating_users(users, game):	
	rating = []
	for user in users:
		scroteMainTime = ReportGame.objects.filter(gameId = game, userFrom = user, outcome = 1).count() + \
			ReportGame.objects.filter(gameId = game, userTo = user, outcome__gt = 1).count()
		scroteExtraTime = ReportGame.objects.filter(gameId = game, userFrom = user, outcome = 2).count() + \
			ReportGame.objects.filter(gameId = game, userTo = user, outcome__gt = 2).count()	
		numberRounds = number_rounds(user, game)
		rating.append((user, scroteExtraTime + scroteMainTime, \
			scroteMainTime, scroteExtraTime, numberRounds))

	rating = sorted(rating, key = lambda x: x[1], reverse=True)
	rangeForRating = range(1, len(rating) + 1)
	return zip(rangeForRating, rating)

class FeatureWords:
	def __init__(self):
		self.duration = 0
		self.numAttempts = 0
		self.latestDuration = 0
		self.latestUserFrom = 0
		self.latestUserTo = 0
		self.tour = -1
	def add(self, attempt):
		self.numAttempts += 1
		self.duration += attempt.duration
		if self.tour < attempt.tour and attempt.outcome > 0:
			self.latestDuration = attempt.duration
			self.tour = attempt.tour
			self.latestUserTo = attempt.userTo
			self.latestUserFrom = attempt.userFrom

def statistics_words(game):
	words = UserWord.objects.filter(game = game)
	reportWords = ReportGame.objects.filter(gameId = game)
	table = dict()
	for word in words:
		if not table.has_key(word.word):
			table[word.word] = FeatureWords()
	for word in reportWords:
		table[word.word.word].add(word)
	return table

def statistics_pair_users(users, game):
	rating = []
	numPairs = 0
	for i in range(len(users)):
		for j in range(i + 1, len(users)):
			numPairs += 1
			rating.append([users[i], users[j],\
				ReportGame.objects.filter(gameId = game, userFrom=users[i], userTo = users[j], outcome__gt = 0).count(),\
				ReportGame.objects.filter(gameId = game, userFrom=users[j], userTo = users[i], outcome__gt = 0).count()] )

	return zip(range(1, numPairs + 1), rating)

def history_game(request, gameId):
	game = Game.objects.get(id = int(gameId))
	users = game.user.all()
	ratingUsers = rating_users(users, game)
	statisticsWords = statistics_words(game)
	reportGame = ReportGame.objects.filter(gameId = game)
	ratingPairUsers = statistics_pair_users(users, game)
	return render_to_response('history_game.html', {'game':game, 'reportGame':reportGame,\
	  	'rating' : ratingUsers, 'ratingPairUsers': ratingPairUsers, 'statisticsWords':statisticsWords.items()}, context_instance=RequestContext(request))

def queue_games(request):
	games = Game.objects.filter(creator = request.user)
	return render_to_response('queue_games.html', {'games':games},context_instance=RequestContext(request))

def take_data(request):	
	json = {}
	
	if request.method == "POST":
		gameId = int(request.POST.get('gameId'))
		password = int(request.POST.get('password'))
		game =  Game.objects.filter(id = gameId)
	
		if len(game) == 1 and game[0].password == password:
			users = game[0].user.all()
			users = map(lambda x: {'userId':x.id, 'userName':x.get_full_name() }, users)
			words = game[0].userword_set.all()
			words = map(lambda x: {'word': x.word.word, 'id': x.id}, words)
			json = simplejson.dumps({'gameId':game[0].id, 'words':words, 'users':users})
	
	return HttpResponse(json)		

def imitator_request(request):

	return render_to_response('imitator_request.html', context_instance=RequestContext(request))