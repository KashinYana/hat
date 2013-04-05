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
		
		newGame = Game(name=nameGame)
		newGame.save()
		
		for player in players:
			words += UserWord.objects.filter(user = User.objects.get(id=player))[0:numberWords]
		
		for word in words:
			print word
			newGame.userword_set.add(word)
			#word.game.add(newGame)
			print word

		words = map(lambda x: {'word': x.word.word, 'id': x.id}, words)
		json = simplejson.dumps({'gameId':newGame.id, 'words':words})
	return request_words(request, json)


def request_words(request, json = ""):
	users = User.objects.all()
	if json == "":
		return render_to_response('request_words.html', {'users':users, 'answer':json}, context_instance=RequestContext(request))
	else:
		return HttpResponse(json)

def new_result_game(request, accept = ""):
	return render_to_response('new_result_game.html', {'accept': accept}, context_instance=RequestContext(request))	

def send_result_game(request):
	accept = ""
	if request.method == "POST":
		dataGame = request.POST.get('data_game')
		gameId = int(simplejson.loads(dataGame)['gameId'])
		statistics = simplejson.loads(dataGame)['statistics']

		for explanation in statistics:
			newDataGame = ReportGame(gameId_id = gameId, word_id = int(explanation['wordId']), userFrom_id = int(explanation['userFrom']), userTo_id = int(explanation['userTo']))
			newDataGame.save()
		accept = "Данные успешно сохранены."
	return new_result_game(request, accept)

def words(request):
	form = WordForm()
	if request.method == "POST":
		form = WordForm(request.POST)
	wordsUser = Word.objects.filter(user = request.user)
	return render_to_response('words.html', {'wordsUser': wordsUser, 'form':form}, context_instance=RequestContext(request))


def history(request):
	games = Game.objects.all()
	return render_to_response('history.html', {'games':games}, context_instance=RequestContext(request))

def history_game(request, gameId):
	game = Game.objects.get(id = int(gameId))
	reportGame = ReportGame.objects.filter(gameId = game)
	return render_to_response('history_game.html', {'game':game, 'reportGame':reportGame}, context_instance=RequestContext(request))

