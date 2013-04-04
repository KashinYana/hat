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
			listNewWords = []
			for word in wordsInput:
				listNewWords.append(Words(user = request.user, word = word))
			Words.objects.bulk_create(listNewWords)
	return HttpResponseRedirect('/words/')

def delete_word(request):
	if request.method == "POST":
		wordsForDelete = request.POST.getlist('del_word')
		wordsForDelete = Words.objects.filter(word__in = wordsForDelete)
		if len(wordsForDelete) > 0:
			wordsForDelete = wordsForDelete[0]
		wordsForDelete.delete()
	return HttpResponseRedirect('/words/')

def create_game(request):
	words = ""
	if request.method == "POST":
		words = []
		players = request.POST.getlist('player')
		players = map(int, players)
		numberWords = int(request.POST.get('number_words'))
		nameGame = request.POST.get('name_game')
		for player in players:
			words += Words.objects.filter(user = User.objects.get(id=player))[0:numberWords]
		players = User.objects.filter(id= players[0])
		newGame = Games(name=nameGame)
		newGame.save()
		newGame.words = words
		newGame.players = players
		words = map(lambda x: (x.word, x.user.id), words)
		json = simplejson.dumps({'gameId':newGame.id, 'words':words})
	return request_words(request, json)

def request_words(request, words = ""):
	users = User.objects.all()
	return render_to_response('request_words.html', {'users':users, 'answer':words}, context_instance=RequestContext(request))

def new_result_game(request, accept = ""):
	return render_to_response('new_result_game.html', {'accept': accept}, context_instance=RequestContext(request))	

def send_result_game(request):
	accept = ""
	if request.method == "POST":
		dataGame = request.POST.get('data_game')
		gameId = int(simplejson.loads(dataGame)['gameId'])
		statistics = simplejson.loads(dataGame)['statistics']
		for explanation in statistics:
			newDataGame = DataGames(gameId_id = gameId, word_id = int(explanation[0]), playerFrom_id = int(explanation[1]), playerTo_id = int(explanation[2]))
			newDataGame.save()
		accept = "Данные успешно сохранены."
	return new_result_game(request, accept)

def words(request):
	form = WordForm()
	if request.method == "POST":
		form = WordForm(request.POST)
	wordsUser = Words.objects.filter(user = request.user)
	return render_to_response('words.html', {'wordsUser': wordsUser, 'form':form}, context_instance=RequestContext(request))
