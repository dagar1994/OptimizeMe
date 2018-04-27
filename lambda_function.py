# -*- coding: utf-8 -*-
"""
This skill gives you stats about the current ongoing crypto currency market
"""

from __future__ import print_function
import requests
import json
import inflect
from bs4 import BeautifulSoup

offset = 0

def build_speechlet_response_stop(title, output, reprompt_text, should_end_session):
    return {
	'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },

	"directives": [
                {
                    "type": "AudioPlayer.Stop",
                }
            ],

        'card': {
            'type': 'Simple',
            'title':  title,
            'content':  "Daily plus one"
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }






def build_speechlet_response_audio(title, url, reprompt_text, should_end_session,offset,output):
    return {
         'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },

	"directives": [
                {
                    "type": "AudioPlayer.Play",
                    "playBehavior": "REPLACE_ALL",
                    "audioItem": {
                        "stream": {
                            "token": "12345",
                            "url": url,
                            "offsetInMilliseconds": offset
                        }
                    }
                }
            ],

        'card': {
            'type': 'Simple',
            'title':  title,
            'content':  "Daily Plus one"
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }





def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }




# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title':  title,
            'content':  output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------


def help_response():
    session_attributes = {}
    card_title = "Help"
    speech_output = """
Say, daily plus one or say whats my flash briefing
			""".strip() 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Say, daily plus one or say whats my flash briefing"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def pause_response():
    session_attributes = {}
    card_title = "User Ended the skill"
    speech_output = "" 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "" 
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response_stop(
        card_title, speech_output, reprompt_text, should_end_session))





def cancel_response():
    session_attributes = {}
    card_title = "User Ended the skill"
    speech_output = "Thank you for using Optimize me, Go do what you like, just make sure you do it wise." 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Thank you for using Optimize me, Go do what you like, just make sure you do it wise." 
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response_stop(
        card_title, speech_output, reprompt_text, should_end_session))




def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Optimize Me. " \
	            "The world’s best wisdom distilled into inspiring, impactful and practical micro-lessons you can apply to your life today and every day. Say daily plus one or flash briefing"\
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Welcome to Optimize Me. " \
	            "The world’s best wisdom distilled into inspiring, impactful and practical micro-lessons you can apply to your life today. And every day. Say daily plus one or flash briefing"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))




def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Optimize me, come back tomorrow for daily ispiration and motivation." 
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def dailyPlusOne(intent,session):
    session_attributes = {}
    reprompt_text = None
    res = requests.get("https://www.optimize.me/wp-json/posts?type=plus-one")
    jsonData = json.loads(res.content)
    mp3Link = jsonData[0]['acf']['plus1_class_mp3']
    should_end_session = True
    return build_response({}, build_speechlet_response_audio(
        "Daily +1", mp3Link, None, should_end_session,0,"Daily plus one by brian johnson"))

		    	    
	
    
def resume_response(intent,session):
    session_attributes = {}
    reprompt_text = None
    res = requests.get("https://www.optimize.me/wp-json/posts?type=plus-one")
    jsonData = json.loads(res.content)
    mp3Link = jsonData[0]['acf']['plus1_class_mp3']
    should_end_session = True
    return build_response({}, build_speechlet_response_audio(
        "Daily +1", mp3Link, None, should_end_session,0,"Daily plus one by brian johnson"))


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "AMAZON.HelpIntent":
        return help_response()
    elif intent_name == "AMAZON.CancelIntent":
	return cancel_response()
    elif intent_name == "AMAZON.StopIntent":
        return cancel_response()
    elif intent_name == "AMAZON.PauseIntent":
	return pause_response()
    elif intent_name == "AMAZON.ResumeIntent":
	return resume_response(intent, session)
    elif intent_name == "dailyPlusOne":
	return dailyPlusOne(intent, session)
    elif intent_name == "" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

def on_playback_finished(playbackRequest, session):
    return cancel_response()


def on_playback_stopped(playbackRequest, session):
    global offset
    offset = playbackRequest["offsetInMilliseconds"]	


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
    elif event['request']['type'] == "AudioPlayer.PlaybackFinished":
	return on_playback_finished(event['request'], event['session'])
    elif event['request']['type'] == "AudioPlayer.PlaybackStopped":
	return on_playback_stopped(event['request'], event['session'])
	
